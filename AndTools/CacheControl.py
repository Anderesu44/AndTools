__author__ = "Andev"
from .Types import Version as V, FunctionType
__version__ = V(1,0,0)

from shutil import copy2
from typing import Any, Literal
from datetime import datetime,timedelta,UTC
from .Ptoyects import ConfigManager, json

class FunctionControlled(object):
    def __init__(self,fun:FunctionType,*,cache_time:timedelta|None=None) -> None:
        self.__fun = fun
        self.cache_time = cache_time if isinstance(cache_time,timedelta) else None

    @property
    def __name__(self):
        return self.__fun.__name__

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.__fun(*args,**kwds)

    def __enter__(self)->FunctionControlled:
        return self
    
    def __exit__(self, exc_type, exc, tb)->bool:
        if exc_type:
            return True 
        return True

class CacheController:
    date_format = r"%H:%M:%S, %d/%m/%Y"
    key_format = "{function}: {args};{kwds}"
    def __init__(self,path:str="./db",cache_time:timedelta=timedelta(days=7)) -> None:
        self.cache_db =  ConfigManager(path,"cache",{"cfgs":{"functions":{}},"version":str(__version__)},True)
        if V.fromstr(self.cache_db.version) < float(__version__): # pyright: ignore[reportAttributeAccessIssue]
            # raise Exception("Cache version is not compatible with the current one")
            copy2(self.cache_db.db.plain_file,f"{path}/cache_deprecate.db")
            self.cache_db.set_config({"cfgs":{"functions":{}},"version":str(__version__)})

        self.cache_time:timedelta = cache_time
        self.check()

    def check(self):
        cache:dict[str,dict] = self.cache_db["functions"]
        for key,function in cache.items():
            if datetime.now() >= datetime.strptime(function["date_expired"],self.date_format):
                cache.pop(key)
        self.cache_db["functions"]=cache

    def set_function_cache(self,function:FunctionControlled,args,kwds,fun_return)->str:
        key:str = self.key_format.format(function=function.__name__,args=args,kwds=kwds)
        data:dict = {
            "date_expired":(datetime.now() + (function.cache_time or self.cache_time)).strftime(self.date_format),
            "return_type": type(fun_return).__name__,
            "return_value": fun_return,
        }
        self.cache_db["functions"][key] = data
        self.cache_db.save_config()
        return key

    def get_function_cache(self,function,args,kwds)->dict[Literal["date_expired","return_type","return_value"],Any]|Literal[False]:
        key:str = self.key_format.format(function=function.__name__,args=args,kwds=kwds)
        fun = self.cache_db["functions"].get(key,False)
        if not fun:
            return False
        if datetime.now() >= datetime.strptime(fun["date_expired"],self.date_format):
            self.cache_db["functions"].pop(key)
            return False
        if fun["return_type"] == bytes.__name__:
            fun["return_value"] = eval(fun["return_value"])
        else:
            fun["return_value"] = fun["return_value"]
        return fun

    def __call__(self,fun:FunctionType, *args: Any, **kwds: Any)->FunctionControlled:
        if type(kwds.get("cache_time",False)) == timedelta:
            cache_time = kwds["cache_time"]
        def wrapper(*args,**kwds):
            cfun = FunctionControlled(fun)
            rfun = self.get_function_cache(cfun,args,kwds)
            if rfun:
                return rfun["return_value"]
            else:
                return_value = cfun(*args,**kwds)
                self.set_function_cache(cfun,args,kwds,return_value)
                return return_value
        wrapper.__name__ = fun.__name__
        return FunctionControlled(wrapper)