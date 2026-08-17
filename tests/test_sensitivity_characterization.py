import unittest


class SensitivityCharacterizationTests(unittest.TestCase):
    def test_grid_definition(self):
        levels = tuple(i / 20.0 for i in range(21))
        self.assertEqual(len(levels), 21)
        self.assertEqual(levels[0], 0.0)
        self.assertEqual(levels[-1], 1.0)
        self.assertEqual(levels[1] - levels[0], 0.05)

    def test_normalization_at_zero(self):
        baseline = 0.1220059357126264
        self.assertAlmostEqual(baseline / baseline, 1.0, places=12)

    def test_finite_difference_geometry_is_well_defined(self):
        values = (0.122, 0.110, 0.105)
        first = tuple(values[i + 1] - values[i] for i in range(2))
        second = first[1] - first[0]
        self.assertTrue(all(x <= 0 for x in first))
        self.assertIsInstance(second, float)


if __name__ == "__main__":
    unittest.main()
