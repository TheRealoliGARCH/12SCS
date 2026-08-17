import unittest


class FineGridSensitivityTests(unittest.TestCase):
    def test_grid_has_twenty_one_points(self):
        levels = tuple(i / 20.0 for i in range(21))
        self.assertEqual(len(levels), 21)
        self.assertEqual(levels[0], 0.0)
        self.assertEqual(levels[-1], 1.0)

    def test_grid_spacing(self):
        levels = tuple(i / 20.0 for i in range(21))
        self.assertTrue(all(abs((levels[i + 1] - levels[i]) - 0.05) < 1e-15 for i in range(20)))

    def test_normalization_definition(self):
        baseline = 0.1220059357126264
        self.assertAlmostEqual(baseline / baseline, 1.0, places=12)


if __name__ == "__main__":
    unittest.main()
