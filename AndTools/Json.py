__author__ = "Andev"
from json import JSONDecodeError,JSONDecoder,JSONEncoder
from .Types import Version as V
from .Ptoyects import json
__version__ = V(1,8,0)


dump = json.dump
dumps = json.dumps
load = json.load
loads = json.loads
standarize = json.standarizer
jsonrizer = standarize