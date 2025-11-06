#!/usr/bin/env python3
"""
Simple web GUI for the VM using only Python standard library.
Run: python3 vm_web.py
Open in your browser: http://localhost:8000/

This avoids Tkinter/X11 and works in headless/container environments.
"""

import json
import threading
import time
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
from io import BytesIO
import cgi
import tempfile
import os

from VmPython import SimpleVM
import ByteCodeReader

HOST = '0.0.0.0'
PORT = 8000

vm = SimpleVM()
bytecode = []
vm_lock = threading.Lock()
run_flag = threading.Event()

HTML = b'''<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <title>Simple VM Web GUI</title>
    <style>
        body { font-family: sans-serif; margin: 16px }
        .col { float:left; margin-right: 20px }
        pre { background: #f7f7f7; padding: 10px }
        button { margin: 4px }
        .clear { clear: both }
    </style>
</head>
<body>
    <h2>Simple VM Web GUI</h2>
    <div class="col">
        <div>
            <button onclick="doAction('load')">Load ByteCode.txt</button>
            <button onclick="doAction('reset')">Reset</button>
        </div>
        <div style="margin-top:8px">Status: <span id="status">idle</span></div>
        <div>
            <button onclick="doAction('step')">Step</button>
            <button onclick="doAction('run')">Run</button>
            <button onclick="doAction('stop')">Stop</button>
        </div>
        <h3>Program Counter / Instruction</h3>
        <div id="pc">pc: -</div>
        <h3>Stack</h3>
        <pre id="stack">[]</pre>
        <h3>Memory</h3>
        <pre id="memory">{}</pre>
        <h3>Console</h3>
        <pre id="console"></pre>
    </div>
    <div class="col">
            <h3>Bytecode</h3>
            <pre id="bytecode"></pre>
            <h3>Paste bytecode text</h3>
            <textarea id="bytebox" rows="12" cols="40" placeholder="PUSH\n5\nPRINT\n"></textarea>
            <div>
                <button onclick="loadText()">Load from text</button>
            </div>
    </div>
    <div class="clear"></div>

<script>
let runState = false;
async function doAction(act) {
    const res = await fetch('/' + act, { method: 'POST' });
    const txt = await res.text();
    // append to console if present
    if (txt) {
        const c = document.getElementById('console');
        c.textContent += txt + '\n';
        c.scrollTop = c.scrollHeight;
    }
    setStatus(txt || act + ' OK');
}

async function loadText() {
    const txtarea = document.getElementById('bytebox');
    const text = txtarea.value;
    if (!text) { alert('Paste some bytecode into the box first'); return; }
    const res = await fetch('/load_text', { method: 'POST', body: text });
    const txt = await res.text();
    if (txt) {
        const c = document.getElementById('console');
        c.textContent += txt + '\n';
        c.scrollTop = c.scrollHeight;
    }
    setStatus(txt || 'loaded');
}

function setStatus(s) {
    const st = document.getElementById('status');
    if (!st) return;
    st.textContent = s;
    // briefly highlight
    st.style.transition = 'none';
    st.style.background = '#ffd';
    setTimeout(()=>{ st.style.transition='background 0.6s'; st.style.background='transparent'; }, 50);
}

// Real-time updates via Server-Sent Events
if (typeof EventSource !== 'undefined') {
    const es = new EventSource('/stream');
    es.onmessage = function(e) {
        try {
            const j = JSON.parse(e.data);
            document.getElementById('pc').textContent = 'pc: ' + j.program_counter + (j.halted ? ' (halted)' : '');
            document.getElementById('stack').textContent = JSON.stringify(j.stack, null, 2);
            document.getElementById('memory').textContent = JSON.stringify(j.memory, null, 2);
            document.getElementById('bytecode').textContent = JSON.stringify(j.bytecode, null, 2);
            if (j.console_lines && j.console_lines.length) {
                const c = document.getElementById('console');
                for (const line of j.console_lines) c.textContent += line + '\n';
                c.scrollTop = c.scrollHeight;
            }
        } catch(err) {
            console.error('SSE parse error', err);
        }
    };
    es.onerror = function() { /* ignore, SSE will reconnect in browsers */ };
} else {
    // fallback polling
    setInterval(update, 500);
}

async function update() {
    const res = await fetch('/state');
    if (!res.ok) return;
    const j = await res.json();
    document.getElementById('pc').textContent = 'pc: ' + j.program_counter + (j.halted ? ' (halted)' : '');
    document.getElementById('stack').textContent = JSON.stringify(j.stack, null, 2);
    document.getElementById('memory').textContent = JSON.stringify(j.memory, null, 2);
    document.getElementById('bytecode').textContent = JSON.stringify(j.bytecode, null, 2);
    if (j.console_lines && j.console_lines.length) {
        const c = document.getElementById('console');
        for (const line of j.console_lines) c.textContent += line + '\n';
        c.scrollTop = c.scrollHeight;
    }
}

setInterval(update, 500);
window.onload = update;
</script>
</body>
</html>
'''


class VMHandler(BaseHTTPRequestHandler):
    def _set_json(self):
        self.send_header('Content-Type', 'application/json')

    def do_GET(self):
        if self.path == '/' or self.path.startswith('/index'):
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(HTML)))
            self.end_headers()
            self.wfile.write(HTML)
            return

        if self.path == '/state':
            with vm_lock:
                state = {
                    'program_counter': vm.program_counter,
                    'stack': vm.stack.copy(),
                    'memory': vm.memory.copy(),
                    'bytecode': bytecode.copy(),
                    'halted': vm.halted,
                    'console_lines': ConsoleBuffer.get_and_clear(),
                }
            self.send_response(200)
            self._set_json()
            self.end_headers()
            self.wfile.write(json.dumps(state).encode('utf-8'))
            return

        if self.path == '/stream':
            # Server-Sent Events endpoint: stream JSON state updates
            self.send_response(200)
            self.send_header('Content-Type', 'text/event-stream')
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('Connection', 'keep-alive')
            self.end_headers()
            try:
                while True:
                    with vm_lock:
                        state = {
                            'program_counter': vm.program_counter,
                            'stack': vm.stack.copy(),
                            'memory': vm.memory.copy(),
                            'bytecode': bytecode.copy(),
                            'halted': vm.halted,
                            'console_lines': ConsoleBuffer.get_and_clear(),
                        }
                    payload = json.dumps(state)
                    msg = f"data: {payload}\n\n".encode('utf-8')
                    try:
                        self.wfile.write(msg)
                        self.wfile.flush()
                    except BrokenPipeError:
                        break
                    except ConnectionResetError:
                        break
                    time.sleep(0.1)
            except Exception:
                pass
            return

        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        global bytecode
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length) if length else b''

        if self.path == '/step':
            with vm_lock:
                try:
                    cont = vm.step(bytecode, output_callback=ConsoleBuffer.append)
                    msg = 'Stepped'
                except Exception as e:
                    msg = f'Error: {e}'
            body = msg.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        if self.path == '/run':
            if not run_flag.is_set():
                run_flag.set()
                threading.Thread(target=run_thread, daemon=True).start()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'')
            return

        if self.path == '/stop':
            run_flag.clear()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'')
            return

        if self.path == '/reset':
            with vm_lock:
                vm.reset()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Reset')
            return

        if self.path == '/load':
            # optional: parse filename from body
            fn = 'ByteCode.txt'
            if body:
                try:
                    params = parse_qs(body.decode('utf-8'))
                    if 'file' in params:
                        fn = params['file'][0]
                except Exception:
                    pass
            with vm_lock:
                bytecode = ByteCodeReader.read_text_file_to_list(fn)
                vm.reset()
            body = f'Loaded {fn}'.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        if self.path == '/upload':
            # handle multipart form upload
            try:
                fs = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={
                    'REQUEST_METHOD': 'POST',
                    'CONTENT_TYPE': self.headers.get('Content-Type')
                })
                if 'file' not in fs:
                    raise ValueError('no file field')
                fileitem = fs['file']
                if not fileitem.file:
                    raise ValueError('empty file')
                # save to temporary file
                with tempfile.NamedTemporaryFile(delete=False, prefix='vm_upload_', dir='.') as tf:
                    data = fileitem.file.read()
                    tf.write(data)
                    tmpname = tf.name
                try:
                    with vm_lock:
                        bytecode = ByteCodeReader.read_text_file_to_list(tmpname)
                        vm.reset()
                    body = f'Uploaded and loaded {os.path.basename(tmpname)}'.encode('utf-8')
                finally:
                    # remove the temporary file after loading
                    try:
                        os.unlink(tmpname)
                    except Exception:
                        pass
            except Exception as e:
                body = f'Upload error: {e}'.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        if self.path == '/load_text':
            # body is raw text containing the bytecode lines
            try:
                if not body:
                    raise ValueError('empty request body')
                # Save text to a temporary file and load using ByteCodeReader
                with tempfile.NamedTemporaryFile(delete=False, prefix='vm_text_', dir='.') as tf:
                    if isinstance(body, bytes):
                        tf.write(body)
                    else:
                        tf.write(body.encode('utf-8'))
                    tmpname = tf.name
                try:
                    with vm_lock:
                        bytecode = ByteCodeReader.read_text_file_to_list(tmpname)
                        vm.reset()
                    body = f'Loaded text into {os.path.basename(tmpname)}'.encode('utf-8')
                finally:
                    # remove temp file after loading
                    try:
                        os.unlink(tmpname)
                    except Exception:
                        pass
            except Exception as e:
                body = f'Load text error: {e}'.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        self.send_response(404)
        self.end_headers()


class ConsoleBuffer:
    _lock = threading.Lock()
    _lines = []

    @classmethod
    def append(cls, s):
        with cls._lock:
            cls._lines.append(str(s))

    @classmethod
    def get_and_clear(cls):
        with cls._lock:
            lines = cls._lines.copy()
            cls._lines.clear()
            return lines


def run_thread():
    # Run VM until stopped or halted
    try:
        while run_flag.is_set():
            with vm_lock:
                if vm.halted or vm.program_counter >= len(bytecode):
                    run_flag.clear()
                    break
                vm.step(bytecode, output_callback=ConsoleBuffer.append)
            time.sleep(0.05)
    except Exception as e:
        ConsoleBuffer.append(f'Run error: {e}')
        run_flag.clear()


def main():
    # cleanup leftover temp files from previous runs
    try:
        for fname in os.listdir('.'):
            if fname.startswith('vm_text_') or fname.startswith('vm_upload_'):
                try:
                    os.unlink(fname)
                except Exception:
                    pass
    except Exception:
        pass

    server = ThreadingHTTPServer((HOST, PORT), VMHandler)
    print(f'Web GUI available at http://{HOST}:{PORT}/')
    print('Load ByteCode.txt with the Load button. Use Step/Run/Stop to control the VM.')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('Shutting down')
        server.shutdown()


if __name__ == '__main__':
    main()