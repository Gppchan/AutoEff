from pathlib import Path


class Contents(object):
    def __init__(self, path: str | Path):
        if Path(path).suffix != ".cst":
            raise TypeError()
        if not Path(path).exists():
            raise FileNotFoundError()
        self.__project = Path(path)

    @property
    def name(self):
        return self.__project.stem

    @property
    def project(self):
        return self.__project

    @property
    def project_dir(self):
        return self.__project.parent / self.__project.stem

    @property
    def model_dir(self):
        return self.project_dir / "Model"

    @property
    def result_dir(self):
        return self.project_dir / "Result"

    @property
    def schematic_xml(self):
        return self.model_dir / "DS" / "Schematic.xml"

    @property
    def model_mod(self):
        return self.model_dir / "3D" / "Model.mod"

    @property
    def model_res(self):
        return self.result_dir / "Model.res"

    @property
    def cache_dir(self):
        return self.project_dir / "Cache"

    @property
    def ds_result_dir(self):
        return self.result_dir /  "DS"

    @property
    def ds_model_res(self):
        return self.ds_result_dir / "Model.res"