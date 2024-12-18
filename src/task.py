import time
import numpy as np
import json


class Task:
    def __init__(self, identifier=0, size=None):
        self.identifier = identifier
        # choosee the size of the problem
        self.size = size or np.random.randint(300, 3_000)
        # Generate the input of the problem
        self.a = np.random.rand(self.size, self.size)
        self.b = np.random.rand(self.size)
        # prepare room for the results
        self.x = np.zeros((self.size))
        self.time = 0.0

    def work(self):
        start = time.perf_counter()
        self.x = np.linalg.solve(self.a, self.b)
        self.time = time.perf_counter() - start

    def to_json(self):
        dict = {
            "a": self.a.tolist(),
            "b": self.b.tolist(),
            "x": self.x.tolist(),
            "identifier": self.identifier,
            "time": self.time,
            "size": self.size,
        }
        return json.dumps(dict)

    @staticmethod
    def from_json(json_dict: str):
        data = json.loads(json_dict)

        task = Task()
        task.x = np.array(data["x"])
        task.a = np.array(data["a"])
        task.b = np.array(data["b"])
        task.time = data["time"]
        task.size = data["size"]
        task.identifier = np.array(data["identifier"])
        return task

    def __eq__(self, other):
        if isinstance(other, Task):
            return (
                (other.x.tolist() == self.x.tolist())
                and (other.a.tolist() == self.a.tolist())
                and (other.b.tolist() == self.b.tolist())
                and (self.identifier == other.identifier)
                and (self.time == other.time)
                and (self.size == other.size)
            )

        return False
