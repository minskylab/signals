import unittest
from api import dataframe_to_csv_file
import pandas as pd
import numpy as np
from loguru import logger


class ExportTest(unittest.TestCase):
    def test_dataframe_exporter(self):
        df = pd.DataFrame(np.random.randn(10, 3))
        logger.info(df.head())
        file = dataframe_to_csv_file(df)
        length_file = len(file.readlines())
        logger.info(length_file)
        self.assertNotEqual(length_file, 0, "your converter is bullshit")
        file.close()

    def test_dataframe_rebuild(self):
        n, m = 10, 3
        df = pd.DataFrame(np.random.randn(n, m))
        file = dataframe_to_csv_file(df)
        length_file = len(file.readlines())
        self.assertNotEqual(length_file, 0, "your converter is bullshit")
        logger.info(length_file)
        new_df = pd.read_csv(file.name)
        for i in range(m):
            for j in range(n):
                # each value with a minimal variance
                self.assertLessEqual(new_df[str(i)][j] - df[i][j], 1e-6, f"the converter have rebuild problems at ({i}, {j})")


if __name__ == '__main__':
    unittest.main()
