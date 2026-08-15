<<<<<<< HEAD
__author__ = "Andev"
from .Types import Version as V
__version__ = V(1,6,1)

from os import makedirs, path
from json import JSONDecoder, JSONEncoder, dumps as _json_dumps, dump as _json_dump, loads as _json_loads, load as _json_load
from _io import TextIOWrapper
from typing import Any
from types import NoneType
=======
__author__ = "Anderesu44"
__version__ = 1.4

from os import makedirs, path
from json import load,dump
>>>>>>> facc81aaaf74a44845e68bda355b133bce1c1369

class DataBaseJsonManger():
    def __init__(self,db_path:str=".\\db",name:str="db.json"):
        db_path = path.realpath(path.expanduser(db_path))
        self.plain_file = path.join(db_path,name)
        makedirs(db_path,True)
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
<<<<<<< HEAD
            db_dict = json.load(fp)
=======
            db_dict = load(fp)
>>>>>>> facc81aaaf74a44845e68bda355b133bce1c1369
        try:
            if db_dict[id]:
                return False
        except KeyError:
            pass
        db_dict[id]=registro
        with open(self.plain_file,"w") as fp:
<<<<<<< HEAD
            json.dump(db_dict,fp,indent=4)
        return True
    def update(self,id,registro):
        with open(self.plain_file,"r") as fp:
            db_dict = json.load(fp)
=======
            dump(db_dict,fp,indent=4)
        return True
    def update(self,id,registro):
        with open(self.plain_file,"r") as fp:
            db_dict = load(fp)
>>>>>>> facc81aaaf74a44845e68bda355b133bce1c1369
        try:
            if not db_dict[id]:
                return False
        except KeyError:
            return False
        db_dict[id]=registro
        with open(self.plain_file,"w") as fp:
<<<<<<< HEAD
            json.dump(db_dict,fp,indent=2)
        return True
    def read(self,id=None):
        with open(self.plain_file,"r") as f:
            db_dict:dict = json.load(f)
=======
            dump(db_dict,fp,indent=2)
        return True
    def read(self,id=None):
        with open(self.plain_file,"r") as f:
            db_dict:dict = load(f)
>>>>>>> facc81aaaf74a44845e68bda355b133bce1c1369
        if id:
            return db_dict[id]
        else:
         return db_dict
    def delete(self,id):
        with open(self.plain_file,"r") as f:
<<<<<<< HEAD
            db_dict:dict = json.load(f)
=======
            db_dict:dict = load(f)
>>>>>>> facc81aaaf74a44845e68bda355b133bce1c1369
        try:
            if not db_dict[id]:
                return False
        except KeyError:
            return False
        db_dict.pop(id)
        with open(self.plain_file,"w") as f:
<<<<<<< HEAD
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
            if key != "cfgs":
                if not getattr(self,key,False):
                    setattr(self,key,value)
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
    def dumps(_cls,obj,*,skipkeys: bool = False,ensure_ascii: bool = True,check_circular: bool = True,
            allow_nan: bool = True,cls: type[JSONEncoder] | None = None,indent: int | str | None = None,
            separators: tuple[str, str] | None = None,sort_keys: bool = False,**kwds: Any)->str:
        return _json_dumps(obj,skipkeys=skipkeys,ensure_ascii=ensure_ascii,check_circular=check_circular,allow_nan=allow_nan,
                            cls=cls,indent=indent,separators=separators,default=_cls.default,sort_keys=sort_keys,**kwds)
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
        if isinstance(obj,(str,int,bool,bool,NoneType)):
            try:
                obj = obj.__json__() # pyright: ignore[reportOptionalMemberAccess, reportAttributeAccessIssue]
            except AttributeError:
                try:
                    obj = dict(obj) # pyright: ignore[reportCallIssue, reportArgumentType]
                except TypeError:
                    try:
                        obj = list(obj) # pyright: ignore[reportArgumentType]
                    except TypeError:
                        obj = str(obj)
        else:
            return obj

        if isinstance(obj,dict):
            standarized_obj = {}
            for (key,value) in obj.values():
                standarized_obj[cls.standarizer(key)]=cls.standarizer(value)
        elif isinstance(obj,(list,tuple,set)):
            standarized_obj = []
            for value in obj:
                standarized_obj.append(cls.standarizer(value))
        else:
            raise
=======
            dump(db_dict,f,indent=2)
        return True
    def _set(self,data):
        with open(self.plain_file,"w") as f:
            dump(data,f,indent=2)
        return True

class ConfigManager(dict):
    def __init__(self,db_path: str = ".\\db",name: str = "cfg.json",init:dict|None=None):
        super().__init__()
        self.db = DataBaseJsonManger(db_path,name)
        self.load_config()
        if len(self)==0:
            if init:
                self.set_config(init)

    def save_config(self,*args,**kwargs):
        self.db._set(self)
    def load_config(self):
        data = self.db.read()
        for key in data:
            value = data[key]
            self.__setitem__(key,value)
    def set_config(self,data):
        for key in data:
            value = data[key]
            self.__setitem__(key,value)
        self.save_config()
>>>>>>> facc81aaaf74a44845e68bda355b133bce1c1369
