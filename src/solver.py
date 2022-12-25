from abc import ABCMeta, abstractmethod
from pandas import Series, DataFrame
import pandas as pd
import numpy as np

class BinPackingSolver(metaclass=ABCMeta):
    objective: int
    i: int
    capacity: int
    res_capacity: Series
    weight: Series
    ans: DataFrame # items * bins
    
    def __init__(self, weight: Series, capacity: int) -> None:
        self.weight = weight
        self.i = 1
        self.objective = 1
        self.ans = pd.DataFrame(0, index=weight.index, columns=pd.Index([1], name="Bins"))
        self.capacity = capacity
        self.res_capacity = pd.Series(capacity, index=pd.RangeIndex(1, len(weight.index) + 1))
    
    @abstractmethod
    def pack_current(self) -> None:
        """pack single item"""
        raise NotImplementedError()

    def pack_all(self) -> None:
        """pack all items."""
        for _ in self.ans.loc[self.i:].index:
            self.pack_current()

class NextFit(BinPackingSolver):
        
    def __init__(self, weight: Series, capacity: int) -> None:
        super().__init__(weight, capacity)
        self.j = 1

    def pack_current(self) -> None:
        """pack single item"""
        i = self.i
        j = self.j
        weight = self.weight
        if i not in weight.index:
            return
        
        if weight[i] <= self.res_capacity[j]:
            self.ans.loc[i, j] = weight[i]
            self.res_capacity[j] -= weight[i]
        else:
            self.ans[j + 1] = 0
            self.ans.loc[i, j + 1] = weight[i]
            self.res_capacity[j + 1] -= weight[i]
            self.j += 1
            self.objective += 1
        
        self.i += 1

class FirstFit(BinPackingSolver):
        
    def __init__(self, weight: Series, capacity: int) -> None:
        super().__init__(weight, capacity)

    def pack_current(self) -> None:
        """pack single item"""
        i = self.i
        weight = self.weight
        if i not in weight.index:
            return
        
        j = (weight[i] <= self.res_capacity).idxmax()
        if j <= self.objective:
            self.ans.loc[i, j] = weight[i]
            self.res_capacity[j] -= weight[i]
        else:
            self.ans[j] = 0
            self.ans.loc[i, j] = weight[i]
            self.res_capacity[j] -= weight[i]
            self.objective = j
        
        self.i += 1
        
class FirstFitDescending(BinPackingSolver):
        
    def __init__(self, weight: Series, capacity: int) -> None:
        super().__init__(weight, capacity)
        self.weight = self.weight.sort_values(ascending=False)
        self.i = 0
    
    def pack_current(self) -> None:
        """pack single item"""
        weight = self.weight
        if self.i >= len(weight.index):
            return
        
        i = weight.index[self.i]
        j = (weight[i] <= self.res_capacity).idxmax()
        if j <= self.objective:
            self.ans.loc[i, j] = weight[i]
            self.res_capacity[j] -= weight[i]
        else:
            self.ans[j] = 0
            self.ans.loc[i, j] = weight[i]
            self.res_capacity[j] -= weight[i]
            self.objective = j
        
        self.i += 1