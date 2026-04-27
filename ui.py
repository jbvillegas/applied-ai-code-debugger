from flask import Flask, render_template_string, request, jsonify
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from src.agent import DebugAgent
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

HTML = '''

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>AI Code Debugger</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: 'Inter', Arial, sans-serif;
            background: #f8fafc;
            margin: 0;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            background: #fff;
            border-radius: 12px;
            box-shadow: 0 2px 16px rgba(0,0,0,0.07);
            padding: 32px 24px 24px 24px;
            max-width: 480px;
            width: 100%;
        }
        h2 {
            margin-top: 0;
            font-weight: 600;
            letter-spacing: -1px;
            color: #22223b;
            text-align: center;
        }
        label {
            font-size: 1rem;
            color: #4a4e69;
        }
        textarea {
            width: 100%;
            height: 140px;
            font-family: monospace;
            font-size: 1rem;
            border: 1px solid #e0e1dd;
            border-radius: 6px;
            padding: 10px;
            margin-top: 8px;
            margin-bottom: 18px;
            background: #f4f4f4;
            resize: vertical;
            transition: border 0.2s;
        }
        textarea:focus {
            border: 1.5px solid #4a4e69;
            outline: none;
        }
        button {
            background: #4a4e69;
            color: #fff;
            border: none;
            border-radius: 6px;
            padding: 10px 24px;
            font-size: 1rem;
            font-weight: 500;
            cursor: pointer;
            transition: background 0.2s;
            width: 100%;
        }
        button:hover {
            background: #22223b;
        }
        .result {
            margin-top: 24px;
            background: #f4f4f4;
            border-radius: 6px;
            padding: 16px;
            font-size: 0.98rem;
            color: #22223b;
            word-break: break-word;
            display: none;
        }
        .result.visible {
            display: block;
        }
        .spinner {
            display: flex;
            align-items: center;
            justify-content: center;
            margin-top: 18px;
        }
        .lds-dual-ring {
            display: inline-block;
            width: 32px;
            height: 32px;
        }
        .lds-dual-ring:after {
            content: " ";
            display: block;
            width: 24px;
            height: 24px;
            margin: 4px;
            border-radius: 50%;
            border: 4px solid #4a4e69;
            border-color: #4a4e69 transparent #4a4e69 transparent;
            animation: lds-dual-ring 1.2s linear infinite;
        }
        @keyframes lds-dual-ring {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        @media (max-width: 600px) {
            .container { padding: 18px 4vw; }
            h2 { font-size: 1.3rem; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>AI Code Debugger</h2>
        <form id="debug-form">
            <label for="code">Paste your Python code:</label>
            <textarea id="code" name="code" required placeholder="e.g. def foo(x):\n    return x[0]\nfoo([])"></textarea>
            <button type="submit">Debug</button>
        </form>
        <div class="spinner" id="spinner" style="display:none;">
            <div class="lds-dual-ring"></div>
        </div>
        <div class="result" id="result"></div>
    </div>
    <script>
        const form = document.getElementById('debug-form');
        const resultDiv = document.getElementById('result');
        const spinner = document.getElementById('spinner');
        form.onsubmit = async function(e) {
            e.preventDefault();
            const code = document.getElementById('code').value;
            resultDiv.classList.remove('visible');
            resultDiv.innerHTML = '';
            spinner.style.display = 'flex';
            try {
                const res = await fetch('/debug', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ code })
                });
                if (!res.ok) throw new Error('Network error');
                const data = await res.json();
                let html = `<b>Final Output:</b><pre>${data.final_code}</pre>` +
                    `<b>Success:</b> ${data.success} | <b>Attempts:</b> ${data.attempts} | <b>Confidence:</b> ${data.confidence}<br>`;
                if (data.error) html += `<b>Error:</b> <pre>${data.error}</pre>`;
                resultDiv.innerHTML = html;
                resultDiv.classList.add('visible');
            } catch (err) {
                resultDiv.innerHTML = `<b>Error:</b> <pre>${err.message}</pre>`;
                resultDiv.classList.add('visible');
            } finally {
                spinner.style.display = 'none';
            }
        };
    </script>
</body>
</html>
'''

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/debug", methods=["POST"])
def debug():
    code = request.json.get("code", "")
    agent = DebugAgent()
    result = agent.run(code)
    # Return more detailed error info for debugging
    return jsonify({
        "final_code": result.get("final_code", ""),
        "success": result.get("success", False),
        "attempts": result.get("attempts", 0),
        "confidence": result.get("confidence", 0.0),
        "error": result.get("error", ""),
        "log": result.get("log", []),
        "metrics": result.get("metrics", {}),
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
