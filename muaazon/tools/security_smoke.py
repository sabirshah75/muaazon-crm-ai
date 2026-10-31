#!/usr/bin/env python3
"""Non-destructive checks against a loopback-only CRM installation."""
from urllib import request, error
import json
import sys
base = "http://localhost:3000"
checks={}
def fetch(path, method='GET', data=None):
    payload=json.dumps(data).encode() if data is not None else None
    req=request.Request(base+path, data=payload, method=method,
       headers={'Content-Type':'application/json'} if data is not None else {})
    try:
        with request.urlopen(req, timeout=12) as response:
            return response.status, response.headers, response.read(131072)
    except error.HTTPError as ex:
        return ex.code, ex.headers, ex.read(131072)

status, headers, html = fetch('/')
checks['root_status']=status
checks['branded_title']=b'<title>Muaazon CRM AI</title>' in html
checks['no_env_key_leak']=b'PG_DATABASE_URL' not in html and b'ENCRYPTION_KEY' not in html
checks['html_content_type']=headers.get('content-type','').startswith('text/html')
checks['x_content_type_options']=headers.get('x-content-type-options',None)
checks['content_security_policy']=bool(headers.get('content-security-policy'))
checks['x_frame_options']=headers.get('x-frame-options',None)

status, _, body = fetch('/healthz')
checks['health_status']=status
status, _, manifest = fetch('/manifest.json')
checks['manifest_status']=status
checks['manifest_name']=json.loads(manifest.decode()).get('name') if status==200 else None

status, _, payload = fetch('/graphql','POST',{'query':'query { currentUser { id } }'})
checks['anonymous_query_http']=status
try:
    parsed=json.loads(payload.decode())
except Exception:
    parsed={}
checks['anonymous_current_user']=parsed.get('data',{}).get('currentUser') if isinstance(parsed.get('data'),dict) else None
checks['anonymous_graphql_errors']=bool(parsed.get('errors'))

print(json.dumps(checks,indent=2))
critical=(checks['root_status'] != 200 or checks['health_status'] != 200 or
 not checks['branded_title'] or not checks['no_env_key_leak'] or
 checks['manifest_name']!='Muaazon CRM AI' or checks['anonymous_current_user'] is not None)
if critical:
    sys.exit(1)
print('LOOPBACK_SECURITY_SMOKE_PASS; full independent security review still required')
