# 验收记录

记录时间：2026-11-14。环境：Ubuntu 24.04 / WSL 2，Python 3.12，OpenCV 4.6.0，NumPy 1.26.4，Pillow 10.2.0。

## 1. 自动测试

命令：

```bash
python3 -m unittest discover -s tests -v
```

实际结果：

```
test_loading_coins_shows_two_circles (test_gui.GuiSmokeTest.test_loading_coins_shows_two_circles) ... ok
test_annotation_keeps_source_image (test_hough.AcceptanceTest.test_annotation_keeps_source_image) ... ok
test_coins_marks_two_outer_edges (test_hough.AcceptanceTest.test_coins_marks_two_outer_edges) ... ok
test_plate_marks_one_rim (test_hough.AcceptanceTest.test_plate_marks_one_rim) ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.208s

OK
```

## 2. 硬币图

命令：

```bash
python3 app.py --headless --image examples/coins.jpg --preset coins --output docs/coins-annotated.png
```

实际输出：

```
Detected 2 circle(s): [(567, 191, 179), (193, 193, 180)]
```

判定：2 个圆，半径 179 / 180，落在 170–190 区间；两圆心水平相距 374 像素，均贴合硬币外缘。结果图见 `docs/coins-annotated.png`。

## 3. 饼干盘图

命令：

```bash
python3 app.py --headless --image examples/cookie-plate.jpg --preset cookie-plate --output docs/cookie-plate-annotated.png
```

实际输出：

```
Detected 1 circle(s): [(265, 257, 243)]
```

判定：1 个圆，半径 243，落在 228–258 区间；圆心 (265, 257) 与图片中心 (260, 260) 偏差 5.8 像素，贴合盘沿，盘内饼干未误判。结果图见 `docs/cookie-plate-annotated.png`。

## 4. 界面冒烟

`test_gui.py` 在有 `DISPLAY` 的真实 Tk 窗口中加载 `examples/coins.jpg` 并套用 `coins` 预设，断言：

- 检出的圆数量为 2；
- 状态栏包含「圆 2 个」；
- 预览画布至少包含一个图元。

无显示环境下该测试自动跳过，核心验收不受影响。
