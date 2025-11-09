from pathlib import Path


class Graph(object):
    def __init__(self, lines: list[str]):
        self.__type = ""
        self.__subtype = ""
        self.__problemclass = ""
        self.__visibility = ""
        self.__creation = ""
        self.__lifetime = ""
        self.__result = ""
        self.__parametric = ""
        self.__treepath = ""
        self.__files = ""
        for _line in lines:
            words: list[str] = _line.split("=s:")
            key, value = words[0: 2]
            self.__setattr__(f"_{self.__class__.__name__}__{key}", value)

    def is_sig(self):
        return self.__files.endswith(".sig")

    @property
    def type(self):
        return self.__type

    @property
    def subtype(self):
        return self.__subtype

    @property
    def problemclass(self):
        return self.__problemclass

    @property
    def visibility(self):
        return self.__visibility

    @property
    def creation(self):
        return self.__creation

    @property
    def lifetime(self):
        return self.__lifetime

    @property
    def result(self):
        return self.__result

    @property
    def parametric(self):
        return self.__parametric

    @property
    def treepath(self):
        return self.__treepath

    @property
    def name(self):
        return self.__treepath.split("\\")[-1]

    @property
    def files(self):
        return self.__files

    @staticmethod
    def extract_graph(model_res_path: Path, treepath: str = ""):
        if model_res_path.suffix != ".res":
            raise RuntimeError()
        if not model_res_path.exists():
            raise FileNotFoundError()

        # 读取文件，转化为字符串列表
        lines: list[str]
        with open(model_res_path) as f:
            lines = f.readlines()

        # 去除文件头
        index: int = 0
        for i, _line in enumerate(lines):
            if _line.strip() == "":
                index = i
                break
        head_lines = lines[0:index]
        body_lines = lines[index:]

        # 提取数量
        graph_num = int(head_lines[1].split("=i:")[1])

        all_graphs: list[Graph] = []
        graph_lines: list[str] = []
        for _line in body_lines:
            if not _line.strip():
                if graph_lines:
                    all_graphs.append(Graph(graph_lines))
                    graph_lines = []
            else:
                graph_lines.append(_line.strip())
        if len(all_graphs) != graph_num:
            raise IOError

        graphs: list[Graph] = []
        if treepath:
            for _graph in all_graphs:
                if treepath in _graph.treepath:
                    graphs.append(_graph)
        return graphs
