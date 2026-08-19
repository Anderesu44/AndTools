__author__ = "Andev"
from .Types import Version as V
__version__ = V(1,8,0)

__all__ = ["Algorithms"]
class Algorithms:
    @classmethod
    def bubbleSort(cls,_list:list)->list:
        n = len(_list)
        for i  in range(1, n):
            for j in range(n-1):
                if _list[j] > _list[j+1]:
                    temp = _list[j]
                    _list[j] = _list[j+1]
                    _list[j+1] = temp
        return _list
    @classmethod
    def __merge(cls,list_1:list,list_2:list)->list:
        list_3 = []
        while len(list_1) > 0 and len(list_2) > 0:
            if  list_1[0] < list_2[0]:
                list_3.append(list_1[0])
                list_1 = list_1[1:]
            else:
                list_3.append(list_2[0])
                list_2 = list_2[1:]
        if len(list_1) > 0:
            list_3 = list_3 + list_1
        if len(list_2) > 0:
           list_3 = list_3 + list_2 
        return list_3
    @classmethod
    def mergeSort(cls,_list:list)-> list:
        if len(_list) == 1:
            return _list
        lList = _list[:len(_list)//2]
        rList = _list[len(_list)//2:]
        lList = cls.mergeSort(lList)
        rList = cls.mergeSort(rList)
        return cls.__merge(lList,rList)
    