let ws, myName, mode, target, typingTimer;
const $ = id => document.getElementById(id);

function show(id) {
  document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
  $(id).classList.add('active');
}

function onTyping() {
  ws.send(JSON.stringify({ type: 'typing', active: true, mode, to: target }));
  clearTimeout(typingTimer);
  typingTimer = setTimeout(() =>
    ws.send(JSON.stringify({ type: 'typing', active: false, mode, to: target })), 2000);
}

function submitName() {
  const n = $('name-input').value.trim();
  if (!n) return $('name-err').textContent = 'Enter name';
  myName = n;
  ws = new WebSocket('ws://localhost:8765');
  ws.onopen = () => ws.send(JSON.stringify({ type: 'login', name: n }));
  ws.onerror = () => $('name-err').textContent = 'Server error';
  ws.onmessage = e => handle(JSON.parse(e.data));
}

function joinRoom() {
  const r = $('room-input').value.trim();
  if (!r) return $('room-err').textContent = 'Enter room';
  mode = 'room'; target = r;
  ws.send(JSON.stringify({ type: 'join', room: r }));
}

function loadPrivate() {
  ws.send(JSON.stringify({ type: 'who' }));
  show('private-screen');
}

function startDM() {
  const u = $('user-select').value;
  if (!u) return $('dm-err').textContent = 'Select user';
  mode = 'dm'; target = u;
  ws.send(JSON.stringify({ type: 'load_dm', with: u }));
  openChat(u, 'private chat');
}

function openChat(title, sub) {
  $('chat-title').textContent = title;
  $('chat-sub').textContent = sub;
  $('messages').innerHTML = '';
  $('typing-bar').textContent = '';
  show('chat-screen');
  $('msg-input').focus();
}

function sendMsg() {
  const text = $('msg-input').value.trim();
  if (!text) return;
  ws.send(JSON.stringify(
    mode === 'room'
      ? { type: 'msg', text }
      : { type: 'dm', to: target, text }
  ));
  $('msg-input').value = '';
}

function handle(d) {
  if (d.type === 'ok') {
    $('display-name').textContent = myName;
    return show('home-screen');
  }

  if (d.type === 'joined') {
    openChat(`# ${d.room}`, `${d.members.length} members`);
    d.history.forEach(addMsg);
    return addMsg({ type: 'system', text: `Joined #${d.room}` });
  }

  if (d.type === 'history') {
    return d.history.forEach(addMsg);
  }

  if (d.type === 'who') {
    $('user-select').innerHTML =
      '<option value="">Select user</option>' +
      d.users.filter(u => u !== myName)
             .map(u => `<option>${esc(u)}</option>`).join('');
    return;
  }

  if (d.type === 'typing') {
    if (mode === 'room' || d.from === target)
      $('typing-bar').textContent = d.active ? `${esc(d.from)} typing...` : '';
    return;
  }

  if (d.type === 'dm') {
    const other = d.from === myName ? d.to : d.from;
    if (other !== target) return;
  }

  addMsg(d);
}

function addMsg(d) {
  const box = $('messages');
  if (!box) return;
  if (d.type === 'system') {
    box.innerHTML += `<div class="sys-msg">${esc(d.text)}</div>`;
  } else {
    $('typing-bar').textContent = '';
    const me = d.from === myName;
    box.innerHTML += `
      <div class="bubble-row ${me ? 'me' : 'other'}">
        ${!me ? `<div class="sender-name">${esc(d.from)}</div>` : ''}
        <div class="bubble">
          ${esc(d.text)}
          <span class="time">${esc(d.time)}</span>
        </div>
      </div>`;
  }
  box.scrollTop = box.scrollHeight;
}

const esc = s => String(s)
  .replaceAll('&', '&amp;')
  .replaceAll('<', '&lt;')
  .replaceAll('>', '&gt;');