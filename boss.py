from queueclient import QueueClient
from task import Task


class Boss(QueueClient):
    def __init__(self):
        super().__init__()

    def run_put_queue(self):
        for i in range(10):
            toDoTask = Task(identifier=f"Mangekyu {i}")
            print(f"The task {toDoTask.identifier} is created")
            self.task_queue.put(toDoTask)

    def run_get_result(self):
        for _ in range(10):
            print(self.result_queue.get())


if __name__ == "__main__":
    boss = Boss()

    boss.run_put_queue()
    boss.run_get_result()
