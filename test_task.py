import unittest
import numpy as np

from task import Task


class TestTask(unittest.TestCase):
    def test_work_fail(self):
        task = Task()
        np.testing.assert_allclose(np.dot(task.a, task.x), task.b)

    def test_work_pass(self):
        task = Task()
        task.work()

        np.testing.assert_allclose(np.dot(task.a, task.x), task.b)


if __name__ == "__main__":
    unittest.main()
