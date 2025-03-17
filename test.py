import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QMenu, QAction, QApplication, QTextEdit
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置窗口属性
        self.setWindowTitle("菜单演示程序")
        self.setGeometry(100, 100, 600, 400)

        # 创建文本编辑区域用于演示数据操作
        self.textEdit = QTextEdit(self)
        self.textEdit.setGeometry(50, 50, 500, 300)

        # 创建文件按钮
        self.fileButton = QPushButton('文件', self)
        self.fileButton.setGeometry(10, 10, 60, 30)

        # 创建菜单
        self.fileMenu = QMenu(self)

        # 添加菜单项 - 上传数据
        uploadAction = QAction('上传数据', self)
        uploadAction.triggered.connect(self.uploadData)
        self.fileMenu.addAction(uploadAction)

        # 添加菜单项 - 保存数据
        saveAction = QAction('保存数据', self)
        saveAction.triggered.connect(self.saveData)
        self.fileMenu.addAction(saveAction)

        # 添加菜单项 - 清空数据
        clearAction = QAction('清空数据', self)
        clearAction.triggered.connect(self.clearData)
        self.fileMenu.addAction(clearAction)

        # 将菜单关联到按钮
        self.fileButton.setMenu(self.fileMenu)

    def uploadData(self):
        """模拟上传数据功能"""
        sample_text = "这是示例数据\n新加载的内容"
        self.textEdit.setText(sample_text)
        print("已加载示例数据")

    def saveData(self):
        """模拟保存数据功能"""
        current_text = self.textEdit.toPlainText()
        if current_text:
            print("保存的数据:\n", current_text)
        else:
            print("没有数据可保存")

    def clearData(self):
        """清空数据功能"""
        self.textEdit.clear()
        print("数据已清空")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()