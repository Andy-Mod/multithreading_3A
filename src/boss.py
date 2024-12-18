from queueclient import QueueClient
from task import Task
import matplotlib.pyplot as plt


class Boss(QueueClient):
    def __init__(self):
        super().__init__()
        self.number_of_tasks = 10
        self.tasks_sent = []
        self.tasks_received = []
        self.errors = []

    def run_put_queue(self):
        for i in range(self.number_of_tasks):
            to_do_task = Task(identifier=f"Mangekyu {i}")
            print(f"The task {to_do_task.identifier} is created")
            self.tasks_sent.append(to_do_task)
            self.task_queue.put(to_do_task)

    def run_get_result(self):
        print("Results in C++")
        for _ in range(self.number_of_tasks):
            task = self.result_queue.get()
            self.tasks_received.append(task)
            print(
                f"The task {task.identifier} is done. Problem size :{task.size} Time taken: {task.time} seconds"
            )

    def run_same_tasks_in_python(self):
        print("Results in Python")
        for i, task in enumerate(self.tasks_sent):
            task.work()
            print(
                f"The task {task.identifier} is done. Problem size:  Time taken: {task.time} seconds"
            )

            self.errors.append(task.time - self.tasks_received[i].time)

        plt.plot(self.errors)
        plt.axhline(y=0, color="green", linestyle="--", linewidth=2)
        plt.title("Error Plot")
        plt.xlabel("Task Index")
        plt.ylabel("Error pyhton_time - c++_time")
        plt.show()


if __name__ == "__main__":
    boss = Boss()

    boss.run_put_queue()
    boss.run_get_result()
    boss.run_same_tasks_in_python()
