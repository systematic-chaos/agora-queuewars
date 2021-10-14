from threading import Lock

class SynchronizedSet(set):
    """A set where add(), remove(), and 'in' operators are thread-safe"""

    def __init__(self, *args, **kwargs):
        self._lock = Lock()
        super(SynchronizedSet, self).__init__(*args, **kwargs)
    
    def add(self, elem):
        with self._lock:
            super(SynchronizedSet, self).add(elem)
    
    def remove(self, elem):
        with self._lock:
            super(SynchronizedSet, self).remove(elem)
    
    def __contains__(self, elem):
        with self._lock:
            super(SynchronizedSet, self).__contains__(elem)
