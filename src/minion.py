from queueclient import QueueClient
import numpy as np


class Minion(QueueClient):
    def __init__(self):
        super().__init__()

    def run_queue(self):
        for _ in range(10):
            task = self.task_queue.get()
            task.work()
            self.result_queue.put(
                f"Task {task.identifier} done successfully with norm2(ax) = {np.linalg.norm(task.a @ task.x)}, norm2(b) = {np.linalg.norm(task.b)}"
            )


if __name__ == "__main__":
    minion = Minion()
    minion.run_queue()
