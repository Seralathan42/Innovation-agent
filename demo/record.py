"""Film the demo of the Knowledge Hub (script: docs/demo-script.md) and edit it into an MP4.

It drives a hidden Chrome window through the running terminal (http://127.0.0.1:8001), records every frame the page
draws, adds a smooth pointer, zooms, captions and title cards inside the page, then cuts out the waiting and joins
the scenes with ffmpeg, adding the soundtrack from sound.py. Start the terminal first, and finish the demo brief, its profiles and the paper analysis.

    .venv/bin/python demo/record.py                  # films every scene and writes demo/knowledge-hub-demo.mp4
    .venv/bin/python demo/record.py research sector  # films only these scenes again, then joins all the clips
"""

import base64
import json
import os
import re
import shutil
import socket
import struct
import subprocess
import sys
import tempfile
import threading
import time
import urllib.request
from pathlib import Path

import sound

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
APP = "http://127.0.0.1:8001"
W, H, FPS = 1920, 1080, 30
CLIPS = Path(__file__).parent / "clips"  # one clip per scene, joined by sound.py
BRIEF = "demo-sleep-radar"  # the brief shown, by its disclosure file name
SPEEDUP = 30  # its real run is replayed this many times faster in the upload scene
PAPER = "b7faa01e-fc95-479e-b8f8-8f5f4606f0bd"  # the analysed Aalto paper shown in Past research (lithium recovery, 2018)
PAPER_SEARCH = "lithium recovery"


class CDP:
    """A minimal Chrome DevTools client over a WebSocket, using only the standard library."""

    def __init__(self, url):
        host, rest = url.removeprefix("ws://").split("/", 1)
        name, port = host.split(":")
        self.sock = socket.create_connection((name, int(port)))
        key = base64.b64encode(os.urandom(16)).decode()
        self.sock.sendall(f"GET /{rest} HTTP/1.1\r\nHost: {host}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n"
                          f"Sec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n".encode())
        head = b""
        while not head.endswith(b"\r\n\r\n"):
            head += self.sock.recv(1)
        self.lock, self.cond, self.replies, self.handlers, self.last = threading.Lock(), threading.Condition(), {}, {}, 0
        threading.Thread(target=self._read, daemon=True).start()

    def _exact(self, n):
        data = bytearray()
        while len(data) < n:
            chunk = self.sock.recv(min(n - len(data), 1 << 20))
            if not chunk:
                raise ConnectionError("Chrome closed the connection")
            data += chunk
        return bytes(data)

    def _frame(self):
        b1, b2 = self._exact(2)
        n = b2 & 0x7F
        n = struct.unpack(">H", self._exact(2))[0] if n == 126 else struct.unpack(">Q", self._exact(8))[0] if n == 127 else n
        return b1 & 0x80, b1 & 0x0F, self._exact(n)

    def _read(self):
        while True:
            try:
                fin, op, data = self._frame()
            except (ConnectionError, OSError):
                return  # Chrome closed at the end of the recording
            while not fin:
                fin, _, more = self._frame()
                data += more
            if op == 8:
                return
            if op == 1:
                message = json.loads(data)
                if "id" in message:
                    with self.cond:
                        self.replies[message["id"]] = message
                        self.cond.notify_all()
                elif message.get("method") in self.handlers:
                    self.handlers[message["method"]](message["params"])

    def send(self, method, params=None, wait=True):
        with self.lock:
            self.last += 1
            number = self.last
            payload = json.dumps({"id": number, "method": method, "params": params or {}}).encode()
            mask = os.urandom(4)
            n = len(payload)
            head = bytes([0x81]) + (bytes([0x80 | n]) if n < 126 else bytes([0x80 | 126]) + struct.pack(">H", n) if n < 65536
                                    else bytes([0x80 | 127]) + struct.pack(">Q", n))
            self.sock.sendall(head + mask + bytes(b ^ mask[i % 4] for i, b in enumerate(payload)))
        if not wait:
            return None
        with self.cond:
            self.cond.wait_for(lambda: number in self.replies, timeout=120)
            reply = self.replies.pop(number)
        if "error" in reply:
            raise RuntimeError(f"{method}: {reply['error']}")
        return reply.get("result", {})



# Pointer, zoom, spotlight, captions, cards and the brief's run replayed, added to the page. The zoom moves the whole app (.app) like a
# camera; the spotlight dims everything but one element. The news bar is frozen so it matches across scenes.
STAGE = """
(() => {
  if (window.demo) return;
  const css = document.createElement('style');
  css.textContent = `
    .app { transform-origin: 0 0; transition: transform 1.4s cubic-bezier(.65,0,.35,1); will-change: transform; }
    #d-cursor { position: fixed; left: 0; top: 0; z-index: 99999; pointer-events: none; transition: transform 1.05s cubic-bezier(.45,0,.25,1); }
    #d-cursor svg { filter: drop-shadow(0 2px 4px rgba(0,0,0,.35)); }
    .d-ripple { position: fixed; z-index: 99998; width: 46px; height: 46px; margin: -23px 0 0 -23px; border-radius: 50%;
      border: 3px solid #ffcd00; pointer-events: none; animation: d-ripple .7s ease-out forwards; }
    @keyframes d-ripple { from { transform: scale(.2); opacity: 1; } to { transform: scale(1.6); opacity: 0; } }
    #d-spot { position: fixed; z-index: 99990; pointer-events: none; border-radius: 12px; opacity: 0;
      box-shadow: 0 0 0 4px #ffcd00, 0 0 0 300vmax rgba(12,12,12,.52);
      transition: opacity .45s ease; }
    #d-caption { position: fixed; left: 50%; bottom: 46px; z-index: 99997; transform: translate(-50%, 30px); opacity: 0; pointer-events: none;
      padding: 16px 30px; background: #111; color: #fff; font: 700 30px/1.2 Inter, system-ui, sans-serif; letter-spacing: -.01em;
      border-left: 8px solid #ffcd00; box-shadow: 0 12px 40px rgba(0,0,0,.25); transition: all .45s cubic-bezier(.2,.8,.2,1); white-space: nowrap; }
    #d-caption.on { transform: translate(-50%, 0); opacity: 1; }
    #d-card { position: fixed; inset: 0; z-index: 100000; display: grid; place-content: center; text-align: center;
      font-family: Inter, system-ui, sans-serif; opacity: 0; pointer-events: none; transition: opacity .7s ease; }
    #d-card { background: #111; color: #fff; }
    #d-card.on { opacity: 1; }
    #d-card > * { animation: d-in .7s cubic-bezier(.2,.8,.2,1) both; }
    @keyframes d-in { from { opacity: 0; transform: translateY(18px); } }
    #d-card .stats { display: grid; grid-template-columns: repeat(4, 370px); gap: 40px; text-align: left; transition: opacity .4s; }
    #d-card .stats.out { opacity: 0; }
    #d-card .stat { padding-top: 20px; border-top: 4px solid #ffcd00; opacity: 0; transform: translateY(30px); transition: all .6s cubic-bezier(.2,.8,.2,1); }
    #d-card .stat.on { opacity: 1; transform: none; }
    #d-card .stat b { display: block; font-size: 80px; letter-spacing: -.04em; line-height: 1; font-variant-numeric: tabular-nums; }
    #d-card .stat span { display: block; margin-top: 14px; font-size: 26px; color: #bdbdbd; line-height: 1.3; }
    #d-card h1 { margin: 0; font-size: 96px; letter-spacing: -.04em; line-height: 1; }
    #d-card h1 span { color: #ffcd00; }
    #d-card p { margin: 26px 0 0; font-size: 34px; color: #bdbdbd; letter-spacing: -.01em; }
    #d-card .hub { display: inline-block; margin-top: 18px; padding: 6px 14px; border: 2px solid #ffcd00; color: #ffcd00; font-weight: 700;
      font-size: 22px; letter-spacing: .14em; }
    #d-file { position: fixed; z-index: 99996; left: 0; top: 0; display: flex; gap: 14px; align-items: center; padding: 16px 22px; background: #fff;
      border: 2px solid #111; box-shadow: 0 18px 40px rgba(0,0,0,.25); font: 700 20px Inter, system-ui, sans-serif; opacity: 0;
      transition: transform 1.05s cubic-bezier(.45,0,.25,1), opacity .4s; pointer-events: none; }
    #d-file b { display: grid; place-items: center; width: 42px; height: 52px; background: #ffcd00; font-size: 13px; }`;
  document.head.append(css);
  document.body.insertAdjacentHTML('beforeend', `
    <div id="d-cursor"><svg width="30" height="34" viewBox="0 0 30 34"><path d="M3 2 L3 27 L10 20.5 L14.5 31 L19 29 L14.6 18.8 L24 18.8 Z"
      fill="#111" stroke="#fff" stroke-width="2.2" stroke-linejoin="round"/></svg></div>
    <div id="d-spot"></div><div id="d-caption"></div><div id="d-card"></div>
    <div id="d-file"><b>MD</b><span>demo-sleep-radar.md</span></div>`);
  state.news = 0; renderBreaking(); window.renderBreaking = () => {};
  const app = document.querySelector('.app'), $$ = (sel) => document.querySelector(sel);
  let zoom = { s: 1, x: 0, y: 0 };
  const plain = (r) => ({ x: (r.left - zoom.x) / zoom.s, y: (r.top - zoom.y) / zoom.s, w: r.width / zoom.s, h: r.height / zoom.s });
  window.demo = {
    events: [],  // [time, kind] of what the soundtrack follows: clicks, highlights, zooms, cards and finished agents
    log(kind) { this.events.push([Date.now() / 1000, kind]); },
    pos: { x: innerWidth * .62, y: innerHeight * .55 },
    point(x, y) { this.pos = { x, y }; $$('#d-cursor').style.transform = `translate(${x - 3}px, ${y - 2}px)`; },
    place(x, y) { const c = $$('#d-cursor'); c.style.transition = 'none'; this.point(x, y); c.offsetWidth; c.style.transition = ''; },
    centre(sel) { const el = $$(sel); if (!el) return null; const r = el.getBoundingClientRect();
      return { x: r.left + Math.min(r.width / 2, 60 + r.width * .1), y: r.top + r.height / 2 }; },
    ripple() { this.log('click'); const d = document.createElement('div'); d.className = 'd-ripple'; d.style.left = this.pos.x + 'px'; d.style.top = this.pos.y + 'px';
      document.body.append(d); setTimeout(() => d.remove(), 800); },
    zoom(sel, s) {
      if (!sel || s === 1) { zoom = { s: 1, x: 0, y: 0 }; }
      else { this.log('zoom'); const r = plain($$(sel).getBoundingClientRect()); const cx = r.x + r.w / 2, cy = r.y + r.h / 2;
        zoom = { s, x: Math.min(0, Math.max(innerWidth - innerWidth * s, innerWidth / 2 - cx * s)), y: Math.min(0, Math.max(innerHeight - innerHeight * s, innerHeight / 2 - cy * s)) }; }
      app.style.transform = `translate(${zoom.x}px, ${zoom.y}px) scale(${zoom.s})`;
    },
    spot(sel, pad = 12) {  // appears where it belongs: a visible spotlight fades out first instead of sliding across
      const s = $$('#d-spot'); clearTimeout(this.spotTimer);
      if (!sel) { s.style.opacity = 0; return; }
      const show = () => { this.log('spot'); const r = $$(sel).getBoundingClientRect();
        Object.assign(s.style, { left: r.left - pad + 'px', top: r.top - pad + 'px', width: r.width + 2 * pad + 'px', height: r.height + 2 * pad + 'px', opacity: 1 }); };
      if (+getComputedStyle(s).opacity > 0) { s.style.opacity = 0; this.spotTimer = setTimeout(show, 450); } else show(); },
    stats(items) {  // the closing figures: they rise in one by one and count up
      this.card(`<div class="stats">${items.map(([n, label]) => `<div class="stat"><b>0</b><span>${label}</span></div>`).join('')}</div>`);
      document.querySelectorAll('#d-card .stat').forEach((el, i) => setTimeout(() => { el.classList.add('on'); this.log('pop'); const b = el.querySelector('b'), start = performance.now();
        const step = (now) => { const k = Math.min(1, (now - start) / 1100); b.textContent = Math.round(items[i][0] * (1 - (1 - k) ** 3)).toLocaleString('en-US');
          if (k < 1) requestAnimationFrame(step); }; requestAnimationFrame(step); }, 450 + i * 280)); },
    scroll(sel, offset = 20, smooth = true) { const main = $$('#main'), el = $$(sel);
      main.scrollTo({ top: main.scrollTop + el.getBoundingClientRect().top - main.getBoundingClientRect().top - offset, behavior: smooth ? 'smooth' : 'instant' }); },
    caption(text) { const c = $$('#d-caption'); if (text) { c.textContent = text; c.classList.add('on'); } else c.classList.remove('on'); },
    card(html) { const c = $$('#d-card'); if (html) { this.log('card'); c.innerHTML = html; c.classList.add('on'); } else c.classList.remove('on'); },
    replay(id, times, speed) {  // opens a finished brief as it filled in, speed times faster: times are each agent's [start, end] in seconds
      const start = Date.now(), url = `/api/briefs/${encodeURIComponent(id)}`, real = window.fetch;
      window.fetch = async (u, o) => { const r = await real(u, o); if (u !== url) return r;
        const b = await r.json(), t = (Date.now() - start) / 1000 * speed;
        for (const [a, [from, to]] of Object.entries(times)) if (t < to) {
          b.status[a] = t < from ? 'waiting' : 'running'; if (b.scores) delete b.scores[a]; delete b.reports[a]; if (a === 'check') b.check = null; }
        return new Response(JSON.stringify(b)); };
      Object.values(times).forEach(([, to]) => setTimeout(() => { this.log('done'); showBrief(); }, to / speed * 1000 + 30));
      openBrief(id); },
    file(x, y, show) { const f = $$('#d-file'); f.style.transform = `translate(${x}px, ${y}px)`; f.style.opacity = show ? 1 : 0; },
    go(tab) { state.tab = tab; state.profile = null; renderTabs(); renderMain(true); },
  };
  demo.place(demo.pos.x, demo.pos.y);
})()"""


class Film:
    def __init__(self, cdp, frames_dir):
        self.cdp, self.dir, self.frames, self.cuts, self.keys = cdp, frames_dir, [], [[time.time(), 1.0]], []
        cdp.handlers["Page.screencastFrame"] = self._frame

    def _frame(self, params):
        self.cdp.send("Page.screencastFrameAck", {"sessionId": params["sessionId"]}, wait=False)
        path = self.dir / f"{len(self.frames):06d}.jpg"
        path.write_bytes(base64.b64decode(params["data"]))
        self.frames.append((params["metadata"]["timestamp"], path))

    def speed(self, factor):
        """From now on, play at this speed (0 cuts the part out)."""
        self.cuts.append([time.time(), factor])

    def js(self, expression):
        result = self.cdp.send("Runtime.evaluate", {"expression": expression, "awaitPromise": True, "returnByValue": True})
        if "exceptionDetails" in result:
            raise RuntimeError(f"{expression[:80]}: {result['exceptionDetails'].get('exception', {}).get('description')}")
        return result["result"].get("value")

    def wait_for(self, condition, timeout=240):
        end = time.time() + timeout
        while not self.js(f"!!({condition})"):
            if time.time() > end:
                raise TimeoutError(condition)
            time.sleep(0.25)

    def load(self, condition, timeout=240):
        """Wait for data to load, cut out of the video: nothing moves meanwhile, so the cut does not show."""
        self.speed(0)
        self.wait_for(condition, timeout)
        time.sleep(0.15)
        self.speed(1)

    def move(self, selector, pause=1.1):
        spot = self.js(f"demo.centre({json.dumps(selector)})")
        if not spot:
            raise RuntimeError(f"Not on the page: {selector}")
        self.js(f"demo.point({spot['x']}, {spot['y']})")
        time.sleep(pause)
        return spot

    def click(self, selector, pause=1.1):
        spot = self.move(selector, pause)
        self.js("demo.ripple()")
        for kind in ("mousePressed", "mouseReleased"):
            self.cdp.send("Input.dispatchMouseEvent", {"type": kind, "x": spot["x"], "y": spot["y"], "button": "left", "clickCount": 1})
        time.sleep(0.4)

    def type(self, selector, text, per_char=0.05):
        self.click(selector, 0.9)
        for char in text:
            self.cdp.send("Input.insertText", {"text": char})
            self.keys.append([time.time(), "key"])
            time.sleep(per_char)

    def do(self, *steps):
        """Run page steps: (javascript, seconds to hold afterwards)."""
        for expression, hold in steps:
            self.js(expression)
            time.sleep(hold)


TITLE = '<h1>Aalto Innovation<span>.</span></h1><div><span class="hub">KNOWLEDGE HUB</span></div><p>{}</p>'
STATE = CLIPS / "state.json"  # what one scene leaves behind for the next: the chat, the company opened, the pointer


def remember(key, value):
    saved = json.loads(STATE.read_text()) if STATE.exists() else {}
    saved[key] = value
    STATE.write_text(json.dumps(saved, ensure_ascii=False))


def recall(key, default=None):
    return (json.loads(STATE.read_text()) if STATE.exists() else {}).get(key, default)


def brief_id():
    return next(b["id"] for b in json.load(urllib.request.urlopen(f"{APP}/api/briefs")) if BRIEF in b["id"])


def run_times():
    """When each agent of the demo brief started and finished, in seconds, from its run_info.txt. The checker starts
    when the last report is saved."""
    info = (Path(__file__).parent.parent / "outputs" / brief_id() / "run_info.txt").read_text()
    took = {a: int(s) for a, s in re.findall(r"^\[(\w+)\] saved .+\((\d+) s\)$", info, re.M)}
    check, last = took.pop("check"), max(took.values())
    return {**{a: [0, s] for a, s in took.items()}, "check": [last, last + check]}


# Each scene starts exactly where the one before it ended. after(name) rebuilds that end state on a fresh page (not
# filmed), so any scene can be filmed again on its own. The scenes follow docs/demo-script.md.

def after(f, name):
    if name in ("upload", "result", "assistant"):
        f.js(f"openBrief({json.dumps(brief_id())})")
        f.wait_for("document.querySelector('.score-card')")
        time.sleep(0.6)
    if name in ("result", "assistant"):
        f.js("state.briefPart = 'ip'; showBrief()")
        f.wait_for("document.querySelector('[data-part=\"ip\"].active')")
        time.sleep(0.6)
        f.js("demo.scroll('.report-head', 30, false)")
    if name in ("assistant", "similar", "patents", "research", "sector"):
        f.js(f"document.getElementById('messages').innerHTML = {json.dumps(recall('chat', ''))}; "
             f"document.getElementById('messages').scrollTop = {recall('chat-scroll', 1e9)}")
    if name == "assistant":
        f.js(f"state.profile = {{ kind: 'company', name: {json.dumps(recall('company', 'Sleepiz'))}, context: '' }}; renderProfile()")
        f.wait_for("document.querySelector('.profile .people')")
        time.sleep(0.5)
        f.js("document.getElementById('main').scrollTop = 0")
    if name == "similar":
        f.js(f"demo.go('similar'); state.similarText = document.getElementById('sim-text').value = {json.dumps(SIMILAR_TEXT)}; "
             "document.getElementById('sim-go').click()")
        f.wait_for("document.querySelector('#sim-results h2')")
        time.sleep(0.5)
        f.js("demo.scroll('#sim-results', 10, false)")
    if name == "patents":
        f.js("demo.go('patents')")
        f.wait_for("document.querySelector('.pf-val input[data-f=\"sector\"][data-v=\"HLTH\"]')", 120)
        f.js("demo.scroll('.pf', 10, false); document.querySelector('.pf-val input[data-f=\"sector\"][data-v=\"HLTH\"]').click()")
        time.sleep(1.0)
        f.js("document.querySelector('.pf-actions [data-act=\"refine\"][data-f=\"sector\"]').click()")
        f.wait_for("document.querySelector('.chip-f')")
        f.js("state.filters.patents.sort = 'applicants:asc'; document.getElementById('pf-sort').value = 'column'; applyFilters()")
        f.wait_for("document.querySelector('th.sorted')")
        time.sleep(1.0)
    if name == "research":
        f.js(f"demo.go('research')")
        f.wait_for("document.querySelector('#pf-results tr[data-paper]')", 60)
        f.js(f"const q = document.getElementById('pf-q'); q.value = {json.dumps(PAPER_SEARCH)}; q.dispatchEvent(new Event('input'))")
        f.wait_for(f"document.querySelector('#pf-results tr[data-paper=\"{PAPER}\"]')", 60)
        f.js(f"openPaper('{PAPER}')")
        f.wait_for("document.querySelector('.paper .glance')")
        time.sleep(1.5)
    if name == "sector":
        f.js("openSector('health-tech')")
        f.wait_for("document.querySelector('.grid .panel:nth-child(3)')")
        time.sleep(0.6)
        f.js("demo.scroll('.grid .panel:nth-child(3)', 20, false)")
    point = recall(f"cursor-{name}")
    if point:
        f.js(f"demo.place({point['x']}, {point['y']})")
    time.sleep(0.6)


SIMILAR_TEXT = "Contactless radar for sleep apnea screening"


def title(f):
    f.do(("1", 1.6), ("demo.card(null)", 0.9))


def upload(f):
    f.do(("demo.caption('Drop in an invention disclosure')", 0.5),
         ("demo.file(innerWidth * .58, innerHeight * .72, true); demo.point(innerWidth * .58 + 150, innerHeight * .72 + 40)", 0.7))
    drop = f.js("(() => { const r = document.getElementById('drop').getBoundingClientRect(); return { x: r.left + r.width / 2, y: r.top + r.height / 2 }; })()")
    f.do((f"demo.file({drop['x'] - 140}, {drop['y'] - 40}, true); demo.point({drop['x'] + 10}, {drop['y'] + 2})", 1.2),
         ("demo.log('drop'); document.getElementById('drop').classList.add('over')", 0.5),
         (f"demo.file({drop['x'] - 140}, {drop['y'] - 40}, false); demo.caption(null)", 0.3))
    times = run_times()
    minutes = round(max(end for _, end in times.values()) / 60)
    f.do((f"demo.replay({json.dumps(brief_id())}, {json.dumps(times)}, {SPEEDUP})", 0.5),
         (f"demo.caption('{minutes} minutes of research, sped up')", 0.1))
    f.wait_for("document.querySelector('.verdict')")
    f.do(("1", 0.9), ("demo.caption(null)", 0.6))


def result(f):
    f.do(("demo.caption('Four AI agents research it at the same time')", 0.2),
         ("demo.zoom('.steps', 1.45)", 1.1),
         ("demo.spot('.steps > div:nth-child(2)')", 1.3),
         ("demo.caption('Each part is scored from 1 to 5')", 0.2),
         ("demo.spot('.steps > div:nth-child(4)')", 1.3),
         ("demo.spot(null); demo.scroll('.scores', 150)", 0.3),
         ("demo.caption('A second AI checks every score')", 0.2),
         ("demo.zoom('.score-card:nth-child(3)', 1.6)", 1.3),
         ("demo.spot('.score-card:nth-child(3)')", 0.2))
    f.move(".score-card:nth-child(3) .verdict", 1.4)
    f.do(("demo.spot(null); demo.zoom(null)", 1.2))
    f.click('[data-part="ip"]', 1.1)
    f.load("document.querySelector('[data-part=\"ip\"].active')")
    f.do(("demo.scroll('.report-head', 30)", 0.9), ("demo.caption(null)", 0.6))


def assistant(f):
    f.do(("demo.caption('Ask the assistant follow-up questions')", 0.3))
    f.type("#input", "Who already sells something similar?", 0.035)
    f.click("#send", 0.9)
    time.sleep(0.6)
    f.speed(28)  # the answer streams in, shown sped up
    f.wait_for("!state.busy", 300)
    f.speed(1)
    time.sleep(0.5)
    company = f.js("""(async () => {  // the first company named whose profile is already built, else the first one
      const links = [...document.querySelectorAll("#messages .msg.assistant:last-child a[href^='#company/']")];
      for (const a of links) { const name = decodeURIComponent(a.getAttribute('href').slice(9));
        if ((await (await fetch(`/api/profile?kind=company&name=${encodeURIComponent(name)}`)).json()).status === 'ready') { a.dataset.pick = 1; return name; } }
      if (links[0]) { links[0].dataset.pick = 1; return decodeURIComponent(links[0].getAttribute('href').slice(9)); }
      return null; })()""")
    if company:
        f.do(("demo.caption('One click opens a company profile')", 0.2),
             ("(() => { const m = document.getElementById('messages'), r = document.querySelector('[data-pick]').getBoundingClientRect(); "
              "m.scrollTo({ top: m.scrollTop + r.top - m.getBoundingClientRect().top - m.clientHeight / 2, behavior: 'smooth' }); })()", 0.8))
        f.click("[data-pick]", 1.1)
        time.sleep(0.3)
        if not f.js("!!state.profile"):
            f.js("document.querySelector('[data-pick]').click()")  # the click missed the link
        f.load("document.querySelector('.profile .people')", 300)  # a first click builds the profile
        f.do(("1", 0.3), ("demo.spot('.profile-top')", 2.4), ("demo.spot(null); demo.caption(null)", 0.6))
        remember("company", company)
    remember("chat", f.js("document.getElementById('messages').innerHTML"))
    remember("chat-scroll", f.js("document.getElementById('messages').scrollTop"))


def similar(f):
    f.click('#tabs [data-tab="similar"]', 1.1)
    f.do(("demo.caption('Find similar patents in our local patent database')", 0.3))
    f.type("#sim-text", SIMILAR_TEXT, 0.03)
    f.click("#sim-go", 0.9)
    f.load("document.querySelector('#sim-results .sim-stats')")
    f.do(("demo.scroll('#sim-results', 10)", 1.0), ("demo.spot('.sim-stats > div:first-child')", 1.3),
         ("demo.spot(null); demo.caption(null)", 0.5))


def patents(f):
    f.click('#tabs [data-tab="patents"]', 1.1)
    f.load("document.querySelector('.pf-val input[data-f=\"sector\"][data-v=\"HLTH\"]')", 120)
    f.do((f"demo.caption('Search through {COUNTS['patents'] // 10000 * 10000:,} patents')", 0.2), ("demo.scroll('.pf', 10)", 1.0))
    f.click('.pf-val input[data-f="sector"][data-v="HLTH"]', 1.0)
    f.click('.pf-actions [data-act="refine"][data-f="sector"]', 0.9)
    f.load("document.querySelector('.chip-f') && !document.getElementById('pf-side').classList.contains('counting')")
    f.do(("demo.spot('#pf-count', 8)", 1.2), ("demo.spot(null)", 0.2))
    f.click('th[data-sort="applicants"]', 0.9)
    f.load("document.querySelector('th.sorted')")
    f.do(("1", 0.3), ("demo.caption(null)", 0.6))


def research(f):
    f.click('#tabs [data-tab="research"]', 1.1)
    f.load("document.querySelector('#pf-results tr[data-paper]')", 60)
    f.do(("demo.caption('Spot missed opportunities in past Aalto research')", 0.3))
    f.type("#pf-q", PAPER_SEARCH, 0.04)
    row = f'#pf-results tr[data-paper="{PAPER}"]'
    f.wait_for(f"document.querySelector('{row}')", 60)  # filmed: the list changes to the lithium papers
    time.sleep(0.7)
    f.click(row, 1.0)
    time.sleep(0.3)
    if not f.js("!!document.querySelector('.paper .glance')"):
        f.js(f"openPaper('{PAPER}')")  # the click landed on a list that was being redrawn
    f.load("document.querySelector('.paper .glance')", 60)
    f.do(("1", 0.5), ("demo.zoom('.paper .glance', 1.3)", 1.5), ("demo.spot('.paper .glance')", 3.0),
         ("demo.spot(null); demo.zoom(null)", 1.0), ("demo.caption(null)", 0.6))


def sector(f):
    f.click('.sector[data-id="health-tech"]', 1.1)
    f.load("document.querySelector('.grid .panel:nth-child(3)')")
    f.do(("demo.caption('Market news, figures and funding calls')", 0.2), ("demo.spot('.grid .panel:nth-child(1)')", 1.3),
         ("demo.spot(null); demo.scroll('.grid .panel:nth-child(3)', 20)", 1.0), ("demo.spot('.grid .panel:nth-child(3)')", 1.4),
         ("demo.spot(null); demo.caption(null)", 0.6))


def end(f):
    figures = [[4, "AI agents on every disclosure"], [COUNTS["patents"], "patents searched locally"],
               [COUNTS["papers"], "Aalto papers screened"], [COUNTS["sectors"], "research areas tracked"]]
    f.do((f"demo.stats({json.dumps(figures)})", 2.9), ("document.querySelector('#d-card .stats').classList.add('out')", 0.45),
         (f"demo.card('{TITLE.format('Less background research. More time advising.')}')", 4.4))  # long enough for the last chord to ring out


def counts():
    post = lambda path: json.load(urllib.request.urlopen(urllib.request.Request(f"{APP}{path}", b'{"limit": 1}', {"Content-Type": "application/json"})))
    return {"patents": post("/api/patents/search")["stored"], "papers": post("/api/research/search")["stored"],
            "sectors": len(json.load(urllib.request.urlopen(f"{APP}/api/sectors")))}


COUNTS = {}  # figures shown in the video, read from the running terminal


SCENES = {"title": title, "upload": upload, "result": result, "assistant": assistant, "similar": similar,
          "patents": patents, "research": research, "sector": sector, "end": end}


def edit(frames, cuts, stop, out, events):
    """Play the recording at the marked speeds up to stop and write a 30 fps MP4 with ffmpeg. Chrome sends frames only
    when the page changes, so a still moment is the last frame held. The events go next to it (.json), at the times
    they land in the clip, for the soundtrack."""
    cuts = cuts + [[stop, 0]]
    events = [[max(when, cuts[0][0]), kind] for when, kind in events]  # the page's clock can be a few ms behind
    placed, spent = [], 0.0
    for (start, speed), (end, _) in zip(cuts, cuts[1:]):
        placed += [[round(spent + (when - start) / speed if speed else spent, 3), kind] for when, kind in events if start <= when < end]
        spent += (end - start) / speed if speed else 0
    picks = []  # one recorded frame for each output frame
    i = 0
    for (start, speed), (end, _) in zip(cuts, cuts[1:]):
        t = start
        while speed and t < end:
            while i + 1 < len(frames) and frames[i + 1][0] <= t:
                i += 1
            picks.append(frames[i][1])
            t += speed / FPS
    ffmpeg = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-i", "-",
                               "-vf", f"scale={W}:{H}:flags=lanczos,format=yuv420p", "-c:v", "libx264", "-crf", "17",
                               "-preset", "slow", "-movflags", "+faststart", str(out)], stdin=subprocess.PIPE)
    for path in picks:
        ffmpeg.stdin.write(path.read_bytes())
    ffmpeg.stdin.close()
    ffmpeg.wait()
    out.with_suffix(".json").write_text(json.dumps({"length": len(picks) / FPS, "events": sorted(placed)}))
    return len(picks) / FPS



def main(names):
    """Film the named scenes (all of them if none are named) into demo/clips/, then join every clip with the soundtrack."""
    unknown = [n for n in names if n not in SCENES]
    if unknown:
        sys.exit(f"Unknown scene: {', '.join(unknown)}. Scenes: {', '.join(SCENES)}")
    urllib.request.urlopen(APP, timeout=10)  # the terminal must be running
    COUNTS.update(counts())
    CLIPS.mkdir(exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix="demo-"))
    chrome = subprocess.Popen([CHROME, "--headless=new", "--remote-debugging-port=9333", f"--user-data-dir={work / 'profile'}",
                               f"--window-size={W},{H}", "--hide-scrollbars", "--force-device-scale-factor=1",
                               "--no-first-run", "--no-default-browser-check", "about:blank"],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(50):
            try:
                pages = json.load(urllib.request.urlopen("http://127.0.0.1:9333/json/list"))
                page = next(p for p in pages if p["type"] == "page")
                break
            except Exception:
                time.sleep(0.2)
        cdp = CDP(page["webSocketDebuggerUrl"])
        cdp.send("Emulation.setDeviceMetricsOverride", {"width": W, "height": H, "deviceScaleFactor": 1, "mobile": False})
        cdp.send("Page.enable")
        for number, name in enumerate(SCENES):
            if names and name not in names:
                continue
            frames = work / name
            frames.mkdir()
            f = Film(cdp, frames)
            cdp.send("Page.navigate", {"url": APP})  # every scene starts from a fresh page
            time.sleep(1.0)
            f.wait_for("document.querySelector('#drop') && document.querySelector('.sector')", 60)
            f.js(STAGE)
            if number:
                after(f, list(SCENES)[number - 1])  # start where the scene before ended
            else:
                f.js(f"demo.card('{TITLE.format('Market, patent and funding research for innovation advisors')}')")
                time.sleep(1.0)
            if name == "research":  # warm up the search so the list answers quickly on camera
                f.js(f"fetch('/api/research/search', {{method: 'POST', headers: {{'Content-Type': 'application/json'}}, body: JSON.stringify({{q: {json.dumps(PAPER_SEARCH)}}})}}).then((r) => r.json())")
            play = SCENES[name]
            cdp.send("Page.startScreencast", {"format": "jpeg", "quality": 92, "maxWidth": W, "maxHeight": H, "everyNthFrame": 1})
            f.js("demo.events = []")
            f.cuts = [[time.time(), 1.0]]
            play(f)
            stop = time.time()
            remember(f"cursor-{name}", f.js("demo.pos"))
            time.sleep(0.2)
            cdp.send("Page.stopScreencast")
            length = edit(f.frames, f.cuts, stop, CLIPS / f"{number + 1}-{name}.mp4", f.js("demo.events") + f.keys)
            print(f"{name}: {length:.1f} s")
    finally:
        chrome.terminate()
        shutil.rmtree(work, ignore_errors=True)
    sound.mix([f"{n + 1}-{name}" for n, name in enumerate(SCENES)])


if __name__ == "__main__":
    main(sys.argv[1:])
