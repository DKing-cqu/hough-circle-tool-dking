"""两张实拍图的验收测试：硬币两个外缘、饼干盘一个盘沿。"""

import unittest
from pathlib import Path

import numpy as np

import hough

ROOT = Path(__file__).resolve().parent.parent
EXAMPLES = ROOT / "examples"


class AcceptanceTest(unittest.TestCase):
    def test_coins_marks_two_outer_edges(self) -> None:
        image = hough.load_image(EXAMPLES / "coins.jpg")

        circles = hough.detect_circles(image, hough.PRESETS["coins"])

        self.assertEqual(len(circles), 2, circles)
        left, right = sorted(circles, key=lambda circle: circle[0])
        for _x, _y, radius in (left, right):
            self.assertAlmostEqual(radius, 180, delta=10)
        self.assertGreater(right[0] - left[0], 300)

    def test_plate_marks_one_rim(self) -> None:
        image = hough.load_image(EXAMPLES / "cookie-plate.jpg")

        circles = hough.detect_circles(image, hough.PRESETS["cookie-plate"])

        self.assertEqual(len(circles), 1, circles)
        x, y, radius = circles[0]
        self.assertAlmostEqual(radius, 243, delta=15)
        self.assertLessEqual(abs(x - image.shape[1] / 2), 25)
        self.assertLessEqual(abs(y - image.shape[0] / 2), 25)

    def test_annotation_keeps_source_image(self) -> None:
        image = hough.load_image(EXAMPLES / "coins.jpg")
        before = image.copy()

        annotated = hough.annotate(image, [(100, 100, 50)])

        self.assertTrue(np.array_equal(image, before))
        self.assertFalse(np.array_equal(annotated, image))


if __name__ == "__main__":
    unittest.main()
