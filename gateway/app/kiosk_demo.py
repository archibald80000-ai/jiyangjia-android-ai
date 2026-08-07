from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import HTMLResponse


router = APIRouter()


@router.get("/demo/kiosk", response_class=HTMLResponse)
def kiosk_demo() -> str:
    return KIOSK_DEMO_HTML


KIOSK_DEMO_HTML = r"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
  <title>积养家数字人客服</title>
  <style>
    * { box-sizing: border-box; }
    html, body { width: 100%; height: 100%; margin: 0; background: #101416; color: #fff; font-family: system-ui, sans-serif; overflow: hidden; }
    body { display: grid; place-items: center; }
    #stage { position: relative; width: min(100vw, 56.25vh); height: min(177.78vw, 100vh); overflow: hidden; background: #203035; }
    #background, #avatar { position: absolute; inset: 0; width: 100%; height: 100%; }
    #background { object-fit: cover; }
    #avatar-wrap { position: absolute; left: 50%; top: 50%; width: 100%; height: 100%; transform: translate(-50%, -50%); transform-origin: center; }
    #avatar { object-fit: contain; background: transparent; }
    #shade { position: absolute; inset: 0; background: linear-gradient(180deg, rgba(8,12,13,.5), transparent 25%, transparent 62%, rgba(8,12,13,.72)); pointer-events: none; }
    #status { position: absolute; top: 3%; left: 6%; right: 6%; font-size: 15px; text-align: center; text-shadow: 0 2px 8px #000; }
    #trace { position: absolute; top: 7%; left: 6%; right: 6%; font-size: 11px; color: #d4e0dc; text-align: center; overflow-wrap: anywhere; }
    #subtitle { position: absolute; left: 8%; right: 8%; bottom: 13%; font-size: 36px; line-height: 1.35; text-align: center; text-shadow: 0 3px 10px #000; max-height: 30%; overflow: hidden; }
    #sources { position: absolute; left: 7%; right: 7%; bottom: 3%; font-size: 12px; color: #d9e8e2; text-align: center; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    #consult { position: absolute; left: 50%; top: 90%; transform: translate(-50%, -50%); min-width: 156px; min-height: 54px; padding: 0 24px; border: 1px solid rgba(255,255,255,.6); border-radius: 6px; background: #087a63; color: #fff; font-size: 18px; font-weight: 700; cursor: pointer; }
    #consult[data-state="recording"] { background: #a33838; }
    #consult:disabled { opacity: .55; cursor: wait; }
    #text-form { position: absolute; left: 6%; right: 6%; top: 11%; display: flex; gap: 6px; opacity: .2; transition: opacity .2s; }
    #text-form:focus-within, #text-form:hover { opacity: .95; }
    #text-question { min-width: 0; flex: 1; height: 36px; border: 1px solid rgba(255,255,255,.45); border-radius: 4px; padding: 0 10px; background: rgba(10,18,18,.7); color: #fff; }
    #text-submit { width: 58px; border: 0; border-radius: 4px; background: #dce9e4; color: #18312a; font-weight: 700; cursor: pointer; }
    @media (max-width: 600px) { #stage { width: 100vw; height: 100vh; } #subtitle { font-size: 30px; } }
  </style>
</head>
<body>
  <main id="stage">
    <img id="background" alt="" hidden>
    <div id="avatar-wrap"><video id="avatar" muted loop autoplay playsinline></video></div>
    <div id="shade"></div>
    <div id="status" aria-live="polite">正在载入人物形象</div>
    <div id="trace"></div>
    <form id="text-form"><input id="text-question" placeholder="输入问题" autocomplete="off"><button id="text-submit">发送</button></form>
    <div id="subtitle" aria-live="polite">您好，欢迎来到积养家</div>
    <div id="sources"></div>
    <button id="consult" type="button" data-state="idle">开始咨询</button>
  </main>
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
    const SILENCE_AUTO_SEND_MS = 3000;
    const SPEECH_RMS_THRESHOLD = 0.02;
    const SPEECH_CONFIRMATION_FRAMES = 2;
    const TARGET_SAMPLE_RATE = 16000;
    const PCM_FRAME_SAMPLES = 320;

    const newRequestId = () => `browser-${crypto.randomUUID?.() || `${Date.now()}-${Math.random().toString(16).slice(2)}`}`;

    function shouldAutoSendAfterSilence(speechDetected, voiceAt, now) {
      return speechDetected && voiceAt > 0 && now - voiceAt >= SILENCE_AUTO_SEND_MS;
    }

    function setStatus(value, requestId='') {
      status.textContent = value;
      trace.textContent = requestId ? `request_id=${requestId}` : '';
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
      answerAudio.onended = resetConsultation;
      answerAudio.onerror = () => { setStatus('回答音频播放失败', requestId); resetButton(); };
      await answerAudio.play();
    }

    function handleStreamEvent(payload) {
      const type = payload.type || 'unknown';
      if (type === 'ready') {
        setStatus('实时语音已连接，请开始说话', streamRequestId);
        return;
      }
      if (type === 'partial_transcript') {
        subtitle.textContent = payload.text || payload.transcript || '正在识别…';
        setStatus('实时识别中', payload.request_id || streamRequestId);
        return;
      }
      if (type === 'final_transcript') {
        subtitle.textContent = payload.text || payload.transcript || '识别完成，正在回答';
        setStatus('正在检索与生成回答', payload.request_id || streamRequestId);
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
        microphone = await navigator.mediaDevices.getUserMedia({audio:{echoCancellation:true,noiseSuppression:true,autoGainControl:true}});
        audioContext = new AudioContextClass();
        await audioContext.resume();
        streamRequestId = newRequestId();
        streamSocket = new WebSocket(websocketUrl());
        streamSocket.binaryType = 'arraybuffer';
        streamSocket.onopen = () => {
          streamSocket.send(JSON.stringify({type:'start', session_id:'browser-kiosk-demo', request_id:streamRequestId, generation:'web-realtime'}));
          startPcmStreaming();
        };
        streamSocket.onmessage = event => {
          try { handleStreamEvent(JSON.parse(event.data)); }
          catch (_) { setStatus('实时语音响应格式错误', streamRequestId); }
        };
        streamSocket.onerror = () => {
          if (consult.dataset.state !== 'idle') setStatus('实时语音连接失败', streamRequestId);
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
        setStatus('麦克风不可用');
        subtitle.textContent = error.name || '请检查麦克风权限';
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
    textForm.addEventListener('submit', event => {
      event.preventDefault();
      const question = textQuestion.value.trim();
      if (!question) return;
      stopAnswer();
      textQuestion.value = '';
      submitText(question);
    });
    loadPresentation();
    setInterval(loadPresentation, 60000);
  </script>
</body>
</html>
"""
