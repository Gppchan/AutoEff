import sys
from pathlib import Path

from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget,
                               QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox)
import tkinter as tk
import tkinter.messagebox
import CST
from LIC import Status, TrialManager
from efficiency import cal_antenna_eff_map, export_antenna_eff_map
from ui import AntennaAllocationWidget, PathSelectionWidget, DARK_STYLE_SHEET


class MainWindow(QMainWindow):
    def __init__(self, cst_path: str):
        super().__init__()
        self.__init_data(cst_path)
        self.__init_ui()

    def __init_data(self, cst_path: str):
        self.cst = CST.Contents(cst_path)

    def __init_ui(self):
        self.setWindowTitle("天线频率选择系统")

        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # 添加天线表格
        self.antenna_allocation = AntennaAllocationWidget(self.cst)
        main_layout.addWidget(self.antenna_allocation)

        self.path_selection = PathSelectionWidget(self.cst)
        main_layout.addWidget(self.path_selection)

        # 添加OK和Cancel按钮
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        ok_btn = QPushButton("确定")
        ok_btn.clicked.connect(self.__on_ok_clicked)
        button_layout.addWidget(ok_btn)
        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(self.__on_cancel_clicked)
        button_layout.addWidget(cancel_btn)
        main_layout.addLayout(button_layout)

        self.setCentralWidget(central_widget)

        # 计算表格高度
        table_height = self.antenna_allocation.get_height()

        # 计算其他组件的高度
        title_height = 50  # 标题高度
        path_height = 40  # 路径选择区域高度
        button_height = 50  # 按钮区域高度
        margin = 40  # 边距

        # 计算总高度
        total_height = title_height + table_height + path_height + button_height + margin

        # 限制最大高度为屏幕高度的80%
        screen_height = QApplication.primaryScreen().availableGeometry().height()
        max_height = int(screen_height * 0.8)

        # 如果计算的高度超过最大高度，使用最大高度并启用滚动
        if total_height > max_height:
            total_height = max_height
            # 设置表格的最大高度，使其可以滚动
            self.antenna_allocation.table_widget.setMaximumHeight(
                max_height - title_height - path_height - button_height - margin)
        else:
            # 设置表格的最大高度为计算的高度
            self.antenna_allocation.table_widget.setMaximumHeight(table_height)

        # 设置窗口大小 - 增加宽度以适应频率选择对话框
        self.resize(1000, total_height)

        # 居中显示窗口
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

    def __on_ok_clicked(self):
        """确定按钮点击事件"""
        result_dir: Path = Path(self.path_selection.get_path())
        if not (result_dir.exists() and result_dir.is_dir()):
            QMessageBox.warning(self, "Error", "指定的路径不存在。")
            return
        antenna_table: list[tuple[str, str, str]] = self.antenna_allocation.get_antenna_table()
        is_null: bool = True
        for _, _ , _freq_text in antenna_table:
            if _freq_text:
                is_null = False
                break
        if is_null:
            QMessageBox.warning(self, "Error", "未指定频段。")
            return

        antenna_eff_map: dict[str, dict[str, tuple[float]]] = cal_antenna_eff_map(self.cst, antenna_table)
        export_antenna_eff_map(antenna_eff_map, result_dir)
        print(antenna_eff_map)

    def __on_cancel_clicked(self):
        """取消按钮点击事件"""
        self.close()


def main():
    if TrialManager.check_user_trial() == Status.EXPIRED:
        tk.messagebox.showerror("Error", "试用过期")
        return
    elif TrialManager.check_user_trial() == Status.ILLEGAL:
        tk.messagebox.showerror("Error", "试用凭证损坏")
        return

    if len(sys.argv) > 1:
        _, cst_path = sys.argv
    else:
        return

    # 显示主窗口
    app = QApplication(sys.argv)
    app.setStyleSheet(DARK_STYLE_SHEET)
    window = MainWindow(cst_path)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
