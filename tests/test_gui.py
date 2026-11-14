"""GUI 冒烟测试：在真实 Tk 窗口里加载图片、套预设并确认状态栏与画布。"""

import os
import unittest
from pathlib import Path

import tkinter as tk

import hough
from app import HoughApp

ROOT = Path(__file__).resolve().parent.parent


@unittest.skipUnless(os.environ.get("DISPLAY"), "requires an X display")
class GuiSmokeTest(unittest.TestCase):
    def test_loading_coins_shows_two_circles(self) -> None:
        try:
            root = tk.Tk()
        except tk.TclError as exc:
            self.skipTest(f"cannot open display: {exc}")
        self.addCleanup(root.destroy)
        root.geometry("1100x720")
        app = HoughApp(root)

        app.image = hough.load_image(ROOT / "examples" / "coins.jpg")
        app.image_path = ROOT / "examples" / "coins.jpg"
        app.preset_box.set("coins")
        app.apply_preset()
        root.update_idletasks()
        root.update()

        self.assertEqual(len(app.circles), 2)
        self.assertIn("圆 2 个", app.status.get())
        self.assertGreater(len(app.canvas.find_all()), 0)


if __name__ == "__main__":
    unittest.main()
