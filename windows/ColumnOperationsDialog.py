from PyQt5.QtWidgets import QDialog, QVBoxLayout, QComboBox, QPushButton, QLabel

class ColumnOperationsDialog(QDialog):
    def __init__(self, columns, data, parent=None):
        super().__init__(parent)
        self.columns = columns
        self.data = data

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        label = QLabel("选择要进行的列操作：", self)
        layout.addWidget(label)

        # 创建下拉列表以显示列名
        self.column_dropdown = QComboBox(self)
        self.column_dropdown.addItems(self.columns)
        layout.addWidget(self.column_dropdown)

        # 创建按钮，执行列操作
        self.operation_button = QPushButton("执行操作", self)
        self.operation_button.clicked.connect(self.performOperation)
        layout.addWidget(self.operation_button)

        self.setLayout(layout)
        self.setWindowTitle("列操作对话框")

    def performOperation(self):
        # 在这里执行列操作，这里只是一个示例
        selected_column = self.column_dropdown.currentText()
        # 对选择的列进行操作，可以在这里添加你的操作逻辑

        # 完成操作后，关闭对话框
        self.accept()
