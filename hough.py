"""霍夫圆检测核心：参数、检测与标注。GUI 与无界面验收共用。"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np


@dataclass(frozen=True)
class HoughParams:
    """一次检测的全部可调参数，对应 OpenCV HoughCircles 的同名参数。"""

    dp: float = 1.2
    min_dist: int = 120
    param1: int = 120
    param2: int = 100
    min_radius: int = 0
    max_radius: int = 0

    def to_cv_args(self) -> dict:
        return {
            "dp": self.dp,
            "minDist": self.min_dist,
            "param1": self.param1,
            "param2": self.param2,
            "minRadius": self.min_radius,
            "maxRadius": self.max_radius,
        }


# 两张实拍图的验收参数，README 和测试都以这里为准。
PRESETS: dict[str, HoughParams] = {
    "default": HoughParams(),
    "coins": HoughParams(min_dist=120, param2=100, min_radius=150, max_radius=220),
    "cookie-plate": HoughParams(min_dist=150, param2=50, min_radius=210, max_radius=270),
}


def load_image(path: str | Path) -> np.ndarray:
    """以 BGR 读取图片；读不到时抛出带路径的 ValueError。"""
    image = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"cannot read image: {path}")
    return image


def detect_circles(image: np.ndarray, params: HoughParams) -> list[tuple[int, int, int]]:
    """返回按 OpenCV 结果顺序排列的 (x, y, radius) 列表。"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    found = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, **params.to_cv_args())
    if found is None:
        return []
    return [tuple(int(value) for value in circle) for circle in np.round(found[0])]


def annotate(
    image: np.ndarray,
    circles: list[tuple[int, int, int]],
    color: tuple[int, int, int] = (0, 0, 255),
    thickness: int = 3,
) -> np.ndarray:
    """在副本上画出圆和圆心，原图保持不变。"""
    annotated = image.copy()
    for x, y, radius in circles:
        cv2.circle(annotated, (x, y), radius, color, thickness)
        cv2.circle(annotated, (x, y), 2, (0, 255, 0), thickness)
    return annotated
