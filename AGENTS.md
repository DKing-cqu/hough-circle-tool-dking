# 项目约定

这是一个 Python 桌面小工具：Tkinter 界面 + OpenCV 霍夫圆检测。没有构建系统，入口是 `python3 app.py`。

## 结构

- `hough.py`：参数、检测、标注，GUI 与无界面模式共用；不要在这里引入 Tkinter。
- `app.py`：界面与 `--headless` 入口；参数控件必须映射到 `HoughParams`。
- `tests/`：`unittest`，GUI 测试在无 `DISPLAY` 时跳过。
- `docs/`：README 引用的标注结果图，由 `--headless` 命令生成，不要手工修图。
- `openspec/`：行为变更先提 change；不要手改 `openspec/specs/`。

## 命令

```bash
python3 app.py
python3 -m unittest discover -s tests -v
openspec validate add-hough-circle-tool --strict
```

## 约束

- 依赖只加 `requirements.txt` 中的 Python 包；Tkinter 走系统包。
- 验收参数以 `hough.PRESETS` 为唯一来源，README 参数表必须与它一致。
- 提交信息用 `<type>: <short description>`，type 取 `feat/fix/refactor/docs/chore/test/build`。
