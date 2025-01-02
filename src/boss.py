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
        for size in self.sizes:
            task = Task(identifier=f"(Job of size {size})", size=size)
            print(f"Task {task.identifier} created.")
            self.tasks_sent.append(task)
            self.task_queue.put(task)

    def run_get_result(self):
        print("Results in C++")
        results = []
        for _ in range(len(self.sizes)):
            task = self.result_queue.get()
            self.tasks_received.append(task)
            result = (
                f"Task {task.identifier} completed, " f"Time: {task.time:.5f} seconds"
            )
            results.append(result)
            print(result)

        with open("data/result_cpp.txt", "w") as file:
            file.write("Results in C++\n" + "\n".join(results) + "\n")

    def run_same_tasks_in_python(self):
        print("Results in Python")
        task_indices = []
        errors = []
        intersections = []

        results = []
        for i, task in enumerate(self.tasks_sent):
            task.work()
            result = (
                f"Task {task.identifier} completed, " f"Time: {task.time:.5f} seconds"
            )
            results.append(result)
            print(result)

            # Calculate error and check intersections
            task_indices.append(i)
            error = task.time - self.tasks_received[i].time
            errors.append(error)

            if task.size > self.big_problem:
                distance = task.size - self.big_problem
                intersections.append((i, error, distance))

        with open("data/result_py.txt", "w") as file:
            file.write("Results in Python\n" + "\n".join(results) + "\n")

        self._plot_errors(task_indices, errors, intersections)

    def _plot_errors(self, task_indices, errors, intersections):
        plt.figure(figsize=(10, 6))
        ax = plt.gca()

        # Plot error line
        ax.plot(
            task_indices, errors, label="Error (Python Time - C++ Time)", color="blue"
        )

        # Highlight intersections
        # Highlight intersections
        if intersections:
            max_distance = max(intersections, key=lambda x: x[2])[2]
            for index, error, distance in intersections:
                normalized_distance = min(distance / max_distance, 1)
                ax.scatter(
                    index, error, color=cm.Reds(normalized_distance), s=100, label=None
                )

        # Highlight points above y=0
        for i, error in enumerate(errors):
            if error > 0:
                ax.scatter(
                    i, error, color="green", label="Above y=0" if i == 0 else None
                )

        # Add color bar for intersections
        if intersections:
            sm = plt.cm.ScalarMappable(
                cmap="Reds", norm=plt.Normalize(vmin=0, vmax=max_distance)
            )
            sm.set_array([])
            cbar = plt.colorbar(sm, ax=ax, aspect=40)
            cbar.set_label(f"Distance from {self.big_problem} (Problem Size)")

        # Plot y=0 line
        ax.axhline(
            y=0,
            color="red",
            linestyle="--",
            linewidth=1,
            label="y=0 (Python faster below)",
        )

        # Final plot settings
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
