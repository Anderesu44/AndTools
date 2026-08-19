__author__ = "Andev"
from .Types import Version as V
from .Ptoyects import json
__version__ = V(1,8,0)


dump = json.dump
dumps = json.dumps
load = json.load
loads = json.loads
standarize = json.standarizer