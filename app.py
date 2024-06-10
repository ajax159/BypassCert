from flask import Flask, request, jsonify
import urllib.request
import json
import ssl
import os

app = Flask(__name__)

def allowSelfSignedHttps(allowed):
    # Bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True) # This line is needed if you use self-signed certificate in your scoring service.

API_URL = 'http://158.23.249.180:80/api/v1/service/aks-shippingia/score'
API_KEY = '7fSDPRkvyknLR5qWvDtQ6gcB8J7sTb4T'

@app.route('/api/v1/service/aks-shippingia/score', methods=['POST'])
def proxy_request():
    data = request.get_json()

    body = str.encode(json.dumps(data))

    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + API_KEY}

    req = urllib.request.Request(API_URL, body, headers)

    try:
        response = urllib.request.urlopen(req)
        result = response.read()
        return jsonify(json.loads(result))
    except urllib.error.HTTPError as error:
        return jsonify({
            'status': error.code,
            'message': error.read().decode('utf8', 'ignore')
        }), error.code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)
