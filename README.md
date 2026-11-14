# 霍夫圆检测工具

一个带图形界面的霍夫圆检测小工具：导入图片、拖动参数、实时看红圈预览、导出标注图。仓库同时保留两张实拍图的验收参数与结果图，方便复现和评审。

## 功能

- 导入 JPG / JPEG / PNG 图片，按比例预览。
- 调节 `dp`、`minDist`、`param1`、`param2`、`minRadius`、`maxRadius` 六个参数并立即重新检测。
- 内置 `coins`、`cookie-plate` 两组验收预设；打开文件名含 `coin`、`cookie` 或 `plate` 的图片时自动套用。
- 一键导出原图分辨率的标注图。
- 无界面模式，便于一条命令复现验收结果、生成 README 图片。

## 环境

- Ubuntu 24.04（WSL 2 可用）
- Python 3.10+
- Tkinter（Ubuntu 上由系统包提供）

```bash
sudo apt install python3-tk
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

依赖：`opencv-python-headless`、`numpy`、`Pillow`。使用 headless 版 OpenCV 是因为界面由 Tkinter 负责，不依赖 OpenCV 自带的窗口系统。

## 启动

```bash
python3 app.py
```

操作顺序：

1. 点 **打开图片**，选择 `examples/coins.jpg` 或 `examples/cookie-plate.jpg`。
2. 确认 **预设** 自动切到对应值；也可以手动拖动滑块调参。
3. 状态栏显示当前圆数量和参数，画布实时更新红圈。
4. 点 **导出标注图**，选择保存路径，得到与原图同尺寸的标注图。

## 两张图的验收参数

| 图片 | 预设 | dp | minDist | param1 | param2 | minRadius | maxRadius | 期望 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `examples/coins.jpg` | `coins` | 1.2 | 120 | 120 | 100 | 150 | 220 | 2 个硬币外缘圆 |
| `examples/cookie-plate.jpg` | `cookie-plate` | 1.2 | 150 | 120 | 50 | 210 | 270 | 1 个盘沿圆 |

参数与 `hough.PRESETS` 保持一致，测试直接引用同一份预设，避免文档和代码漂移。

## 验收结果

硬币图：两枚硬币的外缘各检测到一个圆，半径约 179 / 180 像素。

![硬币检测结果](docs/coins-annotated.png)

饼干盘图：只检测到盘沿一个圆，盘内饼干未被误判，半径约 243 像素。

![饼干盘检测结果](docs/cookie-plate-annotated.png)

### 无界面复现

```bash
python3 app.py --headless --image examples/coins.jpg --preset coins --output /tmp/coins-annotated.png
python3 app.py --headless --image examples/cookie-plate.jpg --preset cookie-plate --output /tmp/cookie-plate-annotated.png
```

预期输出：

```
Detected 2 circle(s): [(567, 191, 179), (193, 193, 180)]
Detected 1 circle(s): [(265, 257, 243)]
```

坐标顺序可能随 OpenCV 版本略有不同，数量和半径区间应保持一致。

## 测试

```bash
python3 -m unittest discover -s tests -v
```

- `tests/test_hough.py`：两张图的检测数量、半径区间、圆心位置，以及标注不修改原图。
- `tests/test_gui.py`：在真实 Tk 窗口中加载硬币图，断言圆数量、状态栏和画布内容；无 `DISPLAY` 时自动跳过。

## OpenSpec 记录

变更记录在 `openspec/changes/add-hough-circle-tool/`：`proposal.md` 说明动机与能力边界，`specs/hough-circle-detection/spec.md` 是可验证的行为规格，`design.md` 记录技术取舍，`tasks.md` 保留带验证方式的任务进度，`acceptance.md` 保存本次验收的命令、输出与判定。评审通过后再归档并把规格合并进 `openspec/specs/`。

## 图片许可

两张实拍图来自 Wikimedia Commons，来源与署名见 [examples/SOURCES.md](examples/SOURCES.md)。
