from __future__ import annotations


def admin_page(section: str) -> str:
    titles = {
        "system": "系统状态",
        "knowledge": "知识库",
        "avatar": "数字人形象",
        "display": "大屏配置",
    }
    title = titles[section]
    return (
        _TEMPLATE.replace("__TITLE__", title)
        .replace("__SECTION__", section)
        .replace(f'__ACTIVE_{section.upper()}__', "active")
        .replace("__ACTIVE_SYSTEM__", "")
        .replace("__ACTIVE_KNOWLEDGE__", "")
        .replace("__ACTIVE_AVATAR__", "")
        .replace("__ACTIVE_DISPLAY__", "")
    )


_TEMPLATE = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>__TITLE__ | 积养家 AI 客服</title>
  <style>
    :root { color-scheme: light; font-family: Inter, "Microsoft YaHei", sans-serif; color: #18201d; background: #f4f6f5; }
    * { box-sizing: border-box; letter-spacing: 0; }
    body { margin: 0; min-width: 320px; }
    header { min-height: 58px; padding: 9px 24px; background: #183b32; color: #fff; display: flex; align-items: center; justify-content: space-between; gap: 16px; }
    header strong { font-size: 17px; }
    header label { display: flex; align-items: center; gap: 8px; font-size: 13px; }
    header input { width: 180px; background: #fff; border: 0; }
    .layout { display: grid; grid-template-columns: 190px minmax(0,1fr); min-height: calc(100vh - 58px); }
    nav { padding: 18px 12px; background: #fff; border-right: 1px solid #dbe2df; }
    nav a { display: block; color: #34443e; text-decoration: none; padding: 11px 12px; border-radius: 6px; margin-bottom: 4px; }
    nav a.active { color: #fff; background: #28745e; font-weight: 600; }
    main { padding: 24px; overflow: hidden; }
    h1 { margin: 0 0 18px; font-size: 24px; }
    h2 { font-size: 16px; margin: 0 0 14px; }
    hr { border: 0; border-top: 1px solid #e2e7e5; margin: 18px 0; }
    .toolbar { display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 16px; align-items: end; }
    .toolbar form { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
    .panel { background: #fff; border: 1px solid #dbe2df; border-radius: 6px; padding: 18px; margin-bottom: 16px; overflow: auto; }
    .subpanel { border-top: 1px solid #e2e7e5; margin-top: 16px; padding-top: 16px; }
    .metrics { display: grid; grid-template-columns: repeat(auto-fit,minmax(150px,1fr)); gap: 12px; }
    .metric { border-left: 3px solid #28745e; padding: 8px 12px; background: #f7faf8; }
    .metric span { display: block; color: #64736e; font-size: 12px; }
    .metric strong { display: block; margin-top: 5px; font-size: 19px; overflow-wrap: anywhere; }
    table { width: 100%; border-collapse: collapse; font-size: 13px; }
    th,td { padding: 10px 8px; border-bottom: 1px solid #e2e7e5; text-align: left; vertical-align: top; }
    th { color: #5e6d68; font-weight: 600; white-space: nowrap; }
    td.actions { min-width: 280px; }
    input,select,button,textarea { min-height: 36px; border: 1px solid #bdc9c5; border-radius: 5px; padding: 7px 10px; font: inherit; }
    button { cursor: pointer; color: #fff; background: #28745e; border-color: #28745e; font-weight: 600; }
    button.secondary { color: #273a34; background: #fff; border-color: #9caaa5; }
    button.danger { background: #a8423d; border-color: #a8423d; }
    button:disabled { cursor: not-allowed; opacity: .45; }
    .form-grid { display: grid; grid-template-columns: repeat(auto-fit,minmax(160px,1fr)); gap: 12px; align-items: end; }
    .form-grid label { font-size: 12px; color: #56645f; }
    .form-grid input,.form-grid select { width: 100%; margin-top: 5px; }
    .form-actions { display: flex; gap: 8px; align-items: end; }
    .state { padding: 16px; color: #65736e; text-align: center; }
    .notice { border: 1px solid #a9cfbf; color: #195541; background: #edf8f3; border-radius: 5px; padding: 10px; margin-bottom: 12px; }
    .error { color: #9e2f2a; background: #fff1f0; border-color: #f0c6c2; }
    .status { font-weight: 600; }
    .preview-grid { display: grid; grid-template-columns: repeat(auto-fit,minmax(240px,1fr)); gap: 10px; }
    .chunk { background: #f7faf8; border-left: 3px solid #7a9f92; padding: 10px; white-space: pre-wrap; overflow-wrap: anywhere; }
    .meta { color: #67746f; font-size: 12px; overflow-wrap: anywhere; }
    video,img { display: block; width: min(100%,640px); max-height: 360px; object-fit: contain; background: #e8eeeb; }
    @media(max-width:760px) { header { padding: 9px 12px; } header label span { display:none; } header input { width: 120px; } .layout { grid-template-columns:1fr; } nav { display:flex; overflow:auto; border-right:0; border-bottom:1px solid #dbe2df; } nav a { white-space:nowrap; margin:0 3px; } main { padding:16px; } td.actions { min-width: 220px; } }
  </style>
</head>
<body data-section="__SECTION__">
<header><strong>积养家 AI 客服管理</strong><label><span>管理口令</span><input id="token" type="password" autocomplete="off" placeholder="仅保存在当前会话"></label></header>
<div class="layout">
  <nav>
    <a href="/admin/system" class="__ACTIVE_SYSTEM__">系统状态</a>
    <a href="/admin/knowledge" class="__ACTIVE_KNOWLEDGE__">知识库</a>
    <a href="/admin/avatar" class="__ACTIVE_AVATAR__">数字人形象</a>
    <a href="/admin/display" class="__ACTIVE_DISPLAY__">大屏配置</a>
  </nav>
  <main><h1>__TITLE__</h1><div id="notice"></div><div id="content" class="panel"><div class="state">正在加载...</div></div></main>
</div>
<script>
const section = document.body.dataset.section;
const tokenInput = document.querySelector('#token');
let currentDisplayProfiles = [];
let currentAssets = [];
let activeObjectUrl = null;
tokenInput.value = sessionStorage.getItem('adminToken') || '';
tokenInput.addEventListener('change', () => { sessionStorage.setItem('adminToken', tokenInput.value); load(); });
const headers = () => tokenInput.value ? {'X-Admin-Token': tokenInput.value} : {};
const escapeText = value => String(value ?? '').replace(/[&<>"']/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
const numberValue = (form, name) => Number(new FormData(form).get(name));
async function api(path, options={}) {
  options.headers = Object.assign({}, options.headers || {}, headers());
  const response = await fetch(path, options);
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(payload.detail?.message || payload.detail?.code || `HTTP ${response.status}`);
  return payload;
}
function setNotice(message, error=false) {
  document.querySelector('#notice').innerHTML = message ? `<div class="notice ${error ? 'error':''}">${escapeText(message)}</div>` : '';
}
function action(label, command, tone='', disabled=false) {
  return `<button type="button" class="${tone}" data-command="${command}" ${disabled ? 'disabled':''}>${escapeText(label)}</button>`;
}
async function load(message='') {
  setNotice(message);
  document.querySelector('#content').innerHTML = '<div class="state">正在加载...</div>';
  try {
    if (section === 'system') await loadSystem();
    if (section === 'knowledge') await loadKnowledge();
    if (section === 'avatar') await loadAvatar();
    if (section === 'display') await loadDisplay();
  } catch (error) {
    setNotice(error.message || error, true);
    document.querySelector('#content').innerHTML = '<div class="state">加载失败</div>';
  }
}
async function loadSystem() {
  const data = await api('/api/v1/admin/system/status');
  const p = data.providers;
  document.querySelector('#content').innerHTML = `<div class="toolbar">${action('刷新状态','system-refresh','secondary')}</div><div class="metrics">
    <div class="metric"><span>Gateway</span><strong>${escapeText(data.gateway.status)}</strong></div>
    <div class="metric"><span>ASR</span><strong>${escapeText(p.asr.ready ? 'ready':'blocked')}</strong></div>
    <div class="metric"><span>TTS</span><strong>${escapeText(p.tts.ready ? 'ready':'blocked')}</strong></div>
    <div class="metric"><span>LLM</span><strong>${escapeText(p.llm.ready ? 'ready':'blocked')}</strong></div>
    <div class="metric"><span>Embedding</span><strong>${escapeText(p.embedding.ready ? 'ready':'blocked')}</strong></div>
    <div class="metric"><span>Approved</span><strong>${data.knowledge.documents.approved}</strong></div>
    <div class="metric"><span>Draft</span><strong>${data.knowledge.documents.draft}</strong></div>
    <div class="metric"><span>FAISS vectors</span><strong>${data.knowledge.faiss.vectors}</strong></div>
    <div class="metric"><span>当前待机视频</span><strong>${escapeText(data.manifest.video?.version || '未发布')}</strong></div>
    <div class="metric"><span>Display Profile</span><strong>${escapeText(data.display_profile?.profile_name || '未设置')}</strong></div>
  </div><div class="subpanel meta">request_id: ${escapeText(data.request_id)}</div>`;
}
async function loadKnowledge() {
  const data = await api('/api/v1/admin/knowledge');
  const rows = data.runs.map(run => {
    const canApprove = ['parsed','preview','failed'].includes(run.status);
    const canPublish = run.status === 'approved';
    const canReject = !['published','rejected'].includes(run.status);
    return `<tr><td>${escapeText(run.document_title)}</td><td class="status">${escapeText(run.status)}</td><td>${run.chunk_count}</td><td>${run.vector_count}</td><td class="actions">${action('预览',`knowledge-preview:${run.run_id}`,'secondary')} ${action('通过',`knowledge-approve:${run.run_id}`,'secondary',!canApprove)} ${action('发布',`knowledge-publish:${run.run_id}`,'',!canPublish)} ${action('驳回',`knowledge-reject:${run.run_id}`,'danger',!canReject)}</td></tr>`;
  }).join('');
  document.querySelector('#content').innerHTML = `<div class="toolbar"><form id="knowledge-upload"><input type="file" name="file" accept=".pdf,.docx,.md,.txt" required><button>上传并解析</button></form><button type="button" class="secondary" data-command="knowledge-refresh">刷新</button></div>
    <form id="knowledge-test" class="toolbar"><input name="query" maxlength="500" placeholder="输入问题测试检索或完整问答" required><button name="mode" value="search">检索测试</button><button name="mode" value="dialogue" class="secondary">问答测试</button></form>
    <div id="knowledge-result" class="subpanel" hidden></div>
    <table><thead><tr><th>文件</th><th>状态</th><th>分块</th><th>向量</th><th>操作</th></tr></thead><tbody>${rows || '<tr><td colspan="5" class="state">暂无上传批次</td></tr>'}</tbody></table>`;
  document.querySelector('#knowledge-upload').addEventListener('submit', uploadKnowledge);
  document.querySelector('#knowledge-test').addEventListener('submit', testKnowledge);
}
async function uploadKnowledge(event) {
  event.preventDefault();
  try {
    const data = await api('/api/v1/admin/knowledge/upload',{method:'POST',body:new FormData(event.target)});
    await load(`上传并解析完成：${data.run.document_title}，状态 ${data.run.status}`);
  } catch (error) { setNotice(error.message || error,true); }
}
async function testKnowledge(event) {
  event.preventDefault();
  const mode = event.submitter?.value || 'search';
  const query = new FormData(event.target).get('query');
  const result = document.querySelector('#knowledge-result');
  result.hidden = false; result.innerHTML = '<div class="state">正在执行...</div>';
  try {
    const data = mode === 'search'
      ? await api('/api/v1/knowledge/search',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({query,top_k:3})})
      : await api('/api/v1/dialogue/text',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text:query,session_id:'admin-test'})});
    const matches = mode === 'search' ? data.matches : data.knowledge.matches;
    const summary = mode === 'search' ? `${data.status}，命中 ${matches.length} 条` : data.answer.text;
    result.innerHTML = `<h2>${mode === 'search' ? '检索结果':'问答结果'}</h2><p>${escapeText(summary)}</p><div class="preview-grid">${(matches || []).map(item=>`<div class="chunk"><strong>${escapeText(item.title)}</strong><br>${escapeText(item.excerpt || '')}<div class="meta">${escapeText(item.source?.uri || '')}</div></div>`).join('') || '<div class="state">没有命中来源</div>'}</div><p class="meta">request_id: ${escapeText(data.request_id)}</p>`;
  } catch (error) { result.innerHTML = `<div class="error notice">${escapeText(error.message || error)}</div>`; }
}
async function loadAvatar() {
  const data = await api('/api/v1/admin/avatar');
  const rows = data.assets.map(asset => {
    const canPublish = asset.status !== 'published';
    const canDelete = asset.status !== 'published';
    return `<tr><td>${escapeText(asset.name)}</td><td>${escapeText(asset.asset_type)}</td><td>${escapeText(asset.version)}</td><td class="status">${escapeText(asset.status)}</td><td>${escapeText(asset.sha256.slice(0,12))}...</td><td class="actions">${action('预览',`asset-preview:${asset.avatar_id}`,'secondary')} ${action('发布',`asset-publish:${asset.avatar_id}`,'',!canPublish)} ${action('回滚到此版本',`asset-rollback:${asset.avatar_id}`,'secondary',asset.status === 'published')} ${action('删除',`asset-delete:${asset.avatar_id}`,'danger',!canDelete)}</td></tr>`;
  }).join('');
  document.querySelector('#content').innerHTML = `<form id="asset-upload" class="toolbar"><input name="name" placeholder="素材名称" required><input name="version" placeholder="版本，如 2026.08.07" required><select name="asset_type"><option value="video">待机视频</option><option value="image">背景图片</option></select><input type="file" name="file" accept=".mp4,.jpg,.jpeg,.png" required><button>上传素材</button><button type="button" class="secondary" data-command="asset-refresh">刷新</button></form><div id="asset-preview" class="subpanel" hidden></div><table><thead><tr><th>名称</th><th>类型</th><th>版本</th><th>状态</th><th>SHA256</th><th>操作</th></tr></thead><tbody>${rows || '<tr><td colspan="6" class="state">暂无素材</td></tr>'}</tbody></table>`;
  document.querySelector('#asset-upload').addEventListener('submit', uploadAsset);
}
async function uploadAsset(event) {
  event.preventDefault();
  try {
    const data = await api('/api/v1/admin/avatar',{method:'POST',body:new FormData(event.target)});
    await load(`素材上传完成：${data.asset.name} ${data.asset.version}，状态 ${data.asset.status}`);
  } catch (error) { setNotice(error.message || error,true); }
}
async function previewAsset(id, type) {
  const response = await fetch(`/api/v1/admin/avatar/${id}/file`,{headers:headers()});
  if(!response.ok) throw new Error('素材预览失败');
  if (activeObjectUrl) URL.revokeObjectURL(activeObjectUrl);
  activeObjectUrl = URL.createObjectURL(await response.blob());
  const tag = type === 'video' ? `<video controls autoplay muted src="${activeObjectUrl}"></video>` : `<img src="${activeObjectUrl}" alt="素材预览">`;
  const target = document.querySelector('#asset-preview'); target.hidden = false; target.innerHTML = `<h2>素材预览</h2>${tag}`;
}
async function loadDisplay() {
  const [displayData,assetData] = await Promise.all([api('/api/v1/admin/display'),api('/api/v1/admin/avatar')]);
  currentDisplayProfiles = displayData.profiles;
  currentAssets = assetData.assets;
  const videos = currentAssets.filter(a=>a.asset_type==='video' && a.status==='published').map(a=>`<option value="${a.avatar_id}">${escapeText(a.name)} / ${escapeText(a.version)}</option>`).join('');
  const images = currentAssets.filter(a=>a.asset_type==='image' && a.status==='published').map(a=>`<option value="${a.avatar_id}">${escapeText(a.name)} / ${escapeText(a.version)}</option>`).join('');
  const rows = currentDisplayProfiles.map(p => `<tr><td>${escapeText(p.profile_name)}</td><td>${p.width_px}x${p.height_px}</td><td>${escapeText(p.orientation)}</td><td>${escapeText(p.scale_mode)}</td><td>${p.character_anchor_x}, ${p.character_anchor_y} / ${p.character_scale}</td><td>${p.subtitle_font_px}</td><td>${p.is_default ? '默认':''}</td><td class="actions">${action('编辑',`display-edit:${p.profile_id}`,'secondary')} ${action('设为默认',`display-default:${p.profile_id}`,'',p.is_default)}</td></tr>`).join('');
  document.querySelector('#content').innerHTML = `<form id="display-form"><input type="hidden" name="profile_id"><div class="form-grid">
    <label>配置名称<input name="profile_name" required></label><label>宽度<input name="width_px" type="number" min="320" max="7680" value="1080" required></label><label>高度<input name="height_px" type="number" min="320" max="7680" value="1920" required></label>
    <label>方向<select name="orientation"><option value="portrait">竖屏</option><option value="landscape">横屏</option></select></label><label>缩放方式<select name="scale_mode"><option value="fit">fit</option><option value="fill">fill</option><option value="crop">crop</option></select></label>
    <label>人物 X（0-1）<input name="character_anchor_x" type="number" min="0" max="1" step="0.01" value="0.5"></label><label>人物 Y（0-1）<input name="character_anchor_y" type="number" min="0" max="1" step="0.01" value="0.5"></label><label>人物缩放<input name="character_scale" type="number" min="0.1" max="5" step="0.05" value="1"></label>
    <label>字幕左安全区<input name="safe_left" type="number" min="0" max="0.45" step="0.01" value="0.08"></label><label>字幕右安全区<input name="safe_right" type="number" min="0" max="0.45" step="0.01" value="0.08"></label><label>字幕底部安全区<input name="safe_bottom" type="number" min="0" max="0.45" step="0.01" value="0.08"></label><label>字幕字号<input name="subtitle_font_px" type="number" min="12" max="240" value="36"></label>
    <label>按钮 X（0-1）<input name="button_x" type="number" min="0" max="1" step="0.01" value="0.5"></label><label>按钮 Y（0-1）<input name="button_y" type="number" min="0" max="1" step="0.01" value="0.88"></label>
    <label>待机视频<select name="avatar_id"><option value="">不绑定</option>${videos}</select></label><label>背景图片<select name="background_id"><option value="">不绑定</option>${images}</select></label>
    <div class="form-actions"><button id="display-save">新增配置</button><button type="button" class="secondary" data-command="display-reset">取消编辑</button></div>
  </div></form><hr><table><thead><tr><th>名称</th><th>分辨率</th><th>方向</th><th>缩放</th><th>人物</th><th>字幕</th><th>状态</th><th>操作</th></tr></thead><tbody>${rows || '<tr><td colspan="8" class="state">暂无配置</td></tr>'}</tbody></table>`;
  document.querySelector('#display-form').addEventListener('submit', saveDisplay);
}
function fillDisplayForm(profile) {
  const form = document.querySelector('#display-form');
  const values = {profile_id:profile.profile_id,profile_name:profile.profile_name,width_px:profile.width_px,height_px:profile.height_px,orientation:profile.orientation,scale_mode:profile.scale_mode,character_anchor_x:profile.character_anchor_x,character_anchor_y:profile.character_anchor_y,character_scale:profile.character_scale,safe_left:profile.subtitle_safe_area.left,safe_right:profile.subtitle_safe_area.right,safe_bottom:profile.subtitle_safe_area.bottom,subtitle_font_px:profile.subtitle_font_px,button_x:profile.button_positions.consult?.x ?? .5,button_y:profile.button_positions.consult?.y ?? .88,avatar_id:profile.avatar_id || '',background_id:profile.background_id || ''};
  Object.entries(values).forEach(([name,value])=>{ if(form.elements[name]) form.elements[name].value=value; });
  document.querySelector('#display-save').textContent='保存修改';
  form.scrollIntoView({behavior:'smooth',block:'start'});
}
async function saveDisplay(event) {
  event.preventDefault();
  const form=event.target; const f=new FormData(form); const profileId=f.get('profile_id');
  const body={profile_name:f.get('profile_name'),width_px:numberValue(form,'width_px'),height_px:numberValue(form,'height_px'),orientation:f.get('orientation'),scale_mode:f.get('scale_mode'),character_anchor_x:numberValue(form,'character_anchor_x'),character_anchor_y:numberValue(form,'character_anchor_y'),character_scale:numberValue(form,'character_scale'),subtitle_safe_area:{left:numberValue(form,'safe_left'),right:numberValue(form,'safe_right'),bottom:numberValue(form,'safe_bottom')},subtitle_font_px:numberValue(form,'subtitle_font_px'),button_positions:{consult:{x:numberValue(form,'button_x'),y:numberValue(form,'button_y')}},avatar_id:f.get('avatar_id') || null,background_id:f.get('background_id') || null,status:'active'};
  try {
    const data=await api(profileId ? `/api/v1/admin/display/${profileId}`:'/api/v1/admin/display',{method:profileId?'PUT':'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
    await load(`大屏配置已保存：${data.profile.profile_name}，request_id ${data.request_id}`);
  } catch(error) { setNotice(error.message || error,true); }
}
document.addEventListener('click', async event => {
  const button=event.target.closest('[data-command]'); if(!button || button.disabled) return;
  const command=button.dataset.command; const [verb,id]=command.split(':'); const [kind,op]=verb.split('-');
  try {
    button.disabled=true;
    if(kind==='system') { await load('系统状态已刷新'); return; }
    if(kind==='knowledge' && op==='refresh') { await load('知识库列表已刷新'); return; }
    if(kind==='knowledge' && ['preview','approve','publish','reject'].includes(op)) {
      const data=await api(`/api/v1/admin/knowledge/${id}/${op}`,{method:'POST'});
      if(op==='preview') {
        const target=document.querySelector('#knowledge-result'); target.hidden=false; target.innerHTML=`<h2>Chunk 预览</h2><div class="preview-grid">${data.preview.map(x=>`<div class="chunk"><strong>${escapeText(x.title)}</strong><br>${escapeText(x.excerpt)}<div class="meta">${escapeText(x.source)}</div></div>`).join('')}</div><p class="meta">request_id: ${escapeText(data.request_id)}</p>`;
        setNotice(`预览完成，共 ${data.preview.length} 个 chunk`); button.disabled=false; return;
      }
      await load(`${op==='approve'?'审核通过':op==='publish'?'发布完成':'已驳回'}：${data.run.document_title}，状态 ${data.run.status}`); return;
    }
    if(kind==='asset' && op==='refresh') { await load('素材列表已刷新'); return; }
    if(kind==='asset' && op==='preview') { await previewAsset(id,button.closest('tr').children[1].textContent); setNotice('素材预览已加载'); button.disabled=false; return; }
    if(kind==='asset' && ['publish','rollback','delete'].includes(op)) {
      if(op==='delete' && !confirm('确认删除这个未发布素材？')) { button.disabled=false; return; }
      const data=await api(`/api/v1/admin/avatar/${id}/${op}`,{method:op==='delete'?'DELETE':'POST'});
      await load(op==='delete' ? '未发布素材已删除' : `${op==='publish'?'素材已发布':'素材已回滚'}：${data.asset.name} ${data.asset.version}`); return;
    }
    if(kind==='display' && op==='edit') { fillDisplayForm(currentDisplayProfiles.find(p=>p.profile_id===id)); button.disabled=false; return; }
    if(kind==='display' && op==='reset') { await load('已取消编辑'); return; }
    if(kind==='display' && op==='default') { const data=await api(`/api/v1/admin/display/${id}/set-default`,{method:'POST'}); await load(`默认配置已切换：${data.profile.profile_name}`); return; }
  } catch(error) { setNotice(error.message || error,true); button.disabled=false; }
});
load();
</script>
</body></html>"""
