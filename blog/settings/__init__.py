
try:
    from .dev import *

    live = False
except ImportError:
    live = True

if live:
    from .prod import *