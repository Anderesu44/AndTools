__author__ = "Andev"
from .Types import Version as V
__version__ = V(1,8,0)

import sys

from os import makedirs, path
from json import JSONDecoder, JSONEncoder, dumps as _json_dumps, dump as _json_dump, loads as _json_loads, load as _json_load
from _io import TextIOWrapper
from typing import Any, Literal,Callable
from .Types import SecureString, FunctionType, NoneType

class DataBaseJsonManger():
    def __init__(self,db_path:str=".\\db",name:str="db.json"):
        db_path = path.realpath(path.expanduser(db_path))
        self.plain_file = path.join(db_path,name)
        makedirs(db_path,511,True)
        try:
            with open(self.plain_file,"r+") as fp:
                a = fp.read()
                if a == "":
                    fp.write("{\n\n}")
        except FileNotFoundError:
            with open(self.plain_file,"w") as fp:
                fp.write("{\n\n}")
    def create(self,id,registro):
        with open(self.plain_file,"r") as fp:
            db_dict = json.load(fp)
        try:
            if db_dict[id]:
                return False
        except KeyError:
            pass
        db_dict[id]=registro
        with open(self.plain_file,"w") as fp:
            json.dump(db_dict,fp,indent=4)
        return True
    def update(self,id,registro):
        with open(self.plain_file,"r") as fp:
            db_dict = json.load(fp)
        try:
            if not db_dict[id]:
                return False
        except KeyError:
            return False
        db_dict[id]=registro
        with open(self.plain_file,"w") as fp:
            json.dump(db_dict,fp,indent=2)
        return True
    def read(self,id=None):
        with open(self.plain_file,"r") as f:
            db_dict:dict = json.load(f)
        if id:
            return db_dict[id]
        else:
         return db_dict
    def delete(self,id):
        with open(self.plain_file,"r") as f:
            db_dict:dict = json.load(f)
        try:
            if not db_dict[id]:
                return False
        except KeyError:
            return False
        db_dict.pop(id)
        with open(self.plain_file,"w") as f:
            json.dump(db_dict,f,indent=2)
        return True
    def _set(self,data):
        with open(self.plain_file,"w") as f:
            json.dump(data,f,indent=2)
        return True

class ConfigFormatError(Exception):...

class ConfigManager():
    def __init__(self,db_path: str = ".\\db",name: str = "cfg.json",init:dict|None=None,dinamic:bool=False):
        super().__init__()
        self.db = DataBaseJsonManger(db_path,name)
        self.__cfgs = {}
        self.load_config()

        self.__isdinamic = dinamic
        if len(self)==0:
            if init:
                self.set_config(init)
    @property
    def dinamic(self):
        return self.__isdinamic

    @dinamic.setter
    def dinamic(self,value:bool):
        if value:
            self.__isdinamic = True
        else:
            self.__isdinamic = False

    def save_config(self,*args,**kwargs):
        self.db._set(self)

    def load_config(self):
        data = self.db.read()
        self.set_config(data,save=False)

    def set_config(self,data,save=True):
        if type(data) != dict:
            raise ConfigFormatError("main type error")
        for key, value in data.items():
            if type(key) != str:
                raise ConfigFormatError(f"main:key type error {type(key)}")
            if key.strip() != "cfgs":
                if key.strip() not in ["","db","_ConfigManager__isdinamic","__isdinamic"] and key[0] not in [str(n) for n in range(10)] and SecureString(key):
                    setattr(self,SecureString(key,allow_chars=SecureString.allow_chars[1:] + ["_"]).s,value)
                else:
                    print(f"[WARNING] attribute {key} not add")
            else:
                if type(value) != dict:
                    raise ConfigFormatError(f"cfg type error {type(value)}")
                self.__cfgs:dict = value
        if save:
            self.save_config()

    def __setitem__(self, key: Any, value: Any) -> None:
        return_ = self.__cfgs[key] = value
        if self.__isdinamic:
            self.save_config()
        return return_

    def __getitem__(self, key):
        if self.__isdinamic:
            self.load_config()
        return self.__cfgs[key]

    def get(self,key:Any,default: None = None,):
        return self.__cfgs.get(key,default)

    def __iter__(self):
        for key,value in self.__cfgs.items():
            yield (key,value)
    
    def __len__(self):
        return len(self.__cfgs)

    def __json__(self):
        dict_ = self.__dict__.copy()
        dict_.pop("db")
        dict_.pop("_ConfigManager__isdinamic")
        dict_["cfgs"] = dict_.pop("_ConfigManager__cfgs")
        return  dict_

class json:
    @classmethod
    def default(cls,obj:Any)->Any:
        try:
            return obj.__json__()
        except AttributeError:
            raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")
    @classmethod
    def str_for_error(cls,obj)->Any:
        try:
            return obj.__json__()
        except AttributeError:
            try:
                return str(obj)
            except AttributeError:
                raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable") 
    @classmethod
    def dumps(_cls,obj,*,skipkeys: bool = False,ensure_ascii: bool = True,check_circular: bool = True,
            allow_nan: bool = True,cls: type[JSONEncoder] | None = None,indent: int | str | None = None,
            separators: tuple[str, str] | None = None,default:Literal["default","str_for_error"]|Callable="default",sort_keys: bool = False,**kwds: Any)->str:
        if type(default) == str:
            match default:
                case "str_for_error":
                    _default = _cls.str_for_error
                case "default":
                    _default = default
        elif isinstance(default,Callable):
            _default = default
        else:
            raise TypeError(f"Default value must be a string or callable")
        return _json_dumps(obj,skipkeys=skipkeys,ensure_ascii=ensure_ascii,check_circular=check_circular,allow_nan=allow_nan,
                            cls=cls,indent=indent,separators=separators,default=_default,sort_keys=sort_keys,**kwds)
    @classmethod
    def dump(_cls,obj,fp:TextIOWrapper,*,skipkeys: bool = False,ensure_ascii: bool = True,check_circular: bool = True,
            allow_nan: bool = True,cls: type[JSONEncoder] | None = None,indent: int | str | None = None,
            separators: tuple[str, str] | None = None,sort_keys: bool = False,**kwds: Any)->None:
        return _json_dump(obj,fp,skipkeys=skipkeys,ensure_ascii=ensure_ascii,check_circular=check_circular,allow_nan=allow_nan,
                           cls=cls,indent=indent,separators=separators,default=_cls.default,sort_keys=sort_keys,**kwds)
    @classmethod
    def loads(_cls,s:str,*,cls: type[JSONDecoder] | None = None,object_hook: dict[Any, Any] | Any | None = None,
              parse_float:str | Any | None = None,parse_int: str | Any | None = None,parse_constant: str | Any | None = None,
              object_pairs_hook: list[tuple[Any, Any]] | Any | None = None,**kwds: Any) -> Any:
        return _json_loads(s)
    @classmethod
    def load(_cls,fp:TextIOWrapper,*,cls: type[JSONDecoder] | None = None,object_hook: dict[Any, Any] | Any | None = None,
             parse_float:str | Any | None = None,parse_int: str | Any | None = None,parse_constant: str | Any | None = None,
             object_pairs_hook: list[tuple[Any, Any]] | Any | None = None,**kwds: Any) -> Any:
        return _json_load(fp)
    @classmethod
    def standarizer(cls,obj:Any)->Any:
        if not isinstance(obj,(str,int,float,bool,NoneType)):
            try:
                obj = obj.__json__() # pyright: ignore[reportOptionalMemberAccess, reportAttributeAccessIssue]
            except AttributeError,TypeError:
                try:
                    obj = dict(obj) # pyright: ignore[reportCallIssue, reportArgumentType]
                except TypeError, ValueError:
                    try:
                        obj = list(obj) # pyright: ignore[reportArgumentType]
                    except TypeError:
                        return str(obj)
        else:
            return obj

        if isinstance(obj,dict):
            standarized_obj = {}
            for (key,value) in obj.items():
                try:
                    standarized_obj[cls.standarizer(key)]=cls.standarizer(value)
                except Exception as Error:
                    standarized_obj[cls.standarizer(key)]="Not accessible"
            return standarized_obj
        elif isinstance(obj,(list,tuple,set)):
            standarized_obj = []
            for value in obj:
                standarized_obj.append(cls.standarizer(value))
            return standarized_obj
        else:
            raise


function = FunctionType
INFORME = """
date:{date}
Context:
    proyect_path:{proyect_path}
    main_file:{main_file}
    argv:
        {argv}
    globals:
        {globals}
    special:
        {special}
Exception:
    {Traceback}
    {Exception}: {Exception_messeger}
    line:{line}
    column:{column}


ExcConVersion = {__version__}
"""
class ErrorControlled(Exception):...
global _special_vars

_special_vars:dict[str,Any]={}
class ExcpectionController:
    def __init__(self,msg:str|Literal[False]|None = None,special_vars:dict[str,Any]={},) -> None:
        _special_vars = special_vars
        msg = "" if msg == False else msg
        self.msg = msg or "An unexpected error has occurred, don't worry. if it persist contact me"
        self.__version__ = "0.1"


    def __call__(self,fun:function,except_fun:function|None = None,except_fun_args:list=[],except_fun_kwds:dict=dict()) -> function:
        
        def wrapper(*args: Any, **kwds: Any)->Any|ErrorControlled:
            try:
                return_ = fun(*args,**kwds)
            except Exception as Error:
                import __main__
                from sys import argv
                from datetime import datetime
                from .TextHandle import format_text as format
                import traceback
                __globals = globals()
                __globals.pop("__builtins__")
                __globals = json.standarizer(__globals)
                _special_vars = __globals.pop("_special_vars")
                _special_vars = json.standarizer(_special_vars)
                if getattr(sys, 'frozen', False):
                    proyect_path = path.dirname(path.abspath(argv[0]))
                else:
                    proyect_path = path.dirname(path.abspath(__main__.__file__))
                info:dict[str,str] = {
                    "date":str(datetime.now()),
                    "proyect_path":proyect_path,
                    "main_file":__main__.__file__,
                    "argv":str(argv),
                    "globals":json.dumps(__globals,indent=4),
                    "Traceback":format(*traceback.format_exception(NameError,Error,tb=Error.__traceback__)[:-1],step="    ").replace('", line ',':'),
                    "Exception":str(type(Error).__name__),
                    "Exception_messeger":str(Error),
                    "special":str(json.dumps(_special_vars,indent=4) or "") ,
                    "__version__":str(__version__),
                    "line":"0", #? IN DEV
                    "column":"1", #? IN DEV
                }
                error_text = INFORME.format(**info)
                try:
                    version = __version__
                except NameError:
                    version = 0.0
                erorr_file = path.join(proyect_path, "errors.log")
                temp:str=""
                try:
                    with open(erorr_file,"r",encoding="UTF-8") as ft:
                        temp = ft.read()
                except FileNotFoundError:
                    pass
                with open(erorr_file,"w",encoding="UTF-8") as ft:
                    temp:str = temp + "\n"+error_text if temp else error_text
                    ft.write(temp)
                    print(self.msg)
                
                return ErrorControlled

            return return_
        return wrapper # type: ignore

    @classmethod
    def add_var(cls,name:str,value:Any) -> None:
        _special_vars[name] = value

ExcCon = ExcpectionController
# exccontroller = ExcpectionController()

# @exccontroller # type: ignore
# def main(*args,**kwds):
#     print(*args,kwds)
#     2/0

# if __name__ == "__main__":
#     pass
#     main("el pepe",24,32,la="loca")