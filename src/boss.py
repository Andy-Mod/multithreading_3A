from queueclient import QueueClient
from task import Task
import matplotlib.pyplot as plt
import matplotlib.cm as cm


class Boss(QueueClient):
    def __init__(self):
        super().__init__()
        self.number_of_tasks = 10
        self.tasks_sent = []
        self.tasks_received = []
        self.errors = []
        self.big_problem = 800
        self.sizes = [4990, 6900, 4200, 100, 1000, 10, 2989, 3080, 3398, 1162, 761]

    def run_put_queue(self):
        for i in self.sizes:
            to_do_task = Task(identifier=f"Mangekyu {i}", size=i)
            print(f"The task {to_do_task.identifier} is created")
            self.tasks_sent.append(to_do_task)
            self.task_queue.put(to_do_task)

    def run_get_result(self):
        print("Results in C++")
        for _ in range(len(self.sizes)):
            task = self.result_queue.get()
            self.tasks_received.append(task)
            print(
                f"The task {task.identifier} is done. Problem size: {task.size} Time taken: {task.time} seconds"
            )

    def run_same_tasks_in_python(self):
        print("Results in Python")
        task_indices = []
        errors = []
        intersections = []

        for i, task in enumerate(self.tasks_sent):
            task.work()
            print(
                f"The task {task.identifier} is done. Problem size: {task.size} Time taken: {task.time} seconds"
            )

            task_indices.append(i)
            error = task.time - self.tasks_received[i].time
            errors.append(error)

            if task.size > self.big_problem:
                distance = task.size - self.big_problem
                intersections.append((i, error, distance))

        plt.figure(figsize=(10, 6))
        ax = plt.gca()

        ax.plot(
            task_indices, errors, label="Error (Python Time - C++ Time)", color="blue"
        )

        for index, error, distance in intersections:
            normalized_distance = min(
                distance / max(intersections, key=lambda x: x[2])[2], 1
            )
            color = cm.Reds(normalized_distance)
            ax.scatter(
                index,
                error,
                color=color,
                label=f"Problem Size over {self.big_problem}"
                if index == intersections[0][0]
                else "",
            )

        for i, error in enumerate(errors):
            if error > 0:
                ax.scatter(
                    i,
                    error,
                    color="green",
                    label="Above y=0"
                    if i == next(idx for idx, val in enumerate(errors) if val > 0)
                    else "",
                )

        sm = plt.cm.ScalarMappable(
            cmap="Reds",
            norm=plt.Normalize(vmin=0, vmax=max(intersections, key=lambda x: x[2])[2]),
        )
        sm.set_array([])
        cbar = plt.colorbar(sm, ax=ax, aspect=30)
        cbar.set_label(f"Distance from {self.big_problem} (Problem Size)")

        ax.axhline(
            y=0,
            color="red",
            linestyle="--",
            linewidth=1,
            label="Under This line the task is faster in Python",
        )
        ax.set_title("Error Plot with Problem Size and Highlighted Points")
        ax.set_xlabel("Task Index")
        ax.set_ylabel("Error (Python Time - C++ Time)")
        ax.legend()
        ax.grid()
        plt.show()


if __name__ == "__main__":
    boss = Boss()

    boss.run_put_queue()
    boss.run_get_result()
    boss.run_same_tasks_in_python()
