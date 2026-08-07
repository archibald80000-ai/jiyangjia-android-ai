# Pending inputs / 待补资料

Updated: 2026-08-07

本文件只记录继续落地需要的人工作业、外部资料和未闭环项。禁止写入任何真实密钥值。

## 已解除阻塞

- TASK-014 腾讯云 Provider 配置链已完成并通过最终验收。
- 线上 Gateway 已包含 FFmpeg，Android WAV 和 MP3 上传均通过真实 ASR/RAG/LLM/TTS 链路。
- Provider 凭据不再是当前阻塞。
- `TASK-014A` 已入主线 `main`，本轮不再重复实现，仅记录与生产验收、真机资料和部署交接清单。

## P0 - Android 12 真机

TASK-015 尚需真实设备完成：

- APK 安装；
- USB 麦克风枚举、录音与默认麦克风 fallback；
- 音响播放与 USB 插拔恢复；
- 真实分辨率、方向、DPI 和安全显示区；
- 网络断开/恢复；
- 重启恢复和长时间运行。

## P1 - TASK-014A 正式内容与生产部署

本地管理后台骨架、API、状态机和持久化已完成。以下业务输入与生产部署仍待人工确认。

### 正式知识资料

服务器当前仅保留 10 条受控 FAQ 为 `approved`。正式知识库仍需业务方人工选择并审核：

- 品牌和门店简介；
- 产品、服务、天然食材和汤品介绍；
- 营业和咨询信息；
- 常见问题与转人工规则；
- 医疗疗效、实时价格、库存和活动等禁止回答边界。

原始目录 `E:\work\积养家` 继续只读，禁止自动全量扫描或上传。新资料必须经过 `draft -> preview -> approve -> publish`。

### 待机人物素材

- 第一版人物形象和待机 MP4；
- JPG/PNG 背景；
- 人物、背景、Logo 和声音的使用权确认；
- 素材名称、版本、SHA-256 和发布日期。

Phase 1 推荐 `composite_video`，即人物和背景合成完整 MP4。

### Display Profile

后台预设 1920x1080、3840x2160、1280x720、1080x1920，并允许自定义。仍需目标设备提供：

- 实际像素宽高、方向和 DPI；
- 字幕安全区、字号和按钮位置；
- 人物位置、缩放和素材绑定；
- USB Audio Class 与内置/外接音响信息。

## P2 - 上线前

- 正式域名与 HTTPS/TLS；
- Device token 和管理后台 `ADMIN_TOKEN`；
- 知识库、素材和 Display Profile 的备份恢复；
- 监控、告警、请求限流和成本保护；
- 正式 release APK 签名；
- 门店连续问答和长稳测试。

## 明确延期

- LiveTalking；
- Wav2Lip；
- MuseTalk；
- WebRTC 实时数字人；
- GPU 推理；
- Dify、LangFlow、Flowise。
