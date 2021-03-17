from functools import partial
from pytz import all_timezones

class Schedule():
    """ The parent of "event" and "recurring" classes."""
    
    def __init__(self, verbose=False):
        self._processes = []
        self._workers = []
        self.verbose = verbose
        
    def timezones(self):
        return all_timezones

    def _print(self, message):
        if self.verbose:
            print(message)

    def run(self):
        try:
            if self._processes:
                [process.start() for process in self._processes]
        except:
            [process.terminate for process in self._processes]
            pass

    def _manifest_function(self, target, args, kwargs):
        try:
            function = partial(target, *args, **kwargs)
            function.__qualname__ = target.__qualname__
            function.__doc__ = target.__doc__
            return function
        except:
            self._processes = []
            raise
