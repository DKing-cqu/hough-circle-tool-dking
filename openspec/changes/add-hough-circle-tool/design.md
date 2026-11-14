# Design

## Context

仓库从零开始，只有两张实拍图和图片许可说明。运行环境是 Ubuntu 24.04 / WSL 2，已有 Python 3.12、OpenCV 4.6、NumPy、Pillow 和 Tkinter。规格见 `specs/hough-circle-detection/spec.md`。

## Goals / Non-Goals

**Goals:**

- 用最少的依赖做出可交互的桌面工具：导入、调参、预览、导出。
- 检测逻辑与界面分离，使验收可以脱离 GUI 自动执行。
- 两张图的验收参数成为仓库中的合同，README、测试、预设三处一致。

**Non-Goals:**

- 不做圆检测算法创新，直接使用 `cv2.HoughCircles`。
- 不引入 PyQt、Web 前端、打包安装包或 CI。
- 不处理视频流、相机或批量目录。

## Decisions

1. **GUI 选 Tkinter。** Python 标准库自带，WSLg 下已验证可开窗；预览用 `Canvas` + Pillow 缩放。相比 PyQt 少一个重依赖，符合“一个训练工具”的规模。
2. **检测核心独立成 `hough.py`。** GUI、无界面验收、测试共用 `HoughParams` / `detect_circles` / `annotate`，避免把算法塞进事件回调，测试不需要模拟点击。
3. **参数以不可变 dataclass 表达。** 预设、滑块、测试都构造同一个 `HoughParams`，`to_cv_args()` 统一映射到 OpenCV 参数名，减少三处手写字典的漂移。
4. **用半径区间排除干扰圆。** 硬币图限制 150–220 像素，避开硬币内部的花环与头像细节；饼干盘图限制 210–270 像素，避开盘内饼干（半径均小于 190）。这比继续提高 `param2` 更稳定。
5. **提供 `--headless` 模式。** README 的标注图由同一预设生成，评审可一条命令复现检测数量，不必依赖人工截图。
6. **不做多线程。** 两张图分别为 760×385 和 520×520，一次检测远低于人眼可感知的卡顿阈值；引入线程只会增加状态同步成本。

## Risks / Trade-offs

- [OpenCV 版本差异导致同一 `param2` 检出数量变化] → 测试断言数量与半径区间而非精确坐标；README 固定依赖大版本范围。
- [滑块拖动过频导致重复计算] → 当前图片尺寸小，直接同步重算；若将来支持大图再加防抖。
- [Tkinter 在无显示环境不可用] → GUI 冒烟测试检测 `DISPLAY`，缺失时跳过；核心验收不依赖 GUI。
- [预设只覆盖两张样例，换图仍需手动调参] → 这是工具定位；README 明确说明预设是验收基线，不是通用最优值。
