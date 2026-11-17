const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

const edgePath = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const userDataDir = 'J:\\Desktop\\online-exam-system\\demo-evidence\\edge-cdp-profile';

async function main() {
  if (!fs.existsSync(userDataDir)) fs.mkdirSync(userDataDir, { recursive: true });

  console.log('Spawning Edge with remote debugging port 9222...');
  const edge = spawn(edgePath, [
    '--remote-debugging-port=9222',
    '--user-data-dir=' + userDataDir,
    '--headless=new',
    '--disable-gpu',
    '--no-first-run',
    'about:blank'
  ]);

  // Wait 2 seconds for port to open
  await new Promise(r => setTimeout(r, 2000));

  try {
    const versionData = await new Promise((resolve, reject) => {
      http.get('http://127.0.0.1:9222/json/version', res => {
        let buf = '';
        res.on('data', d => buf += d);
        res.on('end', () => resolve(JSON.parse(buf)));
      }).on('error', reject);
    });

    console.log('CDP Connected! Browser:', versionData.Browser);
    console.log('WebSocket Debugger URL:', versionData.webSocketDebuggerUrl);

    // Create a new tab using PUT
    const tabData = await new Promise((resolve, reject) => {
      const req = http.request({
        host: '127.0.0.1',
        port: 9222,
        path: '/json/new?http://127.0.0.1:8000/login/',
        method: 'PUT'
      }, res => {
        let buf = '';
        res.on('data', d => buf += d);
        res.on('end', () => resolve(JSON.parse(buf)));
      });
      req.on('error', reject);
      req.end();
    });

    console.log('New tab opened:', tabData.url);
    console.log('Tab WS URL:', tabData.webSocketDebuggerUrl);

    // Connect WebSocket
    const ws = new WebSocket(tabData.webSocketDebuggerUrl);
    let msgId = 1;
    const callbacks = new Map();

    ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      if (msg.id && callbacks.has(msg.id)) {
        callbacks.get(msg.id)(msg);
        callbacks.delete(msg.id);
      }
    };

    function send(method, params = {}) {
      return new Promise((resolve) => {
        const id = msgId++;
        callbacks.set(id, resolve);
        ws.send(JSON.stringify({ id, method, params }));
      });
    }

    await new Promise(r => ws.onopen = r);
    console.log('WebSocket connection established.');

    await send('Page.enable');
    await send('Runtime.enable');
    await new Promise(r => setTimeout(r, 1500));

    // Capture screenshot of login page
    const snap = await send('Page.captureScreenshot', { format: 'png' });
    console.log('Capture screenshot response:', Object.keys(snap), snap.error || 'no error');
    if (snap.result && snap.result.data) {
      const buffer = Buffer.from(snap.result.data, 'base64');
      fs.writeFileSync('J:\\Desktop\\online-exam-system\\demo-evidence\\02_login_page.png', buffer);
      console.log('Screenshot 02_login_page.png saved! Size:', buffer.length);
    }

    ws.close();
  } catch (err) {
    console.error('CDP Error:', err);
  } finally {
    edge.kill();
    console.log('Edge process stopped.');
  }
}

main();
