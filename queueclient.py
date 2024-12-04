from multiprocessing.managers import BaseManager

class QueueManager(BaseManager): 
    pass

class QueueClient:
    def __init__(self):        
        QueueManager.register('get_task_queue')
        QueueManager.register('get_result_queue')

        self.m = QueueManager(address=('127.0.0.1', 50000), authkey=b'abracadabra')
        self.m.connect()