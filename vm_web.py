#!/usr/bin/env python3
"""
Simple web GUI for the VM using only Python standard library.
Run: python3 vm_web.py
Open in your browser: http://localhost:8000/

This avoids Tkinter/X11 and works in headless/container environments.
"""

import json
HTML = b'''<!doctype html>
<html>
#!/usr/bin/env python3
"""
Minimal web GUI for the VM: shows Stack and Memory and accepts pasted commands.
Run: python3 vm_web.py
Open: http://localhost:8000/
"""

import json
import threading
import time
import os
import tempfile
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

from VmPython import SimpleVM
import ByteCodeReader

HOST = '0.0.0.0'
PORT = 8000

vm = SimpleVM()
bytecode = []
vm_lock = threading.Lock()
run_flag = threading.Event()

HTML = """<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    #!/usr/bin/env python3
    """
    Minimal web GUI for the VM: shows Stack and Memory and accepts pasted commands.
    Run: python3 vm_web.py
    Open: http://localhost:8000/
    """

    import json
    import threading
    import time
    import os
    import tempfile
    from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
    from urllib.parse import parse_qs

    from VmPython import SimpleVM
    import ByteCodeReader

    HOST = '0.0.0.0'
    PORT = 8000

    vm = SimpleVM()
    bytecode = []
    vm_lock = threading.Lock()
    run_flag = threading.Event()

    HTML = """<!doctype html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>VM Stack/Memory</title>
        <style>
            body { font-family: sans-serif; margin: 12px }
            textarea { width: 100%; box-sizing: border-box }
            pre { background: #f7f7f7; padding: 8px; white-space: pre-wrap }
            .row { display:flex; gap:12px }
            .col { flex:1 }
            button { margin-top:8px }
        </style>
    </head>
    <body>
        <h3>VM Live View</h3>
        <div class="row">
            <div class="col">
                <h4>Stack</h4>
                <pre id="stack">[]</pre>
            </div>
            <div class="col">
                <h4>Memory</h4>
                <pre id="memory">{}</pre>
            </div>
        </div>

        <h4>Commands (one per line)</h4>
        <textarea id="bytebox" rows="10" placeholder="PUSH\n5\nPRINT\n"></textarea>
        <div>
            <button onclick="loadText()">Load & Reset</button>
            <button onclick="doAction('step')">Step</button>
            <button onclick="doAction('run')">Run</button>
            <button onclick="doAction('stop')">Stop</button>
            <span style="margin-left:12px">Status: <strong id="status">idle</strong></span>
        </div>

    <script>
    async function doAction(act) {
        const res = await fetch('/' + act, { method: 'POST' });
        const txt = await res.text();
        setStatus(txt || act + ' OK');
    }

    async function loadText() {
        const text = document.getElementById('bytebox').value;
        if (!text) return setStatus('no text');
        const res = await fetch('/load_text', { method: 'POST', body: text });
        const txt = await res.text();
        setStatus(txt || 'loaded');
    }

    function setStatus(s) {
        const el = document.getElementById('status');
        if (!el) return;
        el.textContent = s;
    }

    // SSE updates for stack/memory
    if (typeof EventSource !== 'undefined') {
        const es = new EventSource('/stream');
        es.onmessage = function(e) {
            try {
                const j = JSON.parse(e.data);
                document.getElementById('stack').textContent = JSON.stringify(j.stack, null, 2);
                document.getElementById('memory').textContent = JSON.stringify(j.memory, null, 2);
                if (j.console_lines && j.console_lines.length) setStatus(j.console_lines.slice(-1)[0]);
            } catch (err) { console.error(err); }
        };
    }
    </script>
    </body>
    </html>
    """
            cls._lines.clear()
            return lines


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

        if self.path == '/load_text':
            try:
                if not body:
                    raise ValueError('empty request body')
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


def run_thread():
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