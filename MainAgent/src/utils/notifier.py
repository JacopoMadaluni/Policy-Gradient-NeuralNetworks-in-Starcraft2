
import threading
import time
class Notifier(threading.Thread):

    """
    Notifier object.
    A Notifier runs in the background.
    When the condition is met, the callback is executed.
    The Notifier is killed after the callback executes
    """
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
                time.sleep(2)
        print("Killing notifier")        

