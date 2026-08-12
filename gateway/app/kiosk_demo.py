from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import HTMLResponse


router = APIRouter()


@router.get("/demo/kiosk", response_class=HTMLResponse)
def kiosk_demo() -> str:
    return _render_demo("kiosk")


@router.get("/demo/public", response_class=HTMLResponse)
def public_demo() -> str:
    return _render_demo("public")


def _render_demo(mode: str) -> str:
    return KIOSK_DEMO_HTML.replace("__DEMO_MODE__", mode)


KIOSK_DEMO_HTML = r"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='12' fill='%23123f39'/%3E%3Cpath d='M15 17h34v25H32L22 50v-8h-7z' fill='%23fffdf7'/%3E%3Cpath d='M23 29h5v8h-5zm9-7h5v15h-5zm9 4h5v11h-5z' fill='%23e5b84a'/%3E%3C/svg%3E">
  <title>积养家数字人客服</title>
  <style>
    * { box-sizing: border-box; }
    :root { --forest: #123f39; --forest-strong: #073a30; --leaf: #087a63; --mist: #eef3f0; --line: #cad8d3; --ink: #173b32; --soft-radius: 14px; }
    html, body { width: 100%; height: 100%; margin: 0; background: #101416; color: #fff; font-family: "Microsoft YaHei", "PingFang SC", "Noto Sans CJK SC", sans-serif; overflow: hidden; }
    body { display: grid; place-items: center; }
    #public-nav { display: none; }
    body.public { min-height: 100dvh; display: flex; flex-direction: column; overflow: auto; background: radial-gradient(circle at 50% 20%, #dbe9e4 0, var(--mist) 42%, #e7efec 100%); }
    body.public #public-nav { width: 100%; min-height: 72px; padding: 10px 22px; display: flex; align-items: center; gap: 22px; background: rgba(255,255,255,.96); color: var(--ink); border-bottom: 1px solid var(--line); white-space: nowrap; z-index: 10; box-shadow: 0 8px 30px rgba(18,63,57,.08); }
    #brand-lockup { flex: 0 0 auto; margin-right: auto; display: grid; gap: 1px; }
    #brand-lockup strong { font-size: 17px; letter-spacing: .02em; }
    #brand-lockup span { color: #547169; font-size: 11px; }
    #nav-actions { display: flex; align-items: center; gap: 5px; }
    #public-nav a, #public-nav button { min-height: 42px; border: 1px solid transparent; border-radius: 12px; padding: 0 11px; background: transparent; color: #24594c; font: inherit; font-size: 14px; cursor: pointer; text-decoration: none; transition: background .18s ease, border-color .18s ease, color .18s ease, transform .12s ease; }
    #public-nav a:hover, #public-nav button:hover { color: var(--forest-strong); background: #e7f0ed; border-color: #cfddd8; }
    #public-nav a:active, #public-nav button:active { transform: translateY(1px); }
    #public-nav .access-link { display: inline-flex; align-items: center; gap: 7px; border-color: #b9cec7; background: #f4f8f6; }
    #public-nav .access-link small { padding: 2px 6px; border-radius: 8px; background: var(--forest); color: #fff; font-size: 10px; }
    #public-nav .store-download { color: #5f3d35; }
    #access-state { display: none; color: #547169; font-size: 12px; }
    #access-logout { display: none; }
    body[data-access="ready"] #access-state, body[data-access="ready"] #access-logout { display: inline-flex; }
    body[data-access="ready"] .access-link small { background: var(--leaf); }
    #stage { position: relative; width: min(100vw, 56.25vh); height: min(177.78vw, 100vh); overflow: hidden; background: #203035; }
    body.public #stage { flex: 1 1 auto; height: calc(100dvh - 72px); width: auto; max-width: 100vw; aspect-ratio: 9 / 16; box-shadow: 0 24px 70px rgba(18,63,57,.16); }
    #background, #avatar { position: absolute; inset: 0; width: 100%; height: 100%; }
    #background { object-fit: cover; }
    #avatar-wrap { position: absolute; left: 50%; top: 50%; width: 100%; height: 100%; transform: translate(-50%, -50%); transform-origin: center; }
    #avatar { object-fit: contain; background: transparent; }
    #shade { position: absolute; inset: 0; background: linear-gradient(180deg, rgba(8,12,13,.5), transparent 25%, transparent 62%, rgba(8,12,13,.72)); pointer-events: none; }
    #status { position: absolute; top: 3%; left: 6%; right: 6%; font-size: 15px; text-align: center; text-shadow: 0 2px 8px #000; }
    #trace { position: absolute; top: 7%; left: 6%; right: 6%; font-size: 11px; color: #d4e0dc; text-align: center; overflow-wrap: anywhere; }
    #mic-state { position: absolute; top: 9%; left: 8%; right: 8%; display: flex; align-items: center; gap: 8px; font-size: 12px; color: #e2efea; }
    #mic-meter { flex: 1; height: 5px; overflow: hidden; background: rgba(255,255,255,.22); }
    #mic-level { display: block; width: 0; height: 100%; background: #62d5a8; transition: width .08s linear; }
    #subtitle { position: absolute; left: 8%; right: 8%; bottom: 13%; font-size: 36px; line-height: 1.35; text-align: center; text-shadow: 0 3px 10px #000; max-height: 30%; overflow: hidden; }
    #sources { position: absolute; left: 7%; right: 7%; bottom: 3%; font-size: 12px; color: #d9e8e2; text-align: center; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    #consult { position: absolute; left: 50%; top: 90%; transform: translate(-50%, -50%); min-width: 156px; min-height: 54px; padding: 0 24px; border: 1px solid rgba(255,255,255,.6); border-radius: 14px; background: #087a63; color: #fff; font-size: 18px; font-weight: 700; cursor: pointer; }
    #consult[data-state="recording"] { background: #a33838; }
    #consult:disabled { opacity: .55; cursor: wait; }
    #audio-retry { position: absolute; left: 50%; bottom: 8%; transform: translateX(-50%); min-height: 42px; padding: 0 18px; border: 1px solid rgba(255,255,255,.7); background: #fff; color: #173b32; font-weight: 700; cursor: pointer; }
    #text-form { position: absolute; left: 6%; right: 6%; top: 12%; display: flex; gap: 6px; opacity: .2; transition: opacity .2s; }
    #text-form:focus-within, #text-form:hover { opacity: .95; }
    body.public #text-form { opacity: .95; }
    #text-question { min-width: 0; flex: 1; height: 40px; border: 1px solid rgba(255,255,255,.45); border-radius: 12px; padding: 0 12px; background: rgba(10,18,18,.74); color: #fff; }
    #text-submit { width: 64px; border: 0; border-radius: 12px; background: #dce9e4; color: #18312a; font-weight: 700; cursor: pointer; }
    dialog { width: min(92vw, 440px); max-width: 440px; border: 1px solid #d4e0dc; border-radius: var(--soft-radius); padding: 26px; color: var(--ink); background: #fff; box-shadow: 0 24px 70px rgba(7,58,48,.28); }
    dialog::backdrop { background: rgba(0,0,0,.55); }
    dialog h2 { margin: 0 0 12px; font-size: 20px; }
    dialog p { line-height: 1.65; }
    dialog button { min-height: 44px; border: 0; border-radius: 12px; padding: 0 16px; background: var(--leaf); color: #fff; font: inherit; font-weight: 700; cursor: pointer; }
    #access-form { display: grid; gap: 15px; }
    #access-form label { font-size: 13px; font-weight: 700; }
    #access-description { margin: 0; color: #557269; font-size: 14px; line-height: 1.6; }
    #password-row { display: grid; grid-template-columns: 1fr auto; gap: 8px; }
    #access-password { min-width: 0; min-height: 48px; border: 1px solid #9bb5ac; border-radius: 12px; padding: 0 13px; color: #102f29; background: #f8fbfa; font: inherit; }
    #access-password:focus { outline: 3px solid rgba(8,122,99,.2); border-color: var(--leaf); }
    #password-toggle { min-width: 72px; border: 1px solid #9bb5ac; background: #eef5f2; color: var(--forest); }
    #access-error { min-height: 20px; margin: 0; color: #9a302d; font-size: 13px; }
    #access-actions { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
    #access-cancel { border: 1px solid #9bb5ac; background: #fff; color: var(--forest); }
    #access-submit:disabled { opacity: .6; cursor: wait; }
    @media (max-width: 600px) {
      body.public #public-nav { min-height: 62px; padding: 8px 10px; gap: 10px; overflow-x: auto; }
      #brand-lockup { margin-right: 6px; }
      #brand-lockup strong { font-size: 15px; }
      #brand-lockup span, #access-state { display: none !important; }
      #nav-actions { gap: 3px; }
      #public-nav a, #public-nav button { min-height: 42px; padding: 0 9px; font-size: 13px; }
      #public-nav .access-link small { display: none; }
      #stage, body.public #stage { width: 100vw; height: calc(100dvh - 62px); max-height: none; aspect-ratio: auto; }
      body.kiosk #stage { height: 100dvh; }
      #subtitle { font-size: 30px; }
      #access-gate { width: 100vw; max-width: none; margin: auto 0 0; border-radius: 14px 14px 0 0; padding: 24px 18px calc(24px + env(safe-area-inset-bottom)); }
    }
    @media (prefers-reduced-motion: reduce) { *, *::before, *::after { scroll-behavior: auto !important; transition-duration: .01ms !important; animation-duration: .01ms !important; } }
  </style>
</head>
<body class="__DEMO_MODE__">
  <header id="public-nav" aria-label="公开导航">
    <span id="brand-lockup"><strong>积养家AI数字人</strong><span>健康生活知识服务</span></span>
    <nav id="nav-actions" aria-label="主要功能">
      <a href="#consult">语音咨询</a>
      <a href="#text-question">文字咨询</a>
      <button class="access-link" type="button" data-access-target="knowledge-center" data-access-label="知识中心"><span>知识中心</span><small>需验证</small></button>
      <button class="access-link" type="button" data-access-target="public-materials" data-access-label="公开资料"><span>公开资料</span><small>需验证</small></button>
      <a href="/downloads/jiyangjia-ai-digital-human.apk">手机体验版</a>
      <a class="store-download" href="/downloads/jiyangjia-ai-store-kiosk.apk" title="仅用于受管门店大屏，普通手机请勿安装">门店大屏版</a>
      <button id="mic-help-open" type="button">麦克风帮助</button>
      <span id="access-state" aria-live="polite">资料入口已解锁</span>
      <button id="access-logout" type="button">退出资料访问</button>
    </nav>
  </header>
  <main id="stage">
    <img id="background" alt="" hidden>
    <div id="avatar-wrap"><video id="avatar" muted loop autoplay playsinline></video></div>
    <div id="shade"></div>
    <div id="status" aria-live="polite">正在载入人物形象</div>
    <div id="trace"></div>
    <div id="mic-state"><span id="mic-label">麦克风：等待授权</span><span id="mic-meter" aria-hidden="true"><span id="mic-level"></span></span></div>
    <form id="text-form"><input id="text-question" placeholder="输入问题" autocomplete="off"><button id="text-submit">发送</button></form>
    <div id="subtitle" aria-live="polite">您好，欢迎来到积养家</div>
    <div id="sources"></div>
    <button id="audio-retry" type="button" hidden>播放回答</button>
    <button id="consult" type="button" data-state="idle">开始咨询</button>
  </main>
  <dialog id="mic-help">
    <h2>启用实时语音</h2>
    <p>请在浏览器地址栏的网站权限中允许麦克风，然后重新点击“开始咨询”。说话时会显示音量和识别文字；点击结束，或说完后静音 3 秒即可发送。</p>
    <button id="mic-help-close" type="button">知道了</button>
  </dialog>
  <dialog id="access-gate" aria-labelledby="access-title" aria-describedby="access-description">
    <form id="access-form">
      <div>
        <h2 id="access-title">验证资料访问</h2>
        <p id="access-description">请输入访问密码，验证后 24 小时内可查看知识中心和公开资料。</p>
      </div>
      <label for="access-password">访问密码</label>
      <div id="password-row">
        <input id="access-password" name="password" type="password" autocomplete="current-password" maxlength="256" required>
        <button id="password-toggle" type="button" aria-pressed="false">显示</button>
      </div>
      <p id="access-error" role="alert" aria-live="polite"></p>
      <div id="access-actions">
        <button id="access-cancel" type="button">取消</button>
        <button id="access-submit" type="submit">验证并继续</button>
      </div>
    </form>
  </dialog>
  <script>
    const stage = document.querySelector('#stage');
    const background = document.querySelector('#background');
    const avatarWrap = document.querySelector('#avatar-wrap');
    const avatar = document.querySelector('#avatar');
    const status = document.querySelector('#status');
    const trace = document.querySelector('#trace');
    const subtitle = document.querySelector('#subtitle');
    const sources = document.querySelector('#sources');
    const consult = document.querySelector('#consult');
    const textForm = document.querySelector('#text-form');
    const textQuestion = document.querySelector('#text-question');
    const micLabel = document.querySelector('#mic-label');
    const micLevel = document.querySelector('#mic-level');
    const audioRetry = document.querySelector('#audio-retry');
    const micHelp = document.querySelector('#mic-help');
    const micHelpOpen = document.querySelector('#mic-help-open');
    const micHelpClose = document.querySelector('#mic-help-close');
    const accessGate = document.querySelector('#access-gate');
    const accessForm = document.querySelector('#access-form');
    const accessPassword = document.querySelector('#access-password');
    const accessDescription = document.querySelector('#access-description');
    const accessError = document.querySelector('#access-error');
    const accessSubmit = document.querySelector('#access-submit');
    const accessCancel = document.querySelector('#access-cancel');
    const passwordToggle = document.querySelector('#password-toggle');
    const accessLogout = document.querySelector('#access-logout');
    const protectedLinks = [...document.querySelectorAll('[data-access-target]')];
    let microphone = null;
    let answerAudio = null;
    let recordingTimer = null;
    let audioContext = null;
    let streamSource = null;
    let streamProcessor = null;
    let silentGain = null;
    let streamSocket = null;
    let pcmRemainder = new Int16Array(0);
    let hasDetectedSpeech = false;
    let consecutiveSpeechFrames = 0;
    let lastVoiceAt = 0;
    let maxRecordSeconds = 20;
    let streamRequestId = '';
    let streamGeneration = 0;
    const SILENCE_AUTO_SEND_MS = 3000;
    const SPEECH_RMS_THRESHOLD = 0.02;
    const SPEECH_CONFIRMATION_FRAMES = 2;
    const TARGET_SAMPLE_RATE = 16000;
    const PCM_FRAME_SAMPLES = 320;
    let accessAuthenticated = false;
    let pendingAccessTarget = '';

    const newRequestId = () => `browser-${crypto.randomUUID?.() || `${Date.now()}-${Math.random().toString(16).slice(2)}`}`;

    function shouldAutoSendAfterSilence(speechDetected, voiceAt, now) {
      return speechDetected && voiceAt > 0 && now - voiceAt >= SILENCE_AUTO_SEND_MS;
    }

    function setStatus(value, requestId='') {
      status.textContent = value;
      trace.textContent = requestId ? `request_id=${requestId}` : '';
    }

    function setMicrophoneState(value, level=0) {
      micLabel.textContent = `麦克风：${value}`;
      micLevel.style.width = `${Math.max(0, Math.min(100, level))}%`;
    }

    function setAccessState(authenticated, label='') {
      accessAuthenticated = authenticated;
      document.body.dataset.access = authenticated ? 'ready' : 'locked';
      protectedLinks.forEach(button => {
        const badge = button.querySelector('small');
        if (badge) badge.textContent = authenticated ? '已解锁' : '需验证';
      });
      const stateLabel = document.querySelector('#access-state');
      if (stateLabel) stateLabel.textContent = label || (authenticated ? '资料入口已解锁' : '资料入口需验证');
    }

    async function refreshAccessSession() {
      if (!document.body.classList.contains('public')) return;
      try {
        const response = await fetch('/api/v1/public-access/session', {credentials:'same-origin', cache:'no-store'});
        const payload = await response.json();
        setAccessState(Boolean(payload.authenticated));
      } catch (_) {
        setAccessState(false, '资料入口暂不可用');
      }
    }

    function openAccessDestination(target) {
      const url = `/access/go/${encodeURIComponent(target)}`;
      const opened = window.open(url, '_blank', 'noopener,noreferrer');
      if (!opened) window.location.assign(url);
    }

    function showAccessGate(target, label) {
      pendingAccessTarget = target;
      accessDescription.textContent = `请输入访问密码以查看${label}。验证成功后 24 小时内无需重复输入。`;
      accessError.textContent = '';
      accessPassword.value = '';
      accessPassword.type = 'password';
      passwordToggle.textContent = '显示';
      passwordToggle.setAttribute('aria-pressed', 'false');
      accessGate.showModal();
      requestAnimationFrame(() => accessPassword.focus());
    }

    async function submitAccessPassword(event) {
      event.preventDefault();
      accessError.textContent = '';
      accessSubmit.disabled = true;
      accessSubmit.textContent = '正在验证';
      try {
        const response = await fetch('/api/v1/public-access/login', {
          method:'POST',
          credentials:'same-origin',
          headers:{'Content-Type':'application/json'},
          body:JSON.stringify({password:accessPassword.value})
        });
        const payload = await response.json();
        if (!response.ok) throw new Error(payload.detail?.message || '验证失败，请稍后再试。');
        setAccessState(true);
        const target = pendingAccessTarget;
        accessGate.close();
        window.location.assign(`/access/go/${encodeURIComponent(target)}`);
      } catch (error) {
        accessError.textContent = error.message || '验证失败，请稍后再试。';
        accessPassword.select();
      } finally {
        accessSubmit.disabled = false;
        accessSubmit.textContent = '验证并继续';
      }
    }

    function microphoneFailureMessage(error) {
      if (error?.name === 'NotAllowedError' || error?.name === 'SecurityError') return '麦克风权限被拒绝，请在网站权限中允许后重试';
      if (error?.name === 'NotFoundError' || error?.name === 'DevicesNotFoundError') return '没有检测到可用麦克风';
      if (error?.name === 'NotReadableError' || error?.name === 'TrackStartError') return '麦克风正被其他应用占用';
      return '麦克风启动失败，请检查浏览器权限和输入设备';
    }

    function applyProfile(profile) {
      if (!profile) return;
      const scaleMode = profile.scale_mode || 'fit';
      avatar.style.objectFit = scaleMode === 'crop' ? 'cover' : (scaleMode === 'fill' ? 'fill' : 'contain');
      avatarWrap.style.left = `${Number(profile.character_anchor_x ?? .5) * 100}%`;
      avatarWrap.style.top = `${Number(profile.character_anchor_y ?? .5) * 100}%`;
      avatarWrap.style.transform = `translate(-50%, -50%) scale(${Number(profile.character_scale ?? 1)})`;
      const safe = profile.subtitle_safe_area || {};
      subtitle.style.left = `${Number(safe.left ?? .08) * 100}%`;
      subtitle.style.right = `${Number(safe.right ?? .08) * 100}%`;
      subtitle.style.bottom = `${Math.max(.11, Number(safe.bottom ?? .08)) * 100}%`;
      const profileWidth = Math.max(1, Number(profile.width_px || 1080));
      const previewScale = Math.min(1, stage.clientWidth / profileWidth);
      subtitle.style.fontSize = `${Math.max(16, Number(profile.subtitle_font_px || 36) * previewScale)}px`;
      const button = profile.button_positions?.consult || {x:.5,y:.9};
      consult.style.left = `${Number(button.x ?? .5) * 100}%`;
      consult.style.top = `${Number(button.y ?? .9) * 100}%`;
    }

    async function loadPresentation() {
      try {
        const bootstrapResponse = await fetch('/api/v1/client/bootstrap?width=1080&height=1920&orientation=portrait&version_code=1');
        if (!bootstrapResponse.ok) throw new Error('展示配置不可用');
        const payload = await bootstrapResponse.json();
        maxRecordSeconds = Number(payload.config?.max_record_seconds || 20);
        applyProfile(payload.display_profile);
        const manifest = payload.assets_manifest || {};
        const backgroundUrl = manifest.background?.url || manifest.background?.uri;
        const videoUrl = manifest.video?.url || manifest.video?.uri;
        if (backgroundUrl) {
          background.src = backgroundUrl;
          background.hidden = false;
        }
        if (videoUrl && avatar.dataset.version !== manifest.video.sha256) {
          avatar.dataset.version = manifest.video.sha256 || manifest.video.version || '';
          avatar.src = videoUrl;
          await avatar.play().catch(() => { setStatus('待机视频需要点击页面后播放'); });
        }
        setStatus(manifest.video ? '积养家数字人在线' : '等待发布人物素材');
      } catch (error) {
        setStatus(error.message || '展示载入失败');
      }
    }

    function stopAnswer() {
      if (!answerAudio) return;
      answerAudio.pause();
      answerAudio.src = '';
      answerAudio = null;
    }

    function websocketUrl() {
      return `${location.protocol === 'https:' ? 'wss:' : 'ws:'}//${location.host}/api/v1/dialogue/stream`;
    }

    function mergePcm(frame) {
      const merged = new Int16Array(pcmRemainder.length + frame.length);
      merged.set(pcmRemainder);
      merged.set(frame, pcmRemainder.length);
      pcmRemainder = merged;
      while (pcmRemainder.length >= PCM_FRAME_SAMPLES && streamSocket?.readyState === WebSocket.OPEN) {
        streamSocket.send(pcmRemainder.slice(0, PCM_FRAME_SAMPLES).buffer);
        pcmRemainder = pcmRemainder.slice(PCM_FRAME_SAMPLES);
      }
    }

    function downsampleToPcm16(samples, inputRate) {
      const ratio = inputRate / TARGET_SAMPLE_RATE;
      const length = Math.max(1, Math.round(samples.length / ratio));
      const result = new Int16Array(length);
      for (let index = 0; index < length; index += 1) {
        const start = Math.floor(index * ratio);
        const end = Math.min(samples.length, Math.floor((index + 1) * ratio));
        let sum = 0;
        for (let sampleIndex = start; sampleIndex < Math.max(start + 1, end); sampleIndex += 1) sum += samples[sampleIndex] || 0;
        const value = Math.max(-1, Math.min(1, sum / Math.max(1, end - start)));
        result[index] = value < 0 ? value * 0x8000 : value * 0x7fff;
      }
      return result;
    }

    function stopStreamCapture() {
      clearTimeout(recordingTimer);
      recordingTimer = null;
      if (streamProcessor) streamProcessor.disconnect();
      if (streamSource) streamSource.disconnect();
      if (silentGain) silentGain.disconnect();
      streamProcessor = null;
      streamSource = null;
      silentGain = null;
      microphone?.getTracks().forEach(track => track.stop());
      microphone = null;
      const context = audioContext;
      audioContext = null;
      if (context && context.state !== 'closed') context.close().catch(() => {});
      setMicrophoneState('已停止', 0);
    }

    function resetStreamState() {
      stopStreamCapture();
      if (streamSocket && streamSocket.readyState === WebSocket.OPEN) streamSocket.close(1000, 'complete');
      streamSocket = null;
      pcmRemainder = new Int16Array(0);
      streamRequestId = '';
    }

    function renderSources(items) {
      sources.textContent = (items || []).slice(0, 3).map(item => item.title || item.uri).filter(Boolean).join(' / ');
    }

    async function playAnswerAudio(audioId, requestId) {
      if (!audioId) {
        setStatus('已收到文本回答，未返回语音文件', requestId);
        resetButton();
        return;
      }
      setStatus('正在播报回答', requestId);
      answerAudio = new Audio(`/api/v1/audio/${encodeURIComponent(audioId)}`);
      audioRetry.hidden = true;
      answerAudio.onended = resetConsultation;
      answerAudio.onerror = () => { setStatus('回答音频播放失败', requestId); resetButton(); };
      try {
        await answerAudio.play();
      } catch (error) {
        audioRetry.hidden = false;
        setStatus('浏览器等待点击播放回答', requestId);
        subtitle.textContent = '回答已生成，请点击“播放回答”';
      }
    }

    function handleStreamEvent(payload) {
      const type = payload.type || 'unknown';
      if (type === 'stage') {
        const labels = {
          buffered_fallback: '实时识别降级处理中',
          asr_finalizing: '正在确认识别文字',
          answering: '正在检索知识并生成回答',
          cancelled: '咨询已取消'
        };
        if (labels[payload.stage]) setStatus(labels[payload.stage], payload.request_id || streamRequestId);
        return;
      }
      if (type === 'ready') {
        setStatus('实时语音已连接，请开始说话', streamRequestId);
        setMicrophoneState('已连接，请开始说话', 0);
        return;
      }
      if (type === 'partial_transcript') {
        subtitle.textContent = payload.text || payload.transcript || '正在识别…';
        setStatus('实时识别中', payload.request_id || streamRequestId);
        return;
      }
      if (type === 'final_transcript') {
        subtitle.textContent = payload.text || payload.transcript?.text || '识别完成，正在回答';
        setStatus('正在检索与生成回答', payload.request_id || streamRequestId);
        setMicrophoneState('识别完成', 0);
        return;
      }
      if (type === 'answer') {
        const answer = payload.answer?.text || payload.answer || payload.text || '';
        subtitle.textContent = payload.answer?.subtitles?.[0] || answer || '正在生成语音';
        renderSources(payload.sources || payload.knowledge?.sources);
        return;
      }
      if (type === 'tts_ready') {
        playAnswerAudio(payload.tts?.audio_id || payload.audio_id, payload.request_id || streamRequestId).catch(error => {
          subtitle.textContent = error.message || '回答音频播放失败';
          resetButton();
        });
        return;
      }
      if (type === 'error') {
        const message = payload.message_for_user || payload.message || payload.detail || '实时语音服务暂时不可用';
        subtitle.textContent = message;
        setStatus(payload.failed_stage ? `咨询失败：${payload.failed_stage}` : '实时语音失败', payload.request_id || streamRequestId);
        resetStreamState();
        resetButton();
      }
    }

    function startPcmStreaming() {
      if (!audioContext || !microphone || !streamSocket || streamSocket.readyState !== WebSocket.OPEN) return;
      streamSource = audioContext.createMediaStreamSource(microphone);
      streamProcessor = audioContext.createScriptProcessor(4096, 1, 1);
      silentGain = audioContext.createGain();
      silentGain.gain.value = 0;
      streamProcessor.onaudioprocess = event => {
        const samples = event.inputBuffer.getChannelData(0);
        let energy = 0;
        for (const sample of samples) energy += sample * sample;
        const now = performance.now();
        const rms = Math.sqrt(energy / samples.length);
        setMicrophoneState(hasDetectedSpeech ? '实时识别中' : '正在监听', Math.min(100, rms * 500));
        if (rms >= SPEECH_RMS_THRESHOLD) {
          consecutiveSpeechFrames += 1;
          if (consecutiveSpeechFrames >= SPEECH_CONFIRMATION_FRAMES) {
            hasDetectedSpeech = true;
            lastVoiceAt = now;
            setStatus('实时传输中，静音 3 秒后自动发送', streamRequestId);
          }
        } else {
          consecutiveSpeechFrames = 0;
          if (shouldAutoSendAfterSilence(hasDetectedSpeech, lastVoiceAt, now)) {
            stopStreaming('silence');
            return;
          }
        }
        mergePcm(downsampleToPcm16(samples, audioContext.sampleRate));
      };
      streamSource.connect(streamProcessor);
      streamProcessor.connect(silentGain);
      silentGain.connect(audioContext.destination);
    }

    async function startStreaming() {
      stopAnswer();
      const AudioContextClass = window.AudioContext || window.webkitAudioContext;
      if (!navigator.mediaDevices?.getUserMedia || !AudioContextClass || !window.WebSocket) {
        setStatus('浏览器不支持实时麦克风');
        return;
      }
      try {
        setMicrophoneState('正在请求权限', 0);
        microphone = await navigator.mediaDevices.getUserMedia({audio:{echoCancellation:true,noiseSuppression:true,autoGainControl:true}});
        audioContext = new AudioContextClass();
        await audioContext.resume();
        streamRequestId = newRequestId();
        streamSocket = new WebSocket(websocketUrl());
        streamSocket.binaryType = 'arraybuffer';
        streamSocket.onopen = () => {
          streamGeneration += 1;
          streamSocket.send(JSON.stringify({type:'start', session_id:'browser-kiosk-demo', request_id:streamRequestId, generation:streamGeneration}));
          startPcmStreaming();
        };
        streamSocket.onmessage = event => {
          try { handleStreamEvent(JSON.parse(event.data)); }
          catch (_) { setStatus('实时语音响应格式错误', streamRequestId); }
        };
        streamSocket.onerror = () => {
          if (consult.dataset.state !== 'idle') {
            setStatus('实时语音连接失败', streamRequestId);
            setMicrophoneState('连接失败', 0);
          }
        };
        streamSocket.onclose = () => {
          if (consult.dataset.state === 'recording') {
            subtitle.textContent = '实时语音连接已关闭';
            resetStreamState();
            resetButton();
          }
        };
        consult.dataset.state = 'recording';
        consult.textContent = '结束对话';
        subtitle.textContent = '请开始说话';
        setStatus('正在连接实时语音', streamRequestId);
        hasDetectedSpeech = false;
        consecutiveSpeechFrames = 0;
        lastVoiceAt = 0;
        recordingTimer = setTimeout(() => stopStreaming('maximum-duration'), maxRecordSeconds * 1000);
      } catch (error) {
        resetStreamState();
        const message = microphoneFailureMessage(error);
        setStatus('麦克风不可用');
        setMicrophoneState('不可用', 0);
        subtitle.textContent = message;
        if (document.body.classList.contains('public')) micHelp.showModal();
      }
    }

    function stopStreaming(reason='manual') {
      if (!streamSocket || streamSocket.readyState !== WebSocket.OPEN) return;
      clearTimeout(recordingTimer);
      streamSocket.send(JSON.stringify({type:'stop', request_id:streamRequestId}));
      stopStreamCapture();
      consult.dataset.state = 'busy';
      consult.textContent = '处理中';
      consult.disabled = true;
      subtitle.textContent = reason === 'silence' ? '已静音 3 秒，正在生成回答' : '正在生成回答';
      setStatus(reason === 'silence' ? '实时语音自动提交' : '实时语音提交中', streamRequestId);
    }

    async function submitText(question) {
      const requestId = newRequestId();
      await runDialogue('/api/v1/dialogue/text', {
        method:'POST',
        headers:{'Content-Type':'application/json','X-Request-Id':requestId},
        body:JSON.stringify({session_id:'local-avatar-demo',request_id:requestId,text:question})
      }, requestId);
    }

    async function runDialogue(url, options, requestId) {
      consult.disabled = true;
      consult.dataset.state = 'busy';
      consult.textContent = '处理中';
      subtitle.textContent = '正在生成回答';
      setStatus('ASR / RAG / LLM / TTS', requestId);
      try {
        const response = await fetch(url, options);
        const payload = await response.json();
        if (!response.ok) throw new Error(payload.detail?.message_for_user || payload.detail?.message || '咨询服务暂时不可用');
        const answer = payload.answer?.text || '';
        subtitle.textContent = payload.answer?.subtitles?.[0] || answer;
        sources.textContent = (payload.sources || []).slice(0, 3).map(item => item.title || item.uri).filter(Boolean).join(' / ');
        setStatus('正在播报回答', payload.request_id);
        answerAudio = new Audio(`/api/v1/audio/${encodeURIComponent(payload.tts.audio_id)}`);
        answerAudio.onended = resetConsultation;
        answerAudio.onerror = () => { setStatus('回答音频播放失败', payload.request_id); resetButton(); };
        await answerAudio.play();
      } catch (error) {
        subtitle.textContent = error.message || '咨询失败';
        setStatus('咨询失败', requestId);
        resetButton();
      }
    }

    function resetConsultation() {
      setStatus('积养家数字人在线');
      resetStreamState();
      audioRetry.hidden = true;
      setMicrophoneState('等待授权', 0);
      resetButton();
    }

    function resetButton() {
      consult.disabled = false;
      consult.dataset.state = 'idle';
      consult.textContent = '开始咨询';
    }

    avatar.addEventListener('error', () => setStatus('待机视频加载失败，请刷新后重试'));
    avatar.addEventListener('loadeddata', () => {
      if (consult.dataset.state === 'idle') setStatus('积养家数字人在线');
    });
    document.addEventListener('pointerdown', () => {
      if (avatar.paused && avatar.src) avatar.play().catch(() => {});
    }, {once:true});
    consult.addEventListener('click', () => {
      if (consult.dataset.state === 'recording') stopStreaming('manual');
      else startStreaming();
    });
    audioRetry.addEventListener('click', () => {
      if (!answerAudio) return;
      answerAudio.play().then(() => { audioRetry.hidden = true; }).catch(() => setStatus('回答音频仍无法播放'));
    });
    micHelpOpen?.addEventListener('click', () => micHelp.showModal());
    micHelpClose.addEventListener('click', () => micHelp.close());
    protectedLinks.forEach(button => button.addEventListener('click', () => {
      const target = button.dataset.accessTarget;
      if (accessAuthenticated) openAccessDestination(target);
      else showAccessGate(target, button.dataset.accessLabel || '资料');
    }));
    accessForm.addEventListener('submit', submitAccessPassword);
    accessCancel.addEventListener('click', () => accessGate.close());
    passwordToggle.addEventListener('click', () => {
      const visible = accessPassword.type === 'text';
      accessPassword.type = visible ? 'password' : 'text';
      passwordToggle.textContent = visible ? '显示' : '隐藏';
      passwordToggle.setAttribute('aria-pressed', String(!visible));
      accessPassword.focus();
    });
    accessLogout.addEventListener('click', async () => {
      await fetch('/api/v1/public-access/logout', {method:'POST', credentials:'same-origin'}).catch(() => {});
      setAccessState(false);
    });
    textForm.addEventListener('submit', event => {
      event.preventDefault();
      const question = textQuestion.value.trim();
      if (!question) return;
      stopAnswer();
      textQuestion.value = '';
      submitText(question);
    });
    loadPresentation();
    refreshAccessSession();
    setInterval(loadPresentation, 60000);
  </script>
</body>
</html>
"""
