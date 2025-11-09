from pathlib import Path

import numpy as np

from CST.Graph import Graph

class FieldChart(object):
    def __init__(self, graph: Graph, data: list[list[float]]):
        self.__graph = graph
        self.__data = []
        if data:
            for _ in range(len(data[0])):
                self.__data.append([])
            for _line in data:
                for i, __num in enumerate(_line):
                    self.__data[i].append(__num)

    @property
    def graph(self):
        return self.__graph

    @staticmethod
    def parse_ffs_file(dir: Path, graph: Graph):
        ffs_file : Path = dir / graph.files
        if ffs_file.suffix != ".ffs":
            raise RuntimeError()
        if not ffs_file.exists():
            raise FileNotFoundError()

        # 读取文件，转化为字符串列表
        lines: list[str]
        with open(ffs_file) as f:
            lines = f.readlines()

        # 去除文件头
        index: int = 4
        body_lines = lines[index : ]

        data: list[list[float]] = []
        for _line in body_lines:
            words = _line.strip().split(" ")
            nums: list[float] = []
            for __word in words:
                nums.append(float(__word))
            data.append(nums)
        return FieldChart(graph, data)