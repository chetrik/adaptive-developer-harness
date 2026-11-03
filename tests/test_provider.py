import json
import threading
import unittest
from http.server import BaseHTTPRequestHandler,HTTPServer
from adaptive_harness.provider import ollama_assessment
from adaptive_harness.contracts import ROOT,HarnessError
from test_selection import fixture

class ProviderTests(unittest.TestCase):
    def test_real_local_http_contract_keeps_inference_untrusted(self):
        a=fixture();proposal={k:a[k] for k in ('project_type','stage','project_scale','feature_size','surfaces')}
        proposal['facts']={k:v['value'] for k,v in a['facts'].items()};received=[]
        class Handler(BaseHTTPRequestHandler):
            def log_message(self,*args):pass
            def do_POST(self):
                received.append((self.path,json.loads(self.rfile.read(int(self.headers['Content-Length'])))))
                body=json.dumps({'message':{'content':json.dumps(proposal)}}).encode()
                self.send_response(200);self.end_headers();self.wfile.write(body)
        server=HTTPServer(('127.0.0.1',0),Handler);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        try:r=ollama_assessment(ROOT/'examples/PRD_CALCULATOR.md','synthetic-model',endpoint='http://127.0.0.1:'+str(server.server_port))
        finally:server.shutdown();thread.join();server.server_close()
        self.assertEqual(received[0][0],'/api/chat');self.assertFalse(received[0][1]['stream'])
        self.assertEqual(r['assessment']['host']['capabilities']['native_skills']['value'],'unknown')
        self.assertEqual(r['assessment']['facts']['personal_data']['basis'],'inferred')
        self.assertEqual(r['assessment']['prd']['reading']['status'],'partial')
        self.assertEqual(r['assessment']['model_provider']['kind'],'ollama')
    def test_no_remote_upload_or_endpoint_tricks(self):
        for url in ('https://example.org','http://127.0.0.1@evil.test','http://127.0.0.1/redirect','file:///tmp/a','http://localhost?token=x'):
            with self.assertRaises(HarnessError):ollama_assessment(ROOT/'examples/PRD_CALCULATOR.md','model',endpoint=url)
    def test_unavailable_local_provider_is_explicit(self):
        from unittest.mock import patch
        import urllib.error
        with patch('urllib.request.OpenerDirector.open',side_effect=urllib.error.URLError('unavailable')):
            with self.assertRaisesRegex(HarnessError,'Local Ollama unavailable'):ollama_assessment(ROOT/'examples/PRD_CALCULATOR.md','model')
