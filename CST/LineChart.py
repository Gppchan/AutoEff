from pathlib import Path

import numpy as np

from CST.Graph import Graph


class LineChart(object):
    def __init__(self, graph: Graph, x: np.ndarray, y: np.ndarray):
        self.__graph = graph
        self.__x = x
        self.__y = y

    @property
    def graph(self):
        return self.__graph

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @staticmethod
    def parse_sig_file(dir: Path, graph: Graph):
        sig_file: Path = dir / graph.files
        if sig_file.suffix != ".sig":
            raise RuntimeError()
        if not sig_file.exists():
            raise FileNotFoundError()

        # 读取文件，转化为字符串列表
        lines: list[str]
        with open(sig_file) as f:
            lines = f.readlines()

        # 去除文件头
        index: int = 4
        body_lines = lines[index:]

        data: list[list[float]] = []
        for _line in body_lines:
            words = _line.strip().split(" ")
            nums: list[float] = []
            for __word in words:
                nums.append(float(__word))
            data.append(nums)

        x = np.array([_row[0] for _row in data])
        if len(data[0]) == 2:
            y = np.array([_row[1] for _row in data])
        elif len(data[0]) == 3:
            y = np.array([complex(_row[1], _row[2]) for _row in data])
        else:
            raise
        return LineChart(graph, x, y)
