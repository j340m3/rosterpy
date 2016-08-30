try:
    from .context import rosterpy
except SystemError:
    from context import rosterpy

from rosterpy import main

print(main.res)
