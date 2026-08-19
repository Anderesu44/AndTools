__author__ = "Andev"
from .Types import Version as V
__version__ = V(1,8,0)

import sys
from os import listdir, path as os_path, name as os_name, getcwd
from typing import Optional,Literal
from .Types import FunctionType as function
from .TextHandle import format_text

class DirNotFoundError(FileNotFoundError):...

class Path():
    def __init__(self,path:str,*,sep:Optional[str]=None,level:Literal["system","user"]="system") -> None:
        self.sep = sep or self.get_sys_sep()
        self.pre = self.get_pre_path(level)
        self.path = path

    @property
    def realpath(self)->str:
        path = self.path
        if "\\" in path and self.sep != "\\":
            path = path.replace("\\",self.sep)
        if "/" in path and self.sep != "/":
            path = path.replace("/",self.sep)
        part_path = path.split(self.sep)
        if part_path[0] == "~":
            part_path[0] = os_path.expanduser("~")
        if part_path[0] == ".":
            part_path[0] = self.pre
        if part_path[0] == "..":
            part_path[0] = os_path.dirname(self.pre)

        if not part_path[0]:
            if len(part_path[1]) == 1:
                if os_name == "nt":
                    part_path[1] += ":"
                part_path.pop(0)
            else:
                part_path[0]
        
        path = self.sep.join(part_path)
        return os_path.realpath(path)

    def is_dir(self)->bool:
        return os_path.isdir(self.realpath)

    @classmethod
    def get_sys_sep(cls)->Literal["/","\\"]:
        if os_name == "nt":
            return "\\"
        else:
            return "/"
    @classmethod
    def get_pre_path(cls,level:Literal["system","user"]="system")->str:
        def temp(obj):
            try:
                return str(obj)
            except:
                return "No accesible"
        if level == "system":
            if getattr(sys,"freze",False):
                return os_path.dirname(sys.executable)
            else:
                return sys.path[0] #os_path.dirname(sys.path[0])
            
        else:
            return getcwd()

    def __str__(self) -> str:
        return self.realpath


    s = realpath
    
    
class Tree():
    def __init__(self,path_:str,folders_function:function|None=None,files_function:function|None=None) -> None:
        path_ = os_path.realpath(os_path.expanduser(path_))
        if not os_path.isdir(path_):
            raise DirNotFoundError("Dir not found")
        self.root:str = path_ or ""
        self.folders_function:function|None = folders_function
        self.files_function:function|None = files_function
        self.folders:list[str] = []
        self.files:list[str] = []
        self.branches:list[Branch]=[]
        self.fruits:list[Fruit]=[]

    def branche_function(): # pyright: ignore[reportSelfClsParameterName]
        pass

    def fruit_function(): # pyright: ignore[reportSelfClsParameterName]
        pass

    def tree(self,folders_function:function|None=None,files_function:function|None=None):
        if folders_function:
            self.folders_function= folders_function
        if files_function:
            self.files_function= files_function
        self.__map(self.root)

    #!in developemnt
    def __tree(self,branche_function:None|function=None,fruit_function:function|None=None):
        if branche_function:
            self.branche_function= branche_function # pyright: ignore[reportAttributeAccessIssue]
        if fruit_function:
            self.fruit_function= fruit_function # pyright: ignore[reportAttributeAccessIssue]
        self.__map(self.root)
    def __map(self,branch):
        childrens = listdir(branch)
        
        for child in childrens:
            child_path = os_path.join(branch,child)
            if os_path.isdir(child_path):
                #?child_type = "Branch"
                if type(self.folders_function) == function:
                    self.folders_function(child_path)
                self.folders.append(child_path)
            else:
                #*child_type = "Fruit"
                if type(self.files_function) == function:
                    self.files_function(child_path)
                self.files.append(child_path)
                
    def __str__(self)->str:
        return format_text("files:",*self.files,sep="\n\t")+format_text("folders:",*self.folders,sep="\n\t")

#!in development
class Branch:
    def __init__(self,_path:str):
        if not os_path.isdir(_path):
            raise TypeError(f'"{_path}" Not found or not a folder')
        
        name = os_path.basename(_path)
        location = os_path.dirname(_path)
        
        self._path:str = _path
        self.name:str =name
        self.location:str =location
        self._direct_childrens:list[Fruit|Branch] = []
        self._childrens:list[Fruit|Branch] = [] 
        self._branchs:list[Branch] = []
        self._fruits:list[Fruit] = []
        self.length = 0
    
    @property
    def childrens(self)->tuple[Fruit|Branch,...]:
        return tuple(self._childrens)

    @property
    def direct_childrens(self)->tuple[Fruit|Branch,...]:
        return tuple(self._direct_childrens)

    @property
    def branchs(self)->tuple[Branch,...]:
        return tuple(self._branchs)

    @property
    def fruits(self)->tuple[Fruit,...]:
        return tuple(self._fruits)
    
    def append(self,child:Fruit|Branch)-> int:
        if type(child) == Fruit or type(child) == Branch:
            if child.location == self._path:
                self._direct_childrens.append(child)
                if type(child) == Branch:
                    self._branchs.append(child)
                elif type(child) == Fruit:#no uso else por el pylance
                    self._fruits.append(child)
            elif self._path in child.location:
                self._childrens.append(child)
            else:
                raise TypeError(f"expected a child, {child} not is child of {self}")
        else:
            raise TypeError(f'expected Fruit or Branch object, not {type(child)}')
        self.length+=1
        return self.length
    def __str__(self)->str:
        return self.name
    
    def __len__(self)->int:
        return self.length
    __add__ = append
    
class Fruit:
    def __init__(self,_path:str):
        if not os_path.isfile(_path):
            raise TypeError(f'"{_path}" Not found or not a file')
        
        name = os_path.basename(_path)
        location = os_path.dirname(_path)
        
        
        self.path:str = _path
        self.name:str = name
        self.location:str = location
    def __iter__(self):
        yield self.path
        yield self.name
        yield self.location
    