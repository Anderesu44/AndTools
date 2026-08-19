__author__ = "Andev"
from .Types import Version as V
__version__ = V(1,7,0)

def reducing_characters(text:str,character:str = " ")->str:
        #? reducing characters
        switch = 0
        new_text = ""
        for i in text:
            if switch:
                if i == character:
                    switch = 1
                    continue
                else:
                    switch = 0
                    new_text += i
            else:
                if i == character:
                    switch = 1
                    new_text += i
                else:
                    new_text += i
        return new_text

def format_text(*args,sep:str|None=" ",final:str|None=None,start:int|None=None,end:int|None=None,max:int|None=None,min_fill:tuple[int,str]|None=None,three_dot:str="...",**kwargs)->str:
    text:str = ""
    if min_fill:
        min, fill = min_fill
    for arg in args:
        text += str(arg)
        if sep:
            text+= str(sep)
    if sep:
        text = text.rstrip(str(sep))
    if start:
        text = format_text(*text[start:],sep="")
        text = str(three_dot)+text
    if end:
        text = format_text(*text[:end],sep="")
        text += str(three_dot)
    if min_fill:
        if min:
            if len(text)<min:
                missing = min- len(text)
                fillling =  format_text(fill*(min // len(fill)+1),max=missing,three_dot="")
                text+= fillling
        
    if max:
        if len(text)>max:
            text = format_text(*text[:max],sep="")
            text += str(three_dot)

    if final:
        text+= str(final)
    return text