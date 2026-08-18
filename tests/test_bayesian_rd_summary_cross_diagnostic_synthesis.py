import csv
import subprocess
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class CrossDiagnosticSynthesisTests(unittest.TestCase):
    def test_contract_and_reproducibility(self):
        scripts = [
            'results/run_rd_summary_bootstrap.py',
            'results/run_bayesian_rd_summary_hierarchical_pooling.py',
            'results/run_bayesian_rd_summary_hierarchical_sensitivity.py',
            'results/run_bayesian_rd_summary_hierarchical_ppc.py',
            'results/run_bayesian_rd_summary_hierarchical_leave_one_out.py',
            'results/run_bayesian_rd_summary_hierarchical_influence.py',
            'results/run_bayesian_rd_summary_cross_diagnostic_synthesis.py',
        ]
        for script in scripts:
            subprocess.run([sys.executable, script], cwd=ROOT, check=True)
        path = ROOT / 'results/bayesian_rd_summary_cross_diagnostic_synthesis_v1.csv'
        first = path.read_bytes()
        subprocess.run([sys.executable, scripts[-1]], cwd=ROOT, check=True)
        self.assertEqual(first, path.read_bytes())
        rows = list(csv.DictReader(path.open(encoding='utf-8')))
        self.assertEqual(len(rows), 14)
        self.assertEqual({r['diagnostic_layer'] for r in rows}, {'full_sample','hyperprior_sensitivity','leave_one_out','posterior_predictive_check'})
        for r in rows:
            self.assertEqual(r['analysis'], 'bayesian_rd_summary_cross_diagnostic_synthesis')
            float(r['value'])
            self.assertEqual(r['source_type'], 'reported_estimate_and_standard_error')
            self.assertEqual(r['inference_level'], 'summary_data_cross_diagnostic_synthesis')


if __name__ == '__main__':
    unittest.main()
