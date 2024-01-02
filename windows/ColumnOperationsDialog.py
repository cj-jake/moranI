from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QComboBox, QPushButton, QLabel, QDesktopWidget


class ColumnOperationsDialog(QDialog):
    def __init__(self, columns, data, parent=None):
        super().__init__(parent)
        self.columns = columns
        self.data = data

        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, 200, 200)
        self.centerOnScreen()
        layout = QVBoxLayout()  # 使用垂直布局

        label = QLabel("选择要进行的列操作：", self)
        layout.addWidget(label)

        # 创建下拉列表以显示列名
        self.column_dropdown = QComboBox(self)
        self.column_dropdown.addItems(self.columns)
        layout.addWidget(self.column_dropdown)

        button = QPushButton("删除", self)
        button.clicked.connect(self.performOperation)
        layout.addStretch(1)  # 添加一个 stretch 将按钮推到底部
        layout.addWidget(button, alignment=QtCore.Qt.AlignHCenter)

        layout.addStretch(1)  # 添加一个 stretch 将按钮推到底部

        self.setLayout(layout)

        self.setWindowTitle("列操作对话框")

    def performOperation(self):
        # 在这里执行列操作，这里只是一个示例
        selected_column = self.column_dropdown.currentText()
        # 对选择的列进行操作，删除
        self.data.drop(columns=[selected_column], inplace=True)
        # 完成操作后，关闭对话框
        self.accept()

    def centerOnScreen(self):
        '''屏幕中间显示'''
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
