import unittest
from core.ontology_dag import resolve_prerequisites

class TestOntologyDAG(unittest.TestCase):
    def test_resolve_prerequisites_ml(self):
        # Suppose a candidate is missing Deep Learning
        missing = ["Deep Learning"]
        # And they already have Python and Linear Algebra, but missing Machine Learning and Statistics
        acquired = ["Python", "Linear Algebra"]
        
        ordered = resolve_prerequisites(missing, acquired)
        
        # Expected: Statistics -> Machine Learning -> Deep Learning
        # (Order of Statistics and Machine Learning might vary depending on DAG, 
        # but Machine Learning must be before Deep Learning and Statistics before Machine Learning)
        
        self.assertIn("Deep Learning", ordered)
        self.assertIn("Machine Learning", ordered)
        self.assertIn("Statistics", ordered)
        self.assertNotIn("Python", ordered)
        
        dl_index = ordered.index("Deep Learning")
        ml_index = ordered.index("Machine Learning")
        stat_index = ordered.index("Statistics")
        
        self.assertLess(ml_index, dl_index)
        self.assertLess(stat_index, ml_index)

if __name__ == '__main__':
    unittest.main()
