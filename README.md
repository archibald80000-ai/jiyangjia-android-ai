# 积养家 Android 大屏 AI 数字人客服系统

> Repository: `jiyangjia-android-ai`
> Local workspace: `E:\work\ai-kefu\jiyangjia-ai`
> Target device: Android 12 大屏
> Future upstream: [lipku/LiveTalking](https://github.com/lipku/LiveTalking)

本仓库用于管理“门店 Android 大屏 AI 语音客服 / 数字人终端”的产品需求、系统架构、开发任务、Codex 执行规则、项目记忆和后续代码。当前第一阶段目标不是下载模型或搭建实时数字人，而是在 Android 12 大屏上交付“本地待机人物视频 + USB/默认麦克风 + Gateway + 豆包 ASR/TTS + LLM + 小范围 FAQ + 字幕”的最小可上线版本。

## 当前产品路线

```text
阶段 A：Android 12 大屏客户端
  横屏全屏、本地待机人物视频、配置入口、状态机、无网络 fallback

阶段 B：音频硬件
  USB/默认麦克风、录音、音响播放、权限、设备诊断

阶段 C：Gateway 与 Provider
  轻量 Gateway → 豆包 TTS → 豆包 ASR → LLM Provider → 请求日志和错误映射

阶段 D：小范围知识问答
  10～30 条已确认 FAQ，简单检索，禁止回答规则，转人工

阶段 E：闭环、部署与门店验收
  Android → Gateway → ASR/FAQ/LLM/TTS → 播放与字幕 → 腾讯云 → Android 真机

后续增强：LiveTalking / Wav2Lip / MuseTalk / WebRTC 数字人
```

## 两种运行模式

| 模式 | 说明 | GPU |
|---|---|---:|
| `idle_video_voice` | 本地待机人物视频持续播放，知识回答由语音播报并显示字幕 | 不需要 |
| `livetalking_webrtc` | 后续增强：LiveTalking 实时渲染数字人口型，通过 WebRTC 输出 | 需要兼容 GPU 节点 |

Phase 1 只做 `idle_video_voice`。`livetalking_webrtc` 保留接口和文档，等 Android + Gateway 语音 FAQ MVP 验收后再恢复。

## 已知基础条件

- Android 12 大屏设备，通过 APK 安装运行；不是 Windows 设备。
- 可外接 USB 麦克风，具体兼容性必须真机验证。
- 现有腾讯云服务器：8 核 CPU、4 GB 内存、10 Mbps 带宽、无 NVIDIA GPU。
- 腾讯云负责 API、模型转发、轻量知识、配置和日志；不承担实时数字人 GPU 推理。
- 原始积养家资料位于 `E:\work\积养家`，当前只读，不批量导入。
- 所有真实密钥只保存在本地 `.env.local` 或服务器密钥系统中，禁止提交 Git。

## 开始开发

Codex 或新开发者必须依次阅读：

1. [`CODEX_START_HERE.md`](CODEX_START_HERE.md)
2. [`AGENTS.md`](AGENTS.md)
3. [`MEMORY.md`](MEMORY.md)
4. [`PROJECT_STATE.md`](PROJECT_STATE.md)
5. [`docs/00_PRODUCT_REQUIREMENTS.md`](docs/00_PRODUCT_REQUIREMENTS.md)
6. [`docs/architecture/MVP_ARCHITECTURE.md`](docs/architecture/MVP_ARCHITECTURE.md)
7. [`docs/api/MVP_API_SPEC.md`](docs/api/MVP_API_SPEC.md)
8. [`docs/testing/MVP_ACCEPTANCE.md`](docs/testing/MVP_ACCEPTANCE.md)
9. [`tasks/README.md`](tasks/README.md)
10. 当前被授权的 `TASK-xxx` 文件

不得跳过环境审查、直接同时开发 Android、后端、模型和知识库。

## 首个开发任务

从 [`tasks/TASK-000_PROJECT_BOOTSTRAP.md`](tasks/TASK-000_PROJECT_BOOTSTRAP.md) 开始。每个任务独立分支、独立验证、独立报告；只有验收通过后才能把状态改为 `DONE`。

## 推荐本地初始化

```powershell
Set-Location "E:\work\ai-kefu\jiyangjia-ai"

git clone https://github.com/archibald80000-ai/jiyangjia-android-ai.git .
Copy-Item .env.example .env.local

# 检查开发环境
powershell -ExecutionPolicy Bypass -File .\scripts\check_prerequisites.ps1

# Phase 1 不需要下载 LiveTalking 模型资产；只在未来增强阶段恢复 LiveTalking 任务
```

## 仓库结构

```text
android-app/       Android 大屏客户端，后续由 Codex 实现
gateway/           轻量 API 网关、会话、日志与模型路由
integration/       LiveTalking、ASR、TTS、LLM 适配层
knowledge-test/    小范围测试知识，不是正式知识库
third_party/       上游项目说明；实际源码由脚本拉取并忽略提交
config/            示例配置和上游版本锁
assets/            待机视频、测试音频、Avatar 资产说明
docs/              产品、架构、接口、安全、部署、验收文档
tasks/             可独立交给 Codex 执行的任务包
memory/            长期事实、决策、状态和交接记忆
scripts/           Windows 初始化、检查、发布与任务管理脚本
tests/             跨模块测试与验收入口
```

## 开源与上游

本仓库使用 Apache-2.0 许可证。LiveTalking 仍由其原作者和许可证管理；本仓库不重新分发模型权重、人物素材、声音资产或真实业务资料。详见 [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) 与 [`docs/18_OPEN_SOURCE_COMPLIANCE.md`](docs/18_OPEN_SOURCE_COMPLIANCE.md)。

## 当前状态

仓库目前处于 **规划与工程骨架阶段**。没有宣称以下事项已经完成：

- Android APK 已构建并完成 USB 麦克风验证；
- 豆包收费接口已接入；
- 正式知识库已建立；
- 腾讯云生产环境已部署。
- LiveTalking 已在目标 GPU 上实时运行。

真实进度只以 [`PROJECT_STATE.md`](PROJECT_STATE.md)、任务文件和可复现测试证据为准。
