from __future__ import annotations


def admin_page(section: str) -> str:
    titles = {
        "system": "系统状态",
        "knowledge": "知识库",
        "avatar": "数字人形象",
        "display": "大屏配置",
    }
    title = titles[section]
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{title} | 积养家 AI 客服</title>
  <style>
    :root {{ color-scheme: light; font-family: Inter, "Microsoft YaHei", sans-serif; color: #18201d; background: #f4f6f5; }}
    * {{ box-sizing: border-box; letter-spacing: 0; }}
    body {{ margin: 0; min-width: 320px; }}
    header {{ height: 58px; padding: 0 24px; background: #183b32; color: #fff; display: flex; align-items: center; justify-content: space-between; gap: 16px; }}
    header strong {{ font-size: 17px; }}
    header label {{ display: flex; align-items: center; gap: 8px; font-size: 13px; }}
    header input {{ width: 180px; background: #fff; border: 0; }}
    .layout {{ display: grid; grid-template-columns: 190px minmax(0,1fr); min-height: calc(100vh - 58px); }}
    nav {{ padding: 18px 12px; background: #fff; border-right: 1px solid #dbe2df; }}
    nav a {{ display: block; color: #34443e; text-decoration: none; padding: 11px 12px; border-radius: 6px; margin-bottom: 4px; }}
    nav a.active {{ color: #fff; background: #28745e; font-weight: 600; }}
    main {{ padding: 24px; overflow: hidden; }}
    h1 {{ margin: 0 0 20px; font-size: 24px; }}
    h2 {{ font-size: 16px; margin: 0 0 14px; }}
    .toolbar {{ display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 16px; align-items: end; }}
    .panel {{ background: #fff; border: 1px solid #dbe2df; border-radius: 6px; padding: 18px; margin-bottom: 16px; overflow: auto; }}
    .metrics {{ display: grid; grid-template-columns: repeat(auto-fit,minmax(150px,1fr)); gap: 12px; }}
    .metric {{ border-left: 3px solid #28745e; padding: 8px 12px; background: #f7faf8; }}
    .metric span {{ display: block; color: #64736e; font-size: 12px; }}
    .metric strong {{ display: block; margin-top: 5px; font-size: 19px; overflow-wrap: anywhere; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
    th,td {{ padding: 10px 8px; border-bottom: 1px solid #e2e7e5; text-align: left; vertical-align: top; }}
    th {{ color: #5e6d68; font-weight: 600; white-space: nowrap; }}
    input,select,button,textarea {{ min-height: 36px; border: 1px solid #bdc9c5; border-radius: 5px; padding: 7px 10px; font: inherit; }}
    button {{ cursor: pointer; color: #fff; background: #28745e; border-color: #28745e; font-weight: 600; }}
    button.secondary {{ color: #273a34; background: #fff; border-color: #9caaa5; }}
    button.danger {{ background: #a8423d; border-color: #a8423d; }}
    .form-grid {{ display: grid; grid-template-columns: repeat(auto-fit,minmax(170px,1fr)); gap: 10px; }}
    .form-grid label {{ font-size: 12px; color: #56645f; }}
    .form-grid input,.form-grid select {{ width: 100%; margin-top: 5px; }}
    .state {{ padding: 16px; color: #65736e; text-align: center; }}
    .error {{ color: #9e2f2a; background: #fff1f0; border: 1px solid #f0c6c2; border-radius: 5px; padding: 10px; margin-bottom: 12px; }}
    .status {{ font-weight: 600; }}
    video,img {{ display: block; max-width: 220px; max-height: 130px; object-fit: contain; background: #e8eeeb; }}
    @media(max-width:760px) {{ header {{ padding: 0 12px; }} header label span {{ display:none; }} header input {{ width: 120px; }} .layout {{ grid-template-columns:1fr; }} nav {{ display:flex; overflow:auto; border-right:0; border-bottom:1px solid #dbe2df; }} nav a {{ white-space:nowrap; margin:0 3px; }} main {{ padding:16px; }} }}
  </style>
</head>
<body data-section="{section}">
<header><strong>积养家 AI 客服管理</strong><label><span>管理口令</span><input id="token" type="password" autocomplete="off" placeholder="仅保存在当前会话"></label></header>
<div class="layout">
  <nav>
    <a href="/admin/system" class="{'active' if section == 'system' else ''}">系统状态</a>
    <a href="/admin/knowledge" class="{'active' if section == 'knowledge' else ''}">知识库</a>
    <a href="/admin/avatar" class="{'active' if section == 'avatar' else ''}">数字人形象</a>
    <a href="/admin/display" class="{'active' if section == 'display' else ''}">大屏配置</a>
  </nav>
  <main><h1>{title}</h1><div id="error"></div><div id="content" class="panel"><div class="state">正在加载...</div></div></main>
</div>
<script>
const section = document.body.dataset.section;
const tokenInput = document.querySelector('#token');
tokenInput.value = sessionStorage.getItem('adminToken') || '';
tokenInput.addEventListener('change', () => {{ sessionStorage.setItem('adminToken', tokenInput.value); load(); }});
const headers = () => tokenInput.value ? {{'X-Admin-Token': tokenInput.value}} : {{}};
const escapeText = value => String(value ?? '').replace(/[&<>"']/g, ch => ({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[ch]));
async function api(path, options={{}}) {{
  options.headers = Object.assign({{}}, options.headers || {{}}, headers());
  const response = await fetch(path, options);
  const payload = await response.json().catch(() => ({{}}));
  if (!response.ok) throw new Error(payload.detail?.message || payload.detail?.code || `HTTP ${{response.status}}`);
  return payload;
}}
function setError(error) {{ document.querySelector('#error').innerHTML = error ? `<div class="error">${{escapeText(error.message || error)}}</div>` : ''; }}
function action(label, command, tone='') {{ return `<button class="${{tone}}" data-command="${{command}}">${{escapeText(label)}}</button>`; }}
async function load() {{
  setError(); document.querySelector('#content').innerHTML = '<div class="state">正在加载...</div>';
  try {{
    if (section === 'system') await loadSystem();
    if (section === 'knowledge') await loadKnowledge();
    if (section === 'avatar') await loadAvatar();
    if (section === 'display') await loadDisplay();
  }} catch (error) {{ setError(error); document.querySelector('#content').innerHTML = '<div class="state">加载失败</div>'; }}
}}
async function loadSystem() {{
  const data = await api('/api/v1/admin/system/status');
  const p = data.providers;
  document.querySelector('#content').innerHTML = `<div class="metrics">
    <div class="metric"><span>Gateway</span><strong>${{escapeText(data.gateway.status)}}</strong></div>
    <div class="metric"><span>ASR</span><strong>${{escapeText(p.asr.ready ? 'ready':'blocked')}}</strong></div>
    <div class="metric"><span>TTS</span><strong>${{escapeText(p.tts.ready ? 'ready':'blocked')}}</strong></div>
    <div class="metric"><span>LLM</span><strong>${{escapeText(p.llm.ready ? 'ready':'blocked')}}</strong></div>
    <div class="metric"><span>Embedding</span><strong>${{escapeText(p.embedding.ready ? 'ready':'blocked')}}</strong></div>
    <div class="metric"><span>Approved</span><strong>${{data.knowledge.documents.approved}}</strong></div>
    <div class="metric"><span>FAISS vectors</span><strong>${{data.knowledge.faiss.vectors}}</strong></div>
    <div class="metric"><span>Display Profile</span><strong>${{escapeText(data.display_profile?.profile_name || '未设置')}}</strong></div>
  </div>`;
}}
async function loadKnowledge() {{
  const data = await api('/api/v1/admin/knowledge');
  const rows = data.runs.map(run => `<tr><td>${{escapeText(run.document_title)}}</td><td class="status">${{run.status}}</td><td>${{run.chunk_count}}</td><td>${{run.vector_count}}</td><td>${{action('预览',`knowledge-preview:${{run.run_id}}`,'secondary')}} ${{action('通过',`knowledge-approve:${{run.run_id}}`,'secondary')}} ${{action('发布',`knowledge-publish:${{run.run_id}}`)}} ${{action('驳回',`knowledge-reject:${{run.run_id}}`,'danger')}}</td></tr>`).join('');
  document.querySelector('#content').innerHTML = `<div class="toolbar"><form id="knowledge-upload"><input type="file" name="file" accept=".pdf,.docx,.md,.txt" required><button>上传并解析</button></form></div><table><thead><tr><th>文件</th><th>状态</th><th>分块</th><th>向量</th><th>操作</th></tr></thead><tbody>${{rows || '<tr><td colspan="5" class="state">暂无上传批次</td></tr>'}}</tbody></table>`;
  document.querySelector('#knowledge-upload').addEventListener('submit', uploadKnowledge);
}}
async function uploadKnowledge(event) {{ event.preventDefault(); await api('/api/v1/admin/knowledge/upload', {{method:'POST',body:new FormData(event.target)}}); await load(); }}
async function loadAvatar() {{
  const data = await api('/api/v1/admin/avatar');
  const rows = data.assets.map(asset => `<tr><td>${{escapeText(asset.name)}}</td><td>${{asset.asset_type}}</td><td>${{escapeText(asset.version)}}</td><td>${{asset.status}}</td><td>${{asset.sha256.slice(0,12)}}...</td><td>${{action('预览',`asset-preview:${{asset.avatar_id}}`,'secondary')}} ${{action('发布',`asset-publish:${{asset.avatar_id}}`)}} ${{action('回滚到此版本',`asset-rollback:${{asset.avatar_id}}`,'secondary')}} ${{action('删除',`asset-delete:${{asset.avatar_id}}`,'danger')}}</td></tr>`).join('');
  document.querySelector('#content').innerHTML = `<form id="asset-upload" class="toolbar"><input name="name" placeholder="素材名称" required><input name="version" placeholder="版本，如 2026.08.07" required><select name="asset_type"><option value="video">待机视频</option><option value="image">背景图片</option></select><input type="file" name="file" accept=".mp4,.jpg,.jpeg,.png" required><button>上传素材</button></form><div id="preview"></div><table><thead><tr><th>名称</th><th>类型</th><th>版本</th><th>状态</th><th>SHA256</th><th>操作</th></tr></thead><tbody>${{rows || '<tr><td colspan="6" class="state">暂无素材</td></tr>'}}</tbody></table>`;
  document.querySelector('#asset-upload').addEventListener('submit', uploadAsset);
}}
async function uploadAsset(event) {{ event.preventDefault(); await api('/api/v1/admin/avatar', {{method:'POST',body:new FormData(event.target)}}); await load(); }}
async function previewAsset(id, type) {{
  const response = await fetch(`/api/v1/admin/avatar/${{id}}/file`, {{headers:headers()}});
  if(!response.ok) throw new Error('素材预览失败');
  const url = URL.createObjectURL(await response.blob());
  const tag = type === 'video' ? `<video controls src="${{url}}"></video>` : `<img src="${{url}}" alt="素材预览">`;
  document.querySelector('#preview').innerHTML = tag;
}}
async function loadDisplay() {{
  const data = await api('/api/v1/admin/display');
  const rows = data.profiles.map(p => `<tr><td>${{escapeText(p.profile_name)}}</td><td>${{p.width_px}}x${{p.height_px}}</td><td>${{p.orientation}}</td><td>${{p.scale_mode}}</td><td>${{p.subtitle_font_px}}</td><td>${{p.is_default ? '默认':''}}</td><td>${{action('设为默认',`display-default:${{p.profile_id}}`)}}</td></tr>`).join('');
  document.querySelector('#content').innerHTML = `<form id="display-create" class="form-grid"><label>名称<input name="profile_name" required></label><label>宽度<input name="width_px" type="number" min="320" value="1920" required></label><label>高度<input name="height_px" type="number" min="320" value="1080" required></label><label>方向<select name="orientation"><option value="landscape">横屏</option><option value="portrait">竖屏</option></select></label><label>缩放<select name="scale_mode"><option value="fit">fit</option><option value="fill">fill</option><option value="crop">crop</option></select></label><label>字幕字号<input name="subtitle_font_px" type="number" min="12" value="52"></label><button>新增配置</button></form><hr><table><thead><tr><th>名称</th><th>分辨率</th><th>方向</th><th>缩放</th><th>字幕</th><th>状态</th><th>操作</th></tr></thead><tbody>${{rows}}</tbody></table>`;
  document.querySelector('#display-create').addEventListener('submit', createDisplay);
}}
async function createDisplay(event) {{ event.preventDefault(); const f=new FormData(event.target); const body={{profile_name:f.get('profile_name'),width_px:Number(f.get('width_px')),height_px:Number(f.get('height_px')),orientation:f.get('orientation'),scale_mode:f.get('scale_mode'),character_anchor_x:.5,character_anchor_y:.5,character_scale:1,subtitle_safe_area:{{left:.08,right:.08,bottom:.08}},subtitle_font_px:Number(f.get('subtitle_font_px')),button_positions:{{consult:{{x:.5,y:.88}}}},status:'active'}}; await api('/api/v1/admin/display',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify(body)}}); await load(); }}
document.addEventListener('click', async event => {{
  const command=event.target.dataset.command; if(!command) return;
  const [kind,op,id]=command.split(':');
  try {{
    if(kind==='knowledge') {{ const data=await api(`/api/v1/admin/knowledge/${{id}}/${{op}}`,{{method:'POST'}}); if(op==='preview') alert(data.preview.map(x=>x.title+'\\n'+x.excerpt).join('\\n\\n')); }}
    if(kind==='asset' && op==='preview') {{ await previewAsset(id,event.target.closest('tr').children[1].textContent); return; }}
    if(kind==='asset' && op!=='preview') await api(`/api/v1/admin/avatar/${{id}}/${{op}}`,{{method:op==='delete'?'DELETE':'POST'}});
    if(kind==='display') await api(`/api/v1/admin/display/${{id}}/set-default`,{{method:'POST'}});
    await load();
  }} catch(error) {{ setError(error); }}
}});
load();
</script>
</body></html>"""
