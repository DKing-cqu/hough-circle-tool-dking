# Tasks

## 1. 项目与检测核心

- [x] 1.1 建立项目结构（`hough.py`、`app.py`、`tests/`、`examples/`、`requirements.txt`、`.gitignore`）；验证：`find . -maxdepth 2 -type f` 能看到这些文件
- [x] 1.2 实现 `HoughParams`、`detect_circles`、`annotate` 和 `load_image`；验证：`python3 -c "import hough; print(len(hough.detect_circles(hough.load_image('examples/coins.jpg'), hough.PRESETS['coins'])))"` 输出 `2`

## 2. 图形界面

- [x] 2.1 实现 Tkinter 窗口：打开图片、六个参数滑块、预设下拉框、预览画布、状态栏、导出按钮；验证：`python3 app.py` 出现窗口，导入 `examples/coins.jpg` 后状态栏显示圆数量
- [x] 2.2 让文件名自动套用对应预设（`coin` → `coins`，`cookie`/`plate` → `cookie-plate`）；验证：导入两张样例图后滑块值分别等于预设参数

## 3. 验收基线与文档

- [x] 3.1 固定两张图的验收参数并写入 `PRESETS`；验证：`coins` 得到 2 个半径约 180 的圆，`cookie-plate` 得到 1 个半径约 243 的圆
- [x] 3.2 用无界面模式生成 `docs/coins-annotated.png` 与 `docs/cookie-plate-annotated.png`；验证：两张图能在 README 中正常显示且圈贴合目标边缘
- [x] 3.3 编写 README：启动方式、操作步骤、两张图各自的参数表和结果图、无界面复现命令；验证：按 README 命令执行，输出与文档一致

## 4. 测试与验收

- [x] 4.1 新增 `tests/test_hough.py` 覆盖两张图的检测数量、半径区间与标注不改原图；验证：`python3 -m unittest discover -s tests -v` 全部通过
- [x] 4.2 新增 `tests/test_gui.py` 在真实 Tk 窗口中加载硬币图并断言圆数量、状态栏与画布内容；验证：有 `DISPLAY` 时测试通过，无显示环境自动跳过
- [x] 4.3 记录验收实际输出与图片到 `acceptance.md`；验证：文件中的命令、输出与当前仓库一致

## Workflow follow-up

- 评审通过后归档该变更，并确认 `openspec/specs/hough-circle-detection/spec.md` 已由归档流程生成。
