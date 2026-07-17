__author__ = "Anderesu44"
__version__ = 1.4

from os import makedirs, path
from json import load,dump

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
            db_dict = load(fp)
        try:
            if db_dict[id]:
                return False
        except KeyError:
            pass
        db_dict[id]=registro
        with open(self.plain_file,"w") as fp:
            dump(db_dict,fp,indent=4)
        return True
    def update(self,id,registro):
        with open(self.plain_file,"r") as fp:
            db_dict = load(fp)
        try:
            if not db_dict[id]:
                return False
        except KeyError:
            return False
        db_dict[id]=registro
        with open(self.plain_file,"w") as fp:
            dump(db_dict,fp,indent=2)
        return True
    def read(self,id=None):
        with open(self.plain_file,"r") as f:
            db_dict:dict = load(f)
        if id:
            return db_dict[id]
        else:
         return db_dict
    def delete(self,id):
        with open(self.plain_file,"r") as f:
            db_dict:dict = load(f)
        try:
            if not db_dict[id]:
                return False
        except KeyError:
            return False
        db_dict.pop(id)
        with open(self.plain_file,"w") as f:
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
