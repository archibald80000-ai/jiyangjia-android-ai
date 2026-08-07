# Pending inputs / 待补资料与当前阻塞

Updated: 2026-08-06

本文件只记录项目继续落地需要的人工作业、外部资料和未闭环项。禁止写入任何真实密钥值。

## P0 — 当前阻塞

### 1. 腾讯云真实 Provider 配置链

当前服务器代码已部署，Gateway/Nginx/Docker 健康，但真实对话仍被 Provider 凭据配置阻塞。

待完成：

- 在服务器安全位置 `/opt/jiyangjia-ai/secrets/.env.local` 配置并验证真实 Provider；
- Compose 必须实际加载该文件；
- 容器内只检查 configured/missing，不打印值；
- 完成 `/api/v1/readiness`、dialogue/text、dialogue/audio、audio fetch 一次完整验收；
- 不得把下游 Provider 失败误报成上传失败。

需要的配置类别：

- Doubao ASR；
- Doubao TTS；
- Doubao/Volcengine Ark LLM；
- Doubao/Ark Embedding；
- Provider selection；
- SQLite/FAISS 持久化路径。

### 2. Android 12 真机

尚未完成：

- APK 安装；
- USB 麦克风枚举/录音；
- 默认麦克风 fallback；
- 音响播放；
- USB 插拔恢复；
- 真实分辨率/横竖屏；
- 网络断开恢复；
- 重启恢复；
- 长时间运行。

这些属于 TASK-015，不应虚报完成。

## P1 — TASK-014A 管理后台所需资料

### 3. 正式知识资料

当前只有小范围、人工确认的 demo FAQ。正式知识库仍需要业务方整理并审核。

建议第一批只提供：

- 积养家品牌/门店简介；
- 产品与服务介绍；
- 天然食材介绍；
- 汤品介绍；
- 门店营业与咨询信息；
- 常见问题；
- 转人工规则；
- 明确禁止回答的医疗疗效、实时价格/库存/活动等内容。

原始目录 `E:\work\积养家` 默认只读，禁止自动全量扫描或上传。应由人工选择资料，通过新后台进入 draft -> review -> approved 流程。

### 4. 数字人待机素材

尚需人工确认/制作：

- 第一版数字人形象；
- 待机动作视频 MP4；
- 是否把背景直接合成到视频；
- 品牌 Logo/视觉规范；
- 素材使用权确认。

Phase 1 推荐 `composite_video`：人物 + 背景直接输出完整 MP4，避免透明视频兼容风险。

### 5. 大屏真实参数

后台将支持多 Display Profile，但 TASK-015 前仍需采集目标设备真实信息：

- 物理屏幕方向；
- Android 报告的像素宽高；
- DPI / density；
- 是否 1080p / 4K；
- 安全显示区域；
- USB 口与 USB Audio Class 能力；
- 内置/外接音响情况。

预设 Profile：1920x1080、3840x2160、1280x720、1080x1920，并允许自定义。

## P2 — 上线前再处理

- 正式域名与 HTTPS/TLS；
- Device token / 管理后台 ADMIN_TOKEN；
- 正式知识库备份与恢复；
- 素材版本回滚；
- 监控、告警、请求限流；
- 正式 release APK 签名；
- 门店连续 30 次真实问答与长稳测试。

## 明确延期

以下不属于 Phase 1 阻塞：

- LiveTalking；
- Wav2Lip；
- MuseTalk；
- WebRTC 实时数字人；
- GPU 推理；
- Dify / LangFlow / Flowise。
