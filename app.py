from flask import Flask, request, jsonify
import json
from datetime import datetime
from collections import deque

app = Flask(__name__)
request_history = deque(maxlen=100)

@app.route('/api/execute', methods=['POST'])
def execute_code():
    try:
        data = request.get_json()
        
        request_info = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'ip': request.remote_addr,
            'method': request.method,
            'url': request.url,
            'data': data
        }
        request_history.append(request_info)
        
        if not data or 'source_code' not in data:
            return jsonify({'error': 'Missing source_code field'}), 400
        
        source_code = data['source_code']
        name = data.get('name', 'unknown')
        args = data.get('args', {})
        
        exec_globals = {}
        exec_locals = {}
        
        exec(source_code, exec_globals, exec_locals)
        
        if name in exec_locals and callable(exec_locals[name]):
            result = exec_locals[name](**args)
            return jsonify({'result': str(result), 'status': 'success'})
        else:
            return jsonify({'error': f'Function {name} not found'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>HELLO BRO !!!!</title>
        <meta charset="UTF-8">
        <style>
            body { 
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }
            h1 { 
                font-size: 120px;
                color: #fff;
                text-shadow: 4px 4px 8px rgba(0,0,0,0.3);
                margin: 0;
                font-weight: bold;
            }
            .link {
                position: absolute;
                top: 20px;
                right: 20px;
                color: #fff;
                text-decoration: none;
                font-size: 18px;
                background: rgba(255,255,255,0.2);
                padding: 10px 20px;
                border-radius: 5px;
            }
            .link:hover {
                background: rgba(255,255,255,0.3);
            }
        </style>
    </head>
    <body>
        <h1>HELLO BRO !!!!</h1>
        <a href="/requests" class="link">View Requests</a>
    </body>
    </html>
    '''

@app.route('/requests', methods=['GET'])
def show_requests():
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Request History</title>
        <meta charset="UTF-8">
        <style>
            body { 
                font-family: Arial, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background: #f5f5f5;
            }
            h1 { 
                color: #333;
                text-align: center;
            }
            .back-link {
                display: inline-block;
                margin-bottom: 20px;
                color: #667eea;
                text-decoration: none;
                padding: 8px 16px;
                background: #fff;
                border-radius: 5px;
            }
            .request-item {
                background: #fff;
                padding: 15px;
                margin: 10px 0;
                border-radius: 5px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .request-header {
                display: flex;
                justify-content: space-between;
                margin-bottom: 10px;
                padding-bottom: 10px;
                border-bottom: 1px solid #eee;
            }
            .timestamp {
                color: #666;
                font-size: 14px;
            }
            .ip {
                color: #667eea;
                font-weight: bold;
            }
            .request-data {
                background: #f9f9f9;
                padding: 10px;
                border-radius: 3px;
                margin-top: 10px;
                overflow-x: auto;
            }
            pre {
                margin: 0;
                white-space: pre-wrap;
                word-wrap: break-word;
            }
            .empty {
                text-align: center;
                color: #999;
                padding: 50px;
                font-size: 18px;
            }
        </style>
    </head>
    <body>
        <h1>Request History</h1>
        <a href="/" class="back-link">← Back to Home</a>
    '''
    
    if not request_history:
        html += '<div class="empty">No requests received yet.</div>'
    else:
        for req in reversed(list(request_history)):
            html += f'''
        <div class="request-item">
            <div class="request-header">
                <span class="timestamp">{req['timestamp']}</span>
                <span class="ip">IP: {req['ip']}</span>
            </div>
            <div class="request-header">
                <span><strong>Method:</strong> {req['method']}</span>
                <span><strong>URL:</strong> {req['url']}</span>
            </div>
            <div class="request-data">
                <strong>Request Data:</strong>
                <pre>{json.dumps(req['data'], indent=2, ensure_ascii=False)}</pre>
            </div>
        </div>
            '''
    
    html += '''
    </body>
    </html>
    '''
    return html

if __name__ == '__main__':
    print("Starting server on http://127.0.0.1:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)

