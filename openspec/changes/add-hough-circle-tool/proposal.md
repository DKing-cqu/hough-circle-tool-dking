# Proposal

## Why

需要一个能现场调参、立刻看到霍夫圆检测结果的桌面工具：只看命令行输出无法判断圆是否贴合目标边缘。两张实拍图（硬币、饼干盘）还要作为可复现的验收基线，参数和结果必须留在仓库里。

## What Changes

- 新增一个 Tkinter 图形界面工具，支持导入 JPG/JPEG/PNG、调节霍夫圆参数、实时预览检测结果、导出标注图。
- 提供 `coins`、`cookie-plate` 两组验收预设：硬币图标出两个硬币外缘，饼干盘图标出一个盘沿。
- 提供无界面模式，用同一套参数生成 README 所需的标注图并输出检测数量，便于复现验收。
- README 记录启动方式、两张图各自的验收参数与结果图；OpenSpec 变更记录保留规格、任务进度和验收证据。

## Capabilities

### New Capabilities

- `hough-circle-detection`: 通过图形界面导入图片、调节霍夫圆参数、预览并导出检测标注，并对两张实拍图定义可复现的验收参数。

### Modified Capabilities

无。

## Impact

- 新增 Python 代码：检测核心、GUI 入口、测试。
- 新增依赖：OpenCV、NumPy、Pillow；Tkinter 由系统包提供。
- 新增仓库资产：两张样例图、两张标注结果图、OpenSpec 变更记录。
- 不引入构建系统、打包发布或 Web 服务。
