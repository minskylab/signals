import pandas as pd
from analytics.semantic.processor import SemanticProcessor
import unittest

def prepare_data():
    tweets = pd.read_csv('tests/mini_df.csv')
    return tweets

class TestSemanticAnalytics(unittest.TestCase):
    def test_semantic_analysis(self):
        db = None
        tweets = prepare_data()
        assert isinstance(tweets, pd.DataFrame) == True
        result = SemanticProcessor(db).set_data(tweets).preprocess().measure_coherence().retrieve_topics()
        assert result != None
        assert len(result) == 8
        print('result', result)

if __name__ == '__main__':
    unittest.main()
