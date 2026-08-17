import unittest
from model.convergence_analysis import CAPABILITIES, STATES
from model.heterogeneous_scenario import build_scenario

class ActiveSetBreakpointTests(unittest.TestCase):
    def test_scenario_is_valid(self):
        feasibility,costs=build_scenario(STATES,CAPABILITIES)
        self.assertEqual((len(feasibility),len(feasibility[0])),(len(STATES),len(CAPABILITIES)))
        self.assertTrue(all(0.0 <= x <= 1.0 for r in feasibility for x in r))
        self.assertTrue(all(x > 0.0 for r in costs for x in r))
    def test_linear_cost_path_endpoints(self):
        _,costs=build_scenario(STATES,CAPABILITIES)
        homogeneous=tuple(tuple(1.0 for _ in CAPABILITIES) for _ in STATES)
        self.assertTrue(all(abs(x-1.0)<1e-12 for r in homogeneous for x in r))
        self.assertTrue(any(abs(x-1.0)>1e-12 for r in costs for x in r))

if __name__=='__main__': unittest.main()
