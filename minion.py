from queueclient import QueueClient
import numpy as np

class Minion:
    
    def __init__(self, QueueClient):
        
        self.tasks = QueueClient.m.get_task_queue()
        self.results = QueueClient.m.get_result_queue()
        
    def run_queue(self):
        for _ in range(10):
            task = self.tasks.get()
            task.work()
            self.results.put(f"Task {task.identifier} done successfully with norm2(ax) = {np.linalg.norm(task.a @ task.x)}, norm2(b) = {np.linalg.norm(task.b)}")

if __name__ == '__main__':

    minion = Minion(QueueClient())
    minion.run_queue()
