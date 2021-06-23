import subprocess
import sys
import pickle
from queue import Queue, Empty
from threading import Thread

from struct import Struct

ON_POSIX = 'posix' in sys.builtin_module_names
HEADER = Struct("!L")



def send(obj, file=sys.stdout.buffer):
    """Send a pickled message over the given channel."""
    payload = pickle.dumps(obj, -1)
    file.write(HEADER.pack(len(payload)))
    file.write(payload)
    file.flush()

def recieve(file=sys.stdin.buffer):
    """Receive a pickled message over the given channel.
    
    Returns:
        object: A deserialised object from the file buffer.
    """
    header = read_file(file, HEADER.size)
    payload = read_file(file, *HEADER.unpack(header))
    return pickle.loads(payload)

def read_file(file, size):
    """Read a fixed size buffer from the file.
    
    Returns:
        [Byte]: bytes from file buffer.  
    """
    parts = []
    while size > 0:
        part = file.read(size)
        if not part:
            raise EOFError
        parts.append(part)
        size -= len(part)
    return b''.join(parts)



class SubprocessWrapper:
    """Encapsulates subproccess to allow for easier communication between parent and child processes. 
    
        Args:
        module_file (String): A path like for a python script to run as a sub proccess.
    """
    def __init__(self, module_file):
        self.module_file_name = module_file
        self.process = None
        self.in_q = Queue()
        self.out_q = Queue()
    
    def start(self, *args):
        """Starts the threads and subproccess

        Returns:
            SubprocessWrapper: returns self
        """
        print(f"Starting: {self.module_file_name}{args}")
        self.process = subprocess.Popen([sys.executable, self.module_file_name, *args],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, 
                            close_fds=ON_POSIX)
        self.recever = Thread(target=self._enqueue_output, daemon=True)
        self.sender = Thread(target=self._enqueue_input, daemon=True)
        self.sender.start()
        self.recever.start()
        return self

    def send(self,obj):
        """Sends an object to the child process.

        Args:
            obj (object): the object to send to the child process
        """
        self.in_q.put(obj)
    
    def read(self, wait=False):
        """Reads from the child process

        Args:
            wait (bool, optional): Should this block the thread. Defaults to False.

        Raises:
            e: pass through exceptions from child processes.

        Returns:
            obj (object): the object the child process has sent.
        """
        try:  obj = self.out_q.get(wait) 
        except Empty:
            return None 
        else:
            if isinstance(obj, Exception):
                raise obj
            return obj

    def _enqueue_output(self):
        """while the child process is running, it will wait for a message and add it to the output enqueue for the main thread to pick up. 
        """
        try:
            while self.process.poll() is None:
                self.out_q.put(recieve(self.process.stdout))
        except Exception as e:
            self.out_q.put_nowait(e)
        self.process.stdout.close()

    def _enqueue_input(self):
        """while the child process is running, it will wait for a message in the input enqueue and send it to the child process. 
        """
        try:
            while self.process.poll() is None:
                send(self.in_q.get(), self.process.stdin)
        except Exception as e:
            pass
        self.process.stdout.close()

