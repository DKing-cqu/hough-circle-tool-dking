# Spec Delta

## Purpose

提供一个可交互的霍夫圆检测桌面工具：导入图片后调节参数即可看到标注结果并导出，同时用两张实拍图作为可复现的验收基线。

## ADDED Requirements

### Requirement: 图形界面导入与预览图片

工具 SHALL 提供图形界面，允许用户选择 JPG、JPEG、PNG 图片并在窗口中按比例预览。选中的图片 MUST 保持原文件不变。无法读取的图片 MUST 给出错误提示且不改变当前预览。

#### Scenario: 启动界面

- **WHEN** 用户执行启动命令
- **THEN** 出现包含“打开图片”“导出标注图”、参数滑块和预览区的窗口

#### Scenario: 导入实拍图

- **WHEN** 用户选择 `examples/coins.jpg`
- **THEN** 预览区显示完整图片，状态栏显示文件名、尺寸和当前检测到的圆数量

#### Scenario: 导入无法读取的文件

- **WHEN** 用户选择无法解码的图片
- **THEN** 弹出错误提示，当前预览和检测结果保持不变

### Requirement: 参数调节与实时检测

界面 SHALL 提供 dp、minDist、param1、param2、minRadius、maxRadius 六个参数控件，并在参数变化后重新执行检测、更新预览与圆数量。界面 SHALL 提供与 README 验收参数一致的预设选项。

#### Scenario: 修改参数

- **WHEN** 用户拖动任一参数滑块
- **THEN** 工具立即重新检测，预览中的红圈和状态栏的圆数量同步更新

#### Scenario: 应用验收预设

- **WHEN** 用户选择 `coins` 或 `cookie-plate` 预设
- **THEN** 六个参数被设置为该预设的值并立即重新检测

### Requirement: 导出标注图

工具 SHALL 允许用户把当前检测结果导出为图片文件。导出图 MUST 使用原图分辨率并画出所有检测到的圆，且 MUST NOT 修改内存中的原图。

#### Scenario: 导出硬币标注图

- **WHEN** 用户对 `coins.jpg` 以 `coins` 预设执行导出
- **THEN** 生成一张包含两个红色外缘圆的图片，尺寸与原图一致

#### Scenario: 未打开图片时导出

- **WHEN** 用户在没有打开图片时点击导出
- **THEN** 工具提示先打开图片，不产生文件

### Requirement: 两张实拍图的验收基线

仓库 SHALL 记录两张样例图各自的验收参数，并使按该参数运行时检测数量稳定。`examples/coins.jpg` MUST 检测到 2 个半径约 180 像素的硬币外缘圆；`examples/cookie-plate.jpg` MUST 检测到 1 个半径约 243 像素的盘沿圆。两张图的标注结果 MUST 作为图片保存在仓库中。

#### Scenario: 硬币图验收

- **WHEN** 以 `coins` 预设检测 `examples/coins.jpg`
- **THEN** 恰好得到 2 个圆，半径在 170 到 190 像素之间，两个圆心水平相距超过 300 像素

#### Scenario: 饼干盘图验收

- **WHEN** 以 `cookie-plate` 预设检测 `examples/cookie-plate.jpg`
- **THEN** 恰好得到 1 个圆，半径在 228 到 258 像素之间，圆心接近图片中心

#### Scenario: 无界面复现

- **WHEN** 用户按 README 的无界面命令运行两张图
- **THEN** 命令输出分别为 `Detected 2 circle(s)` 和 `Detected 1 circle(s)`，并生成标注图
