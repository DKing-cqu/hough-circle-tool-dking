# Proposal

## Why

当前工具只能对单张图片做霍夫圆检测，接手人若要验证检测参数在一段连续画面中的稳定性，只能逐张导出图片。需要在不改动图片模式的前提下，把同一套检测核心接到视频输入上，并给出可复现的输出约定。

## What Changes

- 新增本地视频输入路径：逐帧解码后复用现有 `hough.detect_circles` 与 `HoughParams`，参数来源仍是 `hough.PRESETS`。
- 新增两类输出：带圆标注的视频，以及逐帧 CSV（帧号、时间、圆数量、圆心与半径）。
- 新增命令行视频模式（`--video`、`--output-video`、`--csv`），第一版不提供 GUI 视频入口。
- 明确范围外：相机实时流、多路视频、GPU 加速、视频内目标跟踪与去重。
- README 增加视频模式的启动与验收命令，OpenSpec 记录实现任务与验收口径。

## Capabilities

### New Capabilities

- `video-circle-detection`: 读取本地视频并逐帧执行霍夫圆检测，输出标注视频与逐帧 CSV，保证同一帧、同一参数下与图片模式的检测结果一致。

### Modified Capabilities

无。图片模式的行为与参数来源不变。

## Impact

- 代码：新增视频读取、写出与 CSV 模块，扩展命令行入口；`hough.py` 的检测语义不变。
- 依赖：继续使用 `opencv-python-headless`、`numpy`，不新增第三方包。
- 资产：仓库需要一段可公开使用的短视频样例，或在 README 说明获取方式；样例许可需在 `examples/SOURCES.md` 登记。
- 风险：视频编解码能力取决于 OpenCV 构建，`mp4v` 写出需在目标环境验证；逐帧检测耗时随分辨率线性增长，第一版不承诺实时处理。
