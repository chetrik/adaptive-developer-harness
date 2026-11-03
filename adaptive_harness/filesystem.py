"""Bounded filesystem inspection. Never follows target symlinks."""
import os
import stat
from pathlib import Path, PurePosixPath
from .contracts import HarnessError, digest, fingerprint

MAX_FILES = 10000
MAX_BYTES = 64 * 1024 * 1024


def root_path(target):
    p = Path(os.path.abspath(target))
    for part in [p, *p.parents]:
        if part.is_symlink():
            raise HarnessError('Target root contains a symlink')
    if not p.is_dir():
        raise HarnessError('Target directory must exist')
    return p


def safe_path(root, name):
    if not isinstance(name, str) or '\\' in name or '\x00' in name:
        raise HarnessError('Invalid target path')
    p = PurePosixPath(name)
    if p.is_absolute() or name != p.as_posix() or any(x in ('..', '.', '') for x in p.parts):
        raise HarnessError('Unsafe target path')
    if not p.parts or any(x == '.git' or x.startswith('.env') for x in p.parts):
        raise HarnessError('Protected target path')
    allowed = name == 'AGENTS.md' or name.startswith(('.adaptive-harness/', '.agents/skills/adh-', '.codex/agents/adh-'))
    if not allowed:
        raise HarnessError('Path outside harness scope')
    current = root
    for part in p.parts:
        current = current / part
        if current.is_symlink():
            raise HarnessError('Symlink target path')
        if current.exists() and current != root / name and not current.is_dir():
            raise HarnessError('Non-directory path ancestor')
    if current.exists() and not current.is_file():
        raise HarnessError('Target is not a regular file')
    return current


def read_regular(path):
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_size > MAX_BYTES:
            raise HarnessError('Unsupported or oversized file')
        with os.fdopen(fd, 'rb', closefd=False) as stream:
            return stream.read(MAX_BYTES + 1)
    finally:
        os.close(fd)


def snapshot(target, *, exclude_sessions=False):
    root = root_path(target)
    entries = []
    size = 0
    for base, dirs, files in os.walk(root, followlinks=False):
        if exclude_sessions and Path(base)==root/'.adaptive-harness':
            dirs[:]=[n for n in dirs if n!='sessions']
        dirs.sort(); files.sort()
        if '.git' in dirs:
            dirs.remove('.git')
        for name in dirs + files:
            p = Path(base) / name
            rel = p.relative_to(root).as_posix()
            st = p.lstat()
            if len(entries) >= MAX_FILES:
                raise HarnessError('Target exceeds inspection file limit')
            if p.is_symlink():
                entries.append([rel, 'symlink', os.readlink(p)])
            elif stat.S_ISDIR(st.st_mode):
                entries.append([rel, 'directory'])
            elif stat.S_ISREG(st.st_mode):
                # Do not read credential material; metadata still detects ordinary changes.
                protected = any(x.startswith('.env') or x in ('.aws', '.ssh', '.credentials') for x in p.relative_to(root).parts)
                if protected:
                    entries.append([rel, 'protected', st.st_size, st.st_mtime_ns, st.st_ino])
                else:
                    size += st.st_size
                    if size > MAX_BYTES:
                        raise HarnessError('Target exceeds inspection byte limit')
                    entries.append([rel, digest(read_regular(p)), stat.S_IMODE(st.st_mode)])
            else:
                raise HarnessError('Special filesystem entry in target')
    # .git data and secrets never enter generated content; this is a consistency fingerprint.
    return fingerprint(entries)
