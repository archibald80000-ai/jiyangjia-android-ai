# Pending inputs / 待补资料

Updated: 2026-08-10

本文件只记录继续落地需要的人工作业、外部资料和未闭环项。禁止写入任何真实密钥值。

## 已解除阻塞

- TASK-014 腾讯云 Provider 配置链已完成并通过最终验收。
- 线上 Gateway 已包含 FFmpeg，Android WAV 和 MP3 上传均通过真实 ASR/RAG/LLM/TTS 链路。
- Provider 凭据不再是当前阻塞。
- `TASK-014A` 已入主线 `main`，本轮不再重复实现，仅记录与生产验收、真机资料和部署交接清单。
- 用户已确认 `E:\work\ai-kefu\资料库\人像背景.MOV` 的本项目使用权；本地已生成并发布 1080x1920 MP4/JPG，绑定最终 9:16 测试 Profile。原始 MOV 未修改，派生媒体不进入 Git。

## P0 - Android 12 真机

TASK-015 尚需真实设备完成：

- APK 安装；
- USB 麦克风枚举、录音与默认麦克风 fallback；
- 音响播放与 USB 插拔恢复；
- 真实分辨率、方向、DPI 和安全显示区；
- 网络断开/恢复；
- 重启恢复和长时间运行。

TASK-015 还必须同时具备：

- 可恢复出厂并配置 Fully Managed Device Owner 的确认窗口；
- 已批准 MP4/背景及 Profile 的可信 HTTPS 生产发布；
- 可信 HTTPS bootstrap 与 APK 地址（HTTP 已恢复为本站 308，HTTPS/SNI 仍在腾讯接入传播阶段）；
- 正式签名身份、双人保管/备份记录；
- 同一正式证书签名且 versionCode 单调递增的 N、N+1，以及上一稳定源码构建的 N+2 回滚包。

当前 `adb devices -l` 无设备，本地 SDK 也没有 emulator/system image；TASK-015 已签发 `NO-GO / BLOCKED`，不能用本地测试替代真机结论。

## P1 - TASK-014A 正式内容与生产部署

本地管理后台骨架、API、状态机和持久化已完成。以下业务输入与生产部署仍待人工确认。

### 正式知识资料

正式知识库 v2.1 已完成 TASK-020D 公开包和生产重导入：用户明确授权的 65 条宣传/员工学习知识位于 `knowledge-public/v2.1/`，线上为 41 approved、24 draft、65 个 2048 维真实向量，当前策略 80/80，draft 泄露 0。原始目录 `E:\work\积养家` 继续只读；未授权资料不得自动扫描或上传，后续新增或修改仍必须经过 `draft -> preview -> approve -> publish`。

TASK-020B 已完成本地绑定；TASK-020C 已把同一正式知识状态、指定 MOV 的兼容视频衍生版和 Profile 发布到生产服务器。当前待办不是重新上传内容，而是解除 TASK-014H 后做一次公网分享验收。

### 待机人物素材

- 第一版人物形象待机 MP4、JPG 背景和权属确认已由用户提供并完成本地发布验证；
- 生产服务器素材、manifest、Profile 和回滚备份已经完成；公网 HTTPS 分享仍待 TASK-014H 放行；
- Logo 和正式声音如后续使用，仍需单独确认权属。

Phase 1 推荐 `composite_video`，即人物和背景合成完整 MP4。

### Display Profile

后台预设 1920x1080、3840x2160、1280x720、1080x1920，并允许自定义。本地最终测试 Profile 已设为 1080x1920 portrait；仍需目标设备提供：

- 实际像素宽高、方向和 DPI；
- 字幕安全区、字号和按钮位置；
- 人物位置、缩放和素材绑定；
- USB Audio Class 与内置/外接音响信息。

## P2 - 上线前

- ICP 已由用户确认完成；仍需等待腾讯公网 HTTPS/SNI 接入传播完成；
- 传播完成后只重新执行一次公网 HTTPS、APK 浏览器下载和 Certbot renewal dry-run；
- Device token 和管理后台 `ADMIN_TOKEN`；
- 知识库、素材和 Display Profile 的备份恢复；
- 监控、告警、请求限流和成本保护；
- 正式 release APK 签名；
- 正式签名证书 SHA-256 与双份离线备份恢复演练；
- 门店连续问答和长稳测试。

## 明确延期

- LiveTalking；
- Wav2Lip；
- MuseTalk；
- WebRTC 实时数字人；
- GPU 推理；
- Dify、LangFlow、Flowise。
