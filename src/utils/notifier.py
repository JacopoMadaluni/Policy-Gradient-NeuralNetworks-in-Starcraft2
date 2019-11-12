
import threading
import time
class Notifier(threading.Thread):

    def __init__(self, condition, callback):
        print("Started notifier")
        super(Notifier, self).__init__()
        self.condition = condition
        self.callback  = callback
        

    def run(self):
        while True:
            ready = self.condition()
            if ready:
                print("Ready to notify")
                self.callback()
                break
            else:
                time.sleep(5)
        print("Killing notifier")        

