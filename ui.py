import re
import os
from pathlib import Path

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
                               QPushButton, QHeaderView, QLabel, QDialog, QCheckBox,
                               QGroupBox, QLineEdit, QFileDialog, QSizePolicy, QMessageBox)
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices

from frequency import FrequencyManager
import CST

# ========================== 样式表定义 ==========================

# 深色模式样式表
DARK_STYLE_SHEET = """
    QMainWindow {
        background-color: #2b2b2b;
        color: #e0e0e0;
    }
    QWidget {
        background-color: #2b2b2b;
        color: #e0e0e0;
    }
    QTableWidget {
        gridline-color: #404040;
        border: 1px solid #404040;
        border-radius: 4px;
        background-color: #323232;
        color: #e0e0e0;
        alternate-background-color: #3a3a3a;
    }
    QTableWidget::item {
        padding: 5px;
        border-bottom: 1px solid #404040;
    }
    QTableWidget::item:selected {
        background-color: #4a4a4a;
        color: #ffffff;
    }
    QHeaderView::section {
        background-color: #404040;
        padding: 5px;
        border: 1px solid #505050;
        font-weight: bold;
        color: #e0e0e0;
    }
    QPushButton {
        background-color: #4CAF50;
        border: none;
        color: white;
        padding: 8px 16px;
        text-align: center;
        text-decoration: none;
        font-size: 14px;
        margin: 4px 2px;
        border-radius: 4px;
    }
    QPushButton:hover {
        background-color: #66BB6A;
    }
    QPushButton:pressed {
        background-color: #388E3C;
    }
    QDialog {
        background-color: #323232;
        color: #e0e0e0;
        border: 1px solid #404040;
        border-radius: 4px;
    }
    QCheckBox {
        spacing: 8px;
        padding: 5px;
        color: #e0e0e0;
        min-width: 100px;
    }
    QCheckBox::indicator {
        width: 18px;
        height: 18px;
        background-color: #404040;
        border: 1px solid #505050;
        border-radius: 2px;
    }
    QCheckBox::indicator:checked {
        background-color: #4CAF50;
        border: 1px solid #4CAF50;
    }
    QCheckBox::indicator:checked:hover {
        background-color: #66BB6A;
        border: 1px solid #66BB6A;
    }
    QCheckBox::indicator:hover {
        border: 1px solid #66BB6A;
    }
    QScrollArea {
        border: 1px solid #404040;
        border-radius: 4px;
        background-color: #323232;
    }
    QScrollBar:vertical {
        background-color: #323232;
        width: 15px;
        margin: 0px;
    }
    QScrollBar::handle:vertical {
        background-color: #505050;
        border-radius: 4px;
        min-height: 20px;
    }
    QScrollBar::handle:vertical:hover {
        background-color: #606060;
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        border: none;
        background: none;
    }
    QLineEdit {
        background-color: #404040;
        border: 1px solid #505050;
        border-radius: 4px;
        padding: 5px;
        color: #e0e0e0;
        selection-background-color: #4CAF50;
    }
    QLineEdit:focus {
        border: 1px solid #4CAF50;
    }
    QLabel {
        font-size: 14px;
        color: #e0e0e0;
    }
    QFrame[frameShape="4"] { /* HLine */
        background-color: #505050;
        border: none;
        max-height: 1px;
        min-height: 1px;
    }
"""

# 浅色模式样式表
LIGHT_STYLE_SHEET = """
    QMainWindow {
        background-color: #f5f5f5;
        color: #333333;
    }
    QWidget {
        background-color: #f5f5f5;
        color: #333333;
    }
    QTableWidget {
        gridline-color: #d0d0d0;
        border: 1px solid #c0c0c0;
        border-radius: 4px;
        background-color: #ffffff;
        color: #333333;
        alternate-background-color: #f8f8f8;
    }
    QTableWidget::item {
        padding: 5px;
        border-bottom: 1px solid #e0e0e0;
    }
    QTableWidget::item:selected {
        background-color: #e3f2fd;
        color: #333333;
    }
    QHeaderView::section {
        background-color: #e0e0e0;
        padding: 5px;
        border: 1px solid #c0c0c0;
        font-weight: bold;
        color: #333333;
    }
    QPushButton {
        background-color: #4CAF50;
        border: none;
        color: white;
        padding: 8px 16px;
        text-align: center;
        text-decoration: none;
        font-size: 14px;
        margin: 4px 2px;
        border-radius: 4px;
    }
    QPushButton:hover {
        background-color: #66BB6A;
    }
    QPushButton:pressed {
        background-color: #388E3C;
    }
    QDialog {
        background-color: #ffffff;
        color: #333333;
        border: 1px solid #c0c0c0;
        border-radius: 4px;
    }
    QCheckBox {
        spacing: 8px;
        padding: 5px;
        color: #333333;
        min-width: 100px;
    }
    QCheckBox::indicator {
        width: 18px;
        height: 18px;
        background-color: #f0f0f0;
        border: 1px solid #c0c0c0;
        border-radius: 2px;
    }
    QCheckBox::indicator:checked {
        background-color: #4CAF50;
        border: 1px solid #4CAF50;
    }
    QCheckBox::indicator:checked:hover {
        background-color: #66BB6A;
        border: 1px solid #66BB6A;
    }
    QCheckBox::indicator:hover {
        border: 1px solid #66BB6A;
    }
    QScrollArea {
        border: 1px solid #c0c0c0;
        border-radius: 4px;
        background-color: #ffffff;
    }
    QScrollBar:vertical {
        background-color: #f0f0f0;
        width: 15px;
        margin: 0px;
    }
    QScrollBar::handle:vertical {
        background-color: #c0c0c0;
        border-radius: 4px;
        min-height: 20px;
    }
    QScrollBar::handle:vertical:hover {
        background-color: #a0a0a0;
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        border: none;
        background: none;
    }
    QLineEdit {
        background-color: #ffffff;
        border: 1px solid #c0c0c0;
        border-radius: 4px;
        padding: 5px;
        color: #333333;
        selection-background-color: #4CAF50;
    }
    QLineEdit:focus {
        border: 1px solid #4CAF50;
    }
    QLabel {
        color: #333333;
    }
    QFrame[frameShape="4"] { /* HLine */
        background-color: #c0c0c0;
        border: none;
        max-height: 1px;
        min-height: 1px;
    }
"""


# ========================== 应用程序类 ==========================

class FrequencySelectionDialog(QDialog):
    """频率选择对话框"""

    def __init__(self, selected_freq: str, parent=None):
        super().__init__(parent)
        self.checked_bands = []
        self.custom_freqs = []
        self.__init_data(selected_freq)
        self.__init_ui()

    def get_selected_freq(self) -> str:
        """获取组合的频率字符串"""
        result_parts = []

        # 添加选中的频率
        if self.checked_bands:
            result_parts.extend(self.checked_bands)

        # 添加自定义频率范围
        if self.custom_freqs:
            result_parts.extend(self.custom_freqs)

        return ", ".join(result_parts) if result_parts else "未选择"

    def __init_data(self, selected_freq: str):
        band_map = FrequencyManager.get_band_map()
        self.band_groups: dict[str, list[str]] = {
            "5G NR": [_band.name for _band in band_map["5G NR"]],
            "4G LTE": [_band.name for _band in band_map["4G LTE"]],
            "3G/2G": ([_band.name for _band in band_map["3G WCDMA"]] +
                      [_band.name for _band in band_map["2G GSM"]]),
            "短距离通信": ([_band.name for _band in band_map["Wi-Fi"]] +
                           [_band.name for _band in band_map["Bluetooth"]] +
                           [_band.name for _band in band_map["NFC"]]),
            "卫星通信": ([_band.name for _band in band_map["GPS"]] +
                         [_band.name for _band in band_map["北斗"]] +
                         [_band.name for _band in band_map["Galileo"]] +
                         [_band.name for _band in band_map["GLONASS"]])}

        if selected_freq:
            selected_freqs = selected_freq.split(",")
            for _freq in selected_freqs:
                if re.findall(r"MHz", _freq):
                    self.custom_freqs.append(_freq)
                else:
                    self.checked_bands.append(_freq)

    def __init_ui(self):
        # 定义频率分组 - 按照您的要求设置

        self.setWindowTitle("选择频率")
        self.setModal(True)

        # 设置对话框固定大小 - 增加高度以容纳两行表格
        self.setFixedSize(920, 750)

        layout = QVBoxLayout()
        layout.setSpacing(8)  # 整体间距
        layout.setContentsMargins(20, 15, 20, 15)  # 边距

        # 创建垂直布局放置所有频率分组
        self.checkboxes = {}

        for _name, _bands in self.band_groups.items():
            # 创建分组框
            group_box = QGroupBox(_name)
            # 设置GroupBox标题样式 - 增大字号
            group_box.setStyleSheet("QGroupBox { font-weight: bold; font-size: 14px; }")
            group_layout = QVBoxLayout(group_box)
            group_layout.setSpacing(5)  # 分组内间距
            group_layout.setContentsMargins(10, 15, 10, 10)  # 设置GroupBox内边距

            # 计算需要的行数和列数
            num_rows = (len(_bands) + 6) // 7  # 向上取整
            num_cols = 7

            # 创建水平布局，用于添加左侧空白、表格和右侧空白
            table_container = QHBoxLayout()
            table_container.setContentsMargins(0, 0, 0, 0)

            # 创建表格控件
            table_widget = QTableWidget(num_rows, num_cols)

            # 隐藏表头
            table_widget.horizontalHeader().setVisible(False)
            table_widget.verticalHeader().setVisible(False)

            # 设置表格属性
            table_widget.setShowGrid(False)  # 不显示网格线
            table_widget.setEditTriggers(QTableWidget.NoEditTriggers)  # 不可编辑
            table_widget.setSelectionMode(QTableWidget.NoSelection)  # 不可选择
            table_widget.setFocusPolicy(Qt.NoFocus)  # 无焦点

            # 关闭滚动条
            table_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            table_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

            # 设置列宽和行高
            for _col in range(num_cols):
                table_widget.setColumnWidth(_col, 120)  # 固定列宽
            for _row in range(num_rows):
                table_widget.setRowHeight(_row, 35)  # 固定行高

            # 添加频率复选框到表格
            for i, __band in enumerate(_bands):
                row = i // num_cols
                col = i % num_cols

                # 创建复选框
                checkbox = QCheckBox(__band)
                checkbox.setChecked(__band in self.checked_bands)
                checkbox.stateChanged.connect(self.__on_checkbox_changed)

                # 设置复选框样式，添加左边距
                checkbox.setStyleSheet("margin-left: 10px;")

                # 将复选框添加到表格单元格
                table_widget.setCellWidget(row, col, checkbox)
                self.checkboxes[__band] = checkbox

            # 设置表格尺寸策略和固定大小
            table_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            table_width = 7 * 120 + 2  # 固定表格宽度
            table_height = num_rows * 35 + 2  # 计算表格总高度
            table_widget.setFixedSize(table_width, table_height)

            # 将表格添加到容器
            table_container.addWidget(table_widget)

            # 将表格容器添加到分组布局
            group_layout.addLayout(table_container)

            # 增加GroupBox的高度
            group_box.setFixedHeight(table_height + 50)  # 表格高度 + 额外空间

            layout.addWidget(group_box)

        # 创建自定义频率范围分组框
        custom_group_box = QGroupBox("自定义频率")
        # 设置自定义频率GroupBox标题样式 - 增大字号
        custom_group_box.setStyleSheet("QGroupBox { font-weight: bold; font-size: 14px; }")
        custom_layout = QVBoxLayout(custom_group_box)
        custom_layout.setSpacing(8)
        custom_layout.setContentsMargins(10, 15, 10, 10)

        # 自定义频率范围输入
        range_layout = QHBoxLayout()

        # 添加左侧空白 - 使用固定宽度的空白部件
        left_spacer = QWidget()
        left_spacer.setFixedWidth(5)
        range_layout.addWidget(left_spacer)

        self.range_edit = QLineEdit()
        if self.custom_freqs:
            self.range_edit.setText(", ".join(self.custom_freqs).replace(" MHz", ""))
        self.range_edit.setPlaceholderText("例如: 1000~2000, 3000; 用英文逗号分割来区分其他频率")
        self.range_edit.textChanged.connect(self.__on_range_changed)
        range_layout.addWidget(self.range_edit)

        unit_label = QLabel("MHz")
        range_layout.addWidget(unit_label)

        # 添加右侧空白 - 使用固定宽度的空白部件
        right_spacer = QWidget()
        right_spacer.setFixedWidth(10)
        range_layout.addWidget(right_spacer)

        custom_layout.addLayout(range_layout)

        # 设置自定义频率GroupBox的高度
        custom_group_box.setFixedHeight(80)

        layout.addWidget(custom_group_box)

        # 底部按钮区域 - 将全选/清除和确定/取消放在同一行
        button_layout = QHBoxLayout()

        # 左侧按钮 - 全选和清除
        select_all_btn = QPushButton("全选")
        select_all_btn.setAutoDefault(False)
        select_all_btn.clicked.connect(self.__select_all)

        clear_all_btn = QPushButton("清除")
        clear_all_btn.setAutoDefault(False)
        clear_all_btn.clicked.connect(self.__clear_all)

        button_layout.addWidget(select_all_btn)
        button_layout.addWidget(clear_all_btn)

        # 添加弹性空间，使左右两侧按钮分开
        button_layout.addStretch()

        # 右侧按钮 - 确定和取消
        ok_btn = QPushButton("确定")
        ok_btn.setAutoDefault(False)
        ok_btn.clicked.connect(self.accept)

        cancel_btn = QPushButton("取消")
        cancel_btn.setAutoDefault(False)
        cancel_btn.clicked.connect(self.reject)

        button_layout.addWidget(ok_btn)
        button_layout.addWidget(cancel_btn)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def __on_checkbox_changed(self):
        """复选框状态改变时更新选择列表"""
        self.checked_bands.clear()
        for _band, _checkbox in self.checkboxes.items():
            if _checkbox.isChecked():
                self.checked_bands.append(_band)

    def __on_range_changed(self, text):
        """自定义频率范围改变时更新"""
        if self.__is_valid_freq(text):
            self.custom_freqs.clear()
            for item in re.split(",", text):
                item : str = item.strip()
                if item:
                    item = f"{item} MHz"
                    self.custom_freqs.append(item)
            self.range_edit.setStyleSheet("border: 1px solid #4CAF50;")  # 清除错误样式
        else:
            self.range_edit.setStyleSheet("border: 1px solid red;")  # 设置错误样式

    def __select_all(self):
        """全选所有频率"""
        for _checkbox in self.checkboxes.values():
            _checkbox.setChecked(True)

    def __clear_all(self):
        """清除所有选择"""
        for _checkbox in self.checkboxes.values():
            _checkbox.setChecked(False)
    
    def __is_valid_freq(self, freq_text : str):
        if not re.match("^[0-9 .~,]*$", freq_text):
            return False

        freq_texts: list[str] = [item.strip() for item in freq_text.split(",")]
        for _freq_text in freq_texts:
            if not _freq_text:
                continue
            elif match := re.match(r"^(\d+\.?\d*)$", _freq_text):
                continue
            elif match := re.match(r"^(\d+\.?\d*)\s*~\s*(\d+\.?\d*)$", _freq_text):
                continue
            else:
                return False
        return True


class AntennaAllocationWidget(QWidget):
    def __init__(self, cst: CST.Contents):
        super().__init__()
        self.antenna_names: list[str] = []
        self.graph_names: list[str] = []
        self.selected_freqs: list[str] = []
        self.__init_data(cst)
        self.__init_ui()

    def get_antenna_table(self) -> list[tuple[str, str, str]]:
        """获取结果路径"""
        return [(self.antenna_names[i], self.graph_names[i], self.selected_freqs[i]) for i in
                range(len(self.antenna_names))]

    def get_height(self):
        """计算表格的合适高度"""
        # 获取表格行数
        row_count = self.table_widget.rowCount()

        # 计算每行的大致高度（包括行高和间距）
        row_height = 40  # 估算每行高度

        # 计算表头高度
        header_height = 40

        # 计算表格总高度
        table_height = header_height + (row_count * row_height)

        return table_height

    def __init_data(self, cst: CST.Contents):
        eff_graphs: list[CST.Graph] = CST.Graph.extract_graph(cst.model_res, "System Tot. Efficiency")
        self.antenna_names = []
        for _graph in eff_graphs:
            if match := re.search(r"\[AC(\d+)]", _graph.name):
                self.antenna_names.append(f"Ant{match[1]}")
                self.graph_names.append(_graph.name)
        self.result_path = str(cst.project_dir)

    def __init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)

        # 标题
        title_label = QLabel("天线频率配置表")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        main_layout.addWidget(title_label)

        # 创建表格
        self.table_widget = QTableWidget(len(self.antenna_names), 3)
        self.table_widget.setHorizontalHeaderLabels(["天线名称", "频率选择", "已选频率"])

        # 设置表格属性 - 确保表格能够扩展填充空间
        self.table_widget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table_widget.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table_widget.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.setAlternatingRowColors(True)

        # 设置表格尺寸策略，使其能够扩展
        self.table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # 填充表格数据
        for _row, _name in enumerate(self.antenna_names):
            # 初始化该行的选择为空列表
            self.selected_freqs.append("")

            # 第一列：天线名称
            name_item = QTableWidgetItem(_name)
            name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
            self.table_widget.setItem(_row, 0, name_item)

            # 第二列：频率选择按钮
            select_btn = QPushButton("选择频率")
            select_btn.clicked.connect(lambda checked, r=_row: self.__open_freq_dialog(r))
            self.table_widget.setCellWidget(_row, 1, select_btn)

            # 第三列：已选频率显示
            selected_item = QTableWidgetItem("未选择")
            selected_item.setFlags(selected_item.flags() & ~Qt.ItemIsEditable)
            self.table_widget.setItem(_row, 2, selected_item)

        main_layout.addWidget(self.table_widget)

        self.setLayout(main_layout)

    def __open_freq_dialog(self, row):
        """打开频率选择对话框"""
        current_selection = self.selected_freqs[row]

        dialog = FrequencySelectionDialog(current_selection, self)

        # 对话框关闭时直接应用选择
        dialog.finished.connect(lambda result, r=row, d=dialog: self.__on_freq_dialog_finished(result, r, d))
        dialog.exec()

    def __on_freq_dialog_finished(self, result, row, dialog):
        """频率选择对话框关闭时的处理"""
        # 无论对话框如何关闭，都更新选择
        selected_freq = dialog.get_selected_freq()
        self.selected_freqs[row] = selected_freq

        # 更新表格显示
        self.table_widget.item(row, 2).setText(selected_freq)


class PathSelectionWidget(QWidget):
    def __init__(self, cst: CST.Contents):
        super().__init__()
        self.result_path: str = ""
        self.__init_data(cst)
        self.__init_ui()

    def get_path(self) -> str:
        """获取结果路径"""
        self.result_path = self.path_edit.text()
        return self.result_path

    def __init_data(self, cst: CST.Contents):
        self.result_path = str(cst.project_dir)

    def __init_ui(self):
        # 路径选择区域
        main_layout = QHBoxLayout()

        # 左侧标记
        path_label = QLabel("结果路径:")
        path_label.setStyleSheet("font-weight: bold;")

        # 中间路径显示框
        self.path_edit = QLineEdit()
        self.path_edit.setText(self.result_path)
        self.path_edit.setPlaceholderText("请选择结果保存路径...")
        self.path_edit.textChanged.connect(self.__on_path_changed)

        # 右侧选择路径按钮
        path_select_btn = QPushButton("选择路径")
        path_select_btn.clicked.connect(self.__select_path)

        # 打开路径按钮
        open_path_btn = QPushButton("打开路径")
        open_path_btn.clicked.connect(self.__open_path)

        main_layout.addWidget(path_label)
        main_layout.addWidget(self.path_edit)
        main_layout.addWidget(path_select_btn)
        main_layout.addWidget(open_path_btn)

        self.setLayout(main_layout)

    def __select_path(self):
        """选择结果保存路径"""
        path = QFileDialog.getExistingDirectory(self, "选择结果保存路径", "")
        if path:
            self.path_edit.setText(path)

    def __open_path(self):
        """打开已选择的路径"""
        path = self.path_edit.text()
        if path and os.path.exists(path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(path))
        else:
            # 如果路径不存在，提示用户
            QMessageBox.warning(self, "路径不存在", "指定的路径不存在，请先选择有效的路径。")

    def __on_path_changed(self, path):
        """自定义路径改变时更新"""
        if Path(path).exists() and Path(path).is_dir():
            self.path_edit.setStyleSheet("border: 1px solid #4CAF50;")  # 清除错误样式
        else:
            self.path_edit.setStyleSheet("border: 1px solid red;")  # 设置错误样式
