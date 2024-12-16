from queueclient import QueueClient
import numpy as np


class Minion(QueueClient):
    def __init__(self):
        super().__init__()
        self.tasks = self.m.get_task_queue()
        self.results = self.m.get_result_queue()

    def run_queue(self):
        for _ in range(10):
            task = self.tasks.get()
            task.work()
            self.results.put(
                f"Task {task.identifier} done successfully with norm2(ax) = {np.linalg.norm(task.a @ task.x)}, norm2(b) = {np.linalg.norm(task.b)}"
            )


if __name__ == "__main__":
    minion = Minion()
    minion.run_queue()
