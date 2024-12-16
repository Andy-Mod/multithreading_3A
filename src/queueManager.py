from multiprocessing.managers import BaseManager
from queue import Queue

task_queue = Queue()
result_queue = Queue()


class QueueManager(BaseManager):
    pass


QueueManager.register("get_task_queue", callable=lambda: task_queue)
QueueManager.register("get_result_queue", callable=lambda: result_queue)

m = QueueManager(address=("127.0.0.1", 50000), authkey=b"abracadabra")
s = m.get_server()
s.serve_forever()
