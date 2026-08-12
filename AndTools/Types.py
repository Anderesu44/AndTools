__author__ = "Anderesu44"
__version__ = 1.6

from typing import Iterable, Iterator, Literal, SupportsIndex


class SecureString():
    _content:str
    allow_chars:list[str] = ["-", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    replace_chars:dict[str,str]={" ":"-",",":"-"}
    _case:Literal["Upper","Lower","Title","Default"]="Lower"
    def __init__(self,object:object = "",*,allow_chars:list|None=None,replace_chars:dict|None=None,case_:Literal["Upper","Lower","Title","Default"]|None=None) -> None:
        if allow_chars:
            self.allow_chars = allow_chars
        if replace_chars:
            self.replace_chars = replace_chars
        if case_:
            self._case = case_
        if not object:
            self._content = ""
            return
        string = str(object)
        secure_string = ""
        for c in string:
            if self._case == "Lower":
                c = c.lower()
            elif self._case == "Upper":
                c = c.upper()
            if c in self.allow_chars:
                secure_string+=c
            elif c in self.replace_chars:
                secure_string+=self.replace_chars[c]
        if self._case == "Title":
            secure_string = secure_string.title()
        # print(secure_string)
        # self = self.replace(self.__str__(),secure_string)
        self._content:str = secure_string

        
    def __add__(self, value: str) -> str:
        return self._content.__add__(value)

    def count(self, sub: str, start: SupportsIndex | None = None, end: SupportsIndex | None = None) -> int:
        return self._content.count(sub, start, end)

    def join(self, iterable: Iterable[str]) -> str:
        return self._content.join(iterable)

    def title(self) -> str:
        return self._content.title()

    def capitalize(self) -> str:
        return self._content.capitalize()

    
    def casefold(self) -> str:
        return self._content.casefold()

    def center(self, width: SupportsIndex, fillchar: str = " ") -> str:
        return self._content.center(width, fillchar)
    
    def encode(self, encoding: str = "utf-8", errors: str = "strict") -> bytes:
        return self._content.encode(encoding, errors)

    def endswith(self, suffix: str | tuple[str, ...], start: SupportsIndex | None = None, end: SupportsIndex | None = None) -> bool:
        return self._content.endswith(suffix, start, end)

    def expandtabs(self, tabsize: SupportsIndex = 8) -> str:
        return self._content.expandtabs(tabsize)

    def find(self, sub: str, start: SupportsIndex | None = None, end: SupportsIndex | None = None) -> int:
        return self._content.find(sub, start, end)
    
    def format(self, *args: object, **kwargs: object) -> str:
        return self._content.format(*args, **kwargs)

    def __hash__(self) -> int:
        return self._content.__hash__()

    def index(self, sub: str, start: SupportsIndex | None = None, end: SupportsIndex | None = None) -> int:
        return self._content.index(sub, start, end)

    def isalnum(self) -> bool:
        return self._content.isalnum()

    def isalpha(self) -> bool:
        return self._content.isalpha()

    def isascii(self) -> bool:
        return self._content.isascii()

    def isdecimal(self) -> bool:
        return self._content.isdecimal()

    def isdigit(self) -> bool:
        return self._content.isdigit()

    def isidentifier(self) -> bool:
        return self._content.isidentifier()

    def islower(self) -> bool:
        return self._content.islower()
    
    def isnumeric(self) -> bool:
        return self._content.isnumeric()

    def isprintable(self) -> bool:
        return self._content.isprintable()

    def isspace(self) -> bool:
        return self._content.isspace()
    
    def istitle(self) -> bool:
        return self._content.istitle()
    
    def isupper(self) -> bool:
        return self._content.isupper()

    def __iter__(self) -> Iterator[str]:
        return self._content.__iter__()

    def lower(self) -> str:
        return self._content.lower()

    def ljust(self, width: SupportsIndex, fillchar: str = " ") -> str:
        return self._content.ljust(width, fillchar)
    
    def lstrip(self, chars: str | None = None) -> str:
        return self._content.lstrip(chars)

    def __len__(self) -> int:
        return self._content.__len__()

    def __le__(self, value: str) -> bool:
        return self._content.__le__(value)

    def __lt__(self, value: str) -> bool:
        return self._content.__lt__(value)

    def partition(self, sep: str) -> tuple[str, str, str]:
        return self._content.partition(sep)

    def removeprefix(self, prefix: str) -> str:
        return self._content.removeprefix(prefix)

    def removesuffix(self, suffix: str) -> str:
        return self._content.removesuffix(suffix)
    
    def replace(self, old: str, new: str, /, count: SupportsIndex = -1) -> str:
        return self._content.replace(old, new, count)

    def rfind(self, sub: str, start: SupportsIndex | None = None, end: SupportsIndex | None = None) -> int:
        return self._content.rfind(sub, start, end)

    def rindex(self, sub: str, start: SupportsIndex | None = None, end: SupportsIndex | None = None) -> int:
        return self._content.rindex(sub, start, end)

    def rjust(self, width: SupportsIndex, fillchar: str = " ") -> str:
        return self._content.rjust(width, fillchar)

    def rpartition(self, sep: str) -> tuple[str, str, str]:
        return self._content.rpartition(sep)

    def rsplit(self, sep: str | None = None, maxsplit: SupportsIndex = -1) -> list[str]:
        return self._content.rsplit(sep, maxsplit)

    def rstrip(self, chars: str | None = None) -> str:
        return self._content.rstrip(chars)

    def split(self, sep: str | None = None, maxsplit: SupportsIndex = -1) -> list[str]:
        return self._content.split(sep, maxsplit)
    
    def splitlines(self, keepends: bool = False) -> list[str]:
        return self._content.splitlines(keepends)

    def startswith(self, prefix: str | tuple[str, ...], start: SupportsIndex | None = None, end: SupportsIndex | None = None) -> bool:
        return self._content.startswith(prefix, start, end)

    def strip(self, chars: str | None = None) -> str:
        return self._content.strip(chars)
    
    def swapcase(self) -> str:
        return self._content.swapcase()
    
    def __str__(self) -> str:
        return str(self._content)

    def __sizeof__(self) -> int:
        return self._content.__sizeof__()

    def upper(self) -> str:
        return self._content.upper()

    def zfill(self, width: SupportsIndex) -> str:
        return self._content.zfill(width)

    def __contains__(self, key: str) -> bool:
        return self._content.__contains__(key)

    def __json__(self):
        return f'"{self}"'

class Version:
    def __init__(self,major:int,minor:int,patch:int) -> None:
        self.major = major
        self.minor = minor
        self.patch = patch

    def as_integer_ratio(self) -> tuple[int, int]:
        return (self.major,self.minor)

    def __bool__(self) -> bool:
        return bool(self.major+self.minor+self.patch)

    def conjugate(self) -> float:
        return float(self).conjugate()

    def __eq__(self, value: int|float|Version) -> bool:
        if type(value) == int:
            return self.major == value
        elif type(value) == float:
            return float(self) == value
        elif type(value) == Version:
            return self.major == value.major and self.minor == value.minor and self.patch == value.patch
        else:
            return NotImplemented

    @classmethod
    def fromhex(cls, string: str):
        return cls(*str(float.fromhex(string))+".0".split(".")) # pyright: ignore[reportOperatorIssue]

    @classmethod
    def fromstr(cls,string:str):
        return cls(*[int(part) for part in string.split(".")])
    
    def __float__(self) -> float:
        return float(f"{self.major}.{self.minor}")

    def __ge__(self, value: int|float|Version) -> bool:
        if type(value) == int:
            return self.major >= value
        elif type(value) == float:
            return float(self) >= value
        elif type(value) == Version:
            return self.major >= value.major and self.minor >= value.minor and self.patch >= value.patch
        else:
            return NotImplemented
    def __gt__(self, value: int|float|Version) -> bool:
        if type(value) == int:
            return self.major > value
        elif type(value) == float:
            return float(self) > value
        elif type(value) == Version:
            return self.major > value.major and self.minor > value.minor and self.patch > value.patch
        else:
            return NotImplemented
    def hex(self) -> str:
        return float(self).hex()

    def __int__(self) -> int:
        return self.major

    def __le__(self, value: int|float|Version) -> bool:
        if type(value) == int:
            return self.major <= value
        elif type(value) == float:
            return float(self) <= value
        elif type(value) == Version:
            return self.major <= value.major and self.minor <= value.minor and self.patch <= value.patch
        else:
            return NotImplemented

    def __lt__(self, value: int|float|Version) -> bool:
        if type(value) == int:
            return self.major > value
        elif type(value) == float:
            return float(self) > value
        elif type(value) == Version:
            return self.major > value.major and self.minor > value.minor and self.patch > value.patch
        else:
            return NotImplemented

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"