"""霍夫圆检测工具：Tkinter 图形界面，附带无界面验收模式。"""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox, ttk

import hough


class HoughApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("霍夫圆检测")
        self.root.geometry("1100x720")

        self.image = None
        self.image_path: Path | None = None
        self.circles: list[tuple[int, int, int]] = []
        self.preview_photo: ImageTk.PhotoImage | None = None

        self.vars = {
            "dp": tk.DoubleVar(value=1.2),
            "min_dist": tk.IntVar(value=120),
            "param1": tk.IntVar(value=120),
            "param2": tk.IntVar(value=100),
            "min_radius": tk.IntVar(value=0),
            "max_radius": tk.IntVar(value=0),
        }

        self._build_toolbar()
        self._build_body()
        self.status = tk.StringVar(value="打开一张图片开始检测")
        ttk.Label(self.root, textvariable=self.status, anchor="w", padding=(8, 4)).pack(
            side=tk.BOTTOM, fill=tk.X
        )

    def _build_toolbar(self) -> None:
        bar = ttk.Frame(self.root, padding=8)
        bar.pack(side=tk.TOP, fill=tk.X)
        ttk.Button(bar, text="打开图片", command=self.open_image).pack(side=tk.LEFT)
        ttk.Button(bar, text="导出标注图", command=self.export_image).pack(
            side=tk.LEFT, padx=(8, 0)
        )
        ttk.Label(bar, text="预设").pack(side=tk.LEFT, padx=(16, 4))
        self.preset_box = ttk.Combobox(
            bar, values=list(hough.PRESETS), state="readonly", width=14
        )
        self.preset_box.set("default")
        self.preset_box.pack(side=tk.LEFT)
        self.preset_box.bind("<<ComboboxSelected>>", self.apply_preset)

    def _build_body(self) -> None:
        body = ttk.Frame(self.root)
        body.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        controls = ttk.Frame(body, width=320)
        controls.pack(side=tk.LEFT, fill=tk.Y)
        controls.pack_propagate(False)
        ttk.Label(controls, text="检测参数", font=("TkDefaultFont", 11, "bold")).pack(
            anchor="w", padx=8, pady=(8, 4)
        )
        self._add_scale(controls, "dp", "dp", 1.0, 2.0, 0.1)
        self._add_scale(controls, "min_dist", "minDist", 10, 400, 5)
        self._add_scale(controls, "param1", "param1", 10, 400, 5)
        self._add_scale(controls, "param2", "param2", 5, 200, 1)
        self._add_scale(controls, "min_radius", "minRadius", 0, 400, 5)
        self._add_scale(controls, "max_radius", "maxRadius", 0, 400, 5)

        self.canvas = tk.Canvas(body, bg="#202020", highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas.bind("<Configure>", lambda _event: self.redraw())

    def _add_scale(self, parent, key, label, from_, to, resolution) -> None:
        row = ttk.Frame(parent)
        row.pack(fill=tk.X, padx=8, pady=3)
        ttk.Label(row, text=label, width=10).pack(side=tk.LEFT)
        tk.Scale(
            row,
            variable=self.vars[key],
            from_=from_,
            to=to,
            resolution=resolution,
            orient=tk.HORIZONTAL,
            showvalue=True,
            command=lambda _value: self.detect(),
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)

    def current_params(self) -> hough.HoughParams:
        min_radius = int(self.vars["min_radius"].get())
        max_radius = int(self.vars["max_radius"].get())
        if max_radius and max_radius < min_radius:
            max_radius = min_radius
        return hough.HoughParams(
            dp=round(float(self.vars["dp"].get()), 1),
            min_dist=int(self.vars["min_dist"].get()),
            param1=int(self.vars["param1"].get()),
            param2=int(self.vars["param2"].get()),
            min_radius=min_radius,
            max_radius=max_radius,
        )

    def apply_preset(self, _event=None) -> None:
        params = hough.PRESETS[self.preset_box.get()]
        for key, value in (
            ("dp", params.dp),
            ("min_dist", params.min_dist),
            ("param1", params.param1),
            ("param2", params.param2),
            ("min_radius", params.min_radius),
            ("max_radius", params.max_radius),
        ):
            self.vars[key].set(value)
        self.detect()

    def open_image(self) -> None:
        path = filedialog.askopenfilename(
            title="选择图片",
            filetypes=[("图片", "*.jpg *.jpeg *.png"), ("所有文件", "*.*")],
        )
        if not path:
            return
        try:
            image = hough.load_image(path)
        except ValueError as exc:
            messagebox.showerror("无法打开图片", str(exc))
            return
        self.image = image
        self.image_path = Path(path)
        self.preset_box.set(self._preset_for(self.image_path.name))
        self.apply_preset()

    @staticmethod
    def _preset_for(name: str) -> str:
        lowered = name.lower()
        if "coin" in lowered:
            return "coins"
        if "cookie" in lowered or "plate" in lowered:
            return "cookie-plate"
        return "default"

    def detect(self) -> None:
        if self.image is None:
            return
        params = self.current_params()
        self.circles = hough.detect_circles(self.image, params)
        self.redraw()
        self.status.set(
            f"{self.image_path.name if self.image_path else ''} · "
            f"圆 {len(self.circles)} 个 · "
            f"dp={params.dp} minDist={params.min_dist} param1={params.param1} "
            f"param2={params.param2} r={params.min_radius}-{params.max_radius}"
        )

    def redraw(self) -> None:
        if self.image is None:
            return
        annotated = hough.annotate(self.image, self.circles)
        canvas_width = max(self.canvas.winfo_width(), 1)
        canvas_height = max(self.canvas.winfo_height(), 1)
        height, width = annotated.shape[:2]
        scale = min(canvas_width / width, canvas_height / height)
        size = (max(1, int(width * scale)), max(1, int(height * scale)))
        rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
        photo = Image.fromarray(rgb).resize(size, Image.LANCZOS)
        self.preview_photo = ImageTk.PhotoImage(photo)
        self.canvas.delete("all")
        self.canvas.create_image(
            canvas_width // 2,
            canvas_height // 2,
            image=self.preview_photo,
            anchor=tk.CENTER,
        )

    def export_image(self) -> None:
        if self.image is None:
            messagebox.showinfo("导出标注图", "先打开一张图片")
            return
        default_name = f"{self.image_path.stem}-annotated.png" if self.image_path else "annotated.png"
        path = filedialog.asksaveasfilename(
            title="导出标注图",
            defaultextension=".png",
            initialfile=default_name,
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")],
        )
        if not path:
            return
        annotated = hough.annotate(self.image, self.circles)
        if not cv2.imwrite(path, annotated):
            messagebox.showerror("导出失败", f"无法写入 {path}")
            return
        self.status.set(f"已导出 {path} · 圆 {len(self.circles)} 个")


def run_headless(image_path: str, preset: str, output: str | None) -> None:
    params = hough.PRESETS[preset]
    image = hough.load_image(image_path)
    circles = hough.detect_circles(image, params)
    if output:
        if not cv2.imwrite(output, hough.annotate(image, circles)):
            raise SystemExit(f"cannot write {output}")
    print(f"Detected {len(circles)} circle(s): {circles}")


def main() -> None:
    parser = argparse.ArgumentParser(description="霍夫圆检测工具")
    parser.add_argument("--headless", action="store_true", help="不启动界面，直接检测")
    parser.add_argument("--image", help="无界面模式下的输入图片")
    parser.add_argument(
        "--preset", choices=list(hough.PRESETS), default="default", help="验收预设"
    )
    parser.add_argument("--output", help="无界面模式下标注图的输出路径")
    args = parser.parse_args()

    if args.headless:
        if not args.image:
            parser.error("--headless requires --image")
        run_headless(args.image, args.preset, args.output)
        return

    root = tk.Tk()
    HoughApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
