import subprocess
import sys
import pickle
from queue import Queue, Empty
from threading import Thread


ON_POSIX = 'posix' in sys.builtin_module_names

def recieve():
    return pickle.load(sys.stdin.buffer)
    
def send(obj):
    pickle.dump(obj, sys.stdout.buffer)

class SubprocessWrapper:
    def __init__(self, module_file):
        self.module_file_name = module_file_name
        self.process = None
        self.in_q = Queue()
        self.out_q = Queue()
    
    def start(self, *args):
        self.process = subprocess.Popen([sys.executable, self.module.__file__, *args],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, 
                            close_fds=ON_POSIX)
        self.recever = Thread(target=self._enqueue_output, daemon=True)
        self.sender = Thread(target=self._enqueue_input, daemon=True)
        self.sender.start()
        self.recever.start()
        return self

    def send(self,obj):
        self.in_q.put(pickle.dumps(obj))
    
    def read(self, wait=False):
        try:  obj = self.out_q.get(wait) 
        except Empty:
            return None 
        else:
            return pickle.loads(obj)

    def _enqueue_output(self):
        for line in iter(self.process.stdout.readline, b''):
            self.out_q.put(line)
        self.process.stdout.close()

    def _enqueue_input(self):
        while self.process.poll() is None:
            self.process.stdin.write(self.in_q.get())
            self.process.stdin.flush()
        self.process.stdout.close()

