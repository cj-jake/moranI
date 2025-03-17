import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QFileDialog, QTableWidget, \
    QTableWidgetItem, QWidget, QMessageBox, QHBoxLayout, QDesktopWidget, QDialog, QAction, QMenu
from windows.ColumnOperationsDialog import ColumnOperationsDialog
from windows.MoranIAnalysis import MoranIAnalysis
from windows.TMoranIAnalysis import TMoranIAnalysis
from windows.STMoranIAnalysis import STMoranIAnalysis

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.data = pd.DataFrame()

    def initUI(self):
        self.setWindowTitle("主用户界面")
        self.setGeometry(0, 0, 900, 900)
        self.centerOnScreen()


        layout = QVBoxLayout()

        # 创建一个水平布局用于放置文件按钮
        menu_layout = QHBoxLayout()
        # 设置布局中部件之间的间距为更小的值（默认是6像素）
        menu_layout.setSpacing(2)  # 减小按钮之间的间距

        # 创建并添加文件按钮
        self.fileButton = QPushButton('文件', self)
        self.createMenuBar()
        # 将文件按钮添加到菜单布局
        menu_layout.addWidget(self.fileButton)


        # 创建并添加数据列操作按钮 - 放在文件按钮之后
        self.column_operations_button = QPushButton("数据列操作", self)
        self.column_operations_button.clicked.connect(self.showColumnOperationsDialog)
        menu_layout.addWidget(self.column_operations_button)

        # 创建并添加模型分析按钮
        self.modelButton = QPushButton('模型分析', self)
        self.createModelMenu()  # 创建模型菜单
        menu_layout.addWidget(self.modelButton)

        menu_layout.addStretch(1)  # 添加弹性空间，使按钮靠左对齐
        # 将菜单布局添加到主布局
        layout.addLayout(menu_layout)


        # 创建一个QTableWidget对象，用于展示数据表格
        self.table = QTableWidget()
        # 将表格添加到布局中，使其在界面上可见
        layout.addWidget(self.table)



        # 创建一个QWidget对象作为容器，用于容纳上述的布局
        container = QWidget()
        # 将布局设置到容器中，这样容器就可以根据布局来调整其大小和位置
        container.setLayout(layout)
        # 将容器设置为窗口的中心部件，使其在窗口中居中显示
        self.setCentralWidget(container)



    def createMenuBar(self):
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

    def createModelMenu(self):
        # 创建菜单
        self.modelMenu = QMenu(self)

        models = ["SMoranI_LISA", "TMoranI_LISA", "STMoranI_LISA"]

        self.analysis_window_mapping = {
            "SMoranI_LISA": MoranIAnalysis,
            "TMoranI_LISA": TMoranIAnalysis,
            "STMoranI_LISA": STMoranIAnalysis
        }

        # 为每个模型添加菜单项
        for model in models:
            modelAction = QAction(f"{model}模型分析", self)
            # 使用lambda来传递模型名称
            modelAction.triggered.connect(lambda checked, m=model: self.openAnalysisWindow(m))
            self.modelMenu.addAction(modelAction)

        # 将菜单关联到按钮
        self.modelButton.setMenu(self.modelMenu)
    def uploadData(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, "选择文件", ".",
                                                   "Excel Files (*.xlsx *.xls);;CSV Files (*.csv);;All Files (*)")

        if file_path:
            if file_path.lower().endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.lower().endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file_path)
            else:
                print("不支持的文件格式")
                return

            common_columns = set(self.data.columns) & set(df.columns)
            if common_columns:
                QMessageBox.warning(self, "警告", f"数据中包含相同字段列: {', '.join(common_columns)}")
            else:
                self.data = pd.concat([self.data, df], axis=1)

            self.displayData(self.data)

    # 显示数据
    def displayData(self, df):
        '''显示数据'''
        if not self.data.empty:
            max_rows = 1000
            num_rows = min(len(df), max_rows)

            self.table.setRowCount(num_rows)
            self.table.setColumnCount(len(df.columns))

            for i, column in enumerate(df.columns):
                item = QTableWidgetItem(str(column))
                self.table.setHorizontalHeaderItem(i, item)

            for i in range(len(df.columns)):
                for j in range(num_rows):
                    item = QTableWidgetItem(str(df.iloc[j, i]))
                    self.table.setItem(j, i, item)


            self.table.resizeColumnsToContents()
            self.table.resizeRowsToContents()
        else:
            QMessageBox.warning(self, "提示", "请先上传数据！")



    def saveData(self):
        if not self.data.empty:
            #Sava data 数据 选择保存路径设置保存文件名称 格式为.csv
            file_dialog = QFileDialog(self)
            file_path, _ = file_dialog.getSaveFileName(self, "保存数据", ".", "CSV Files (*.csv);;All Files (*)")
            if file_path:
                self.data.to_csv(file_path, index=False)
            QMessageBox.information(self, "提示", "数据已保存到本地！")
        else:
            QMessageBox.warning(self, "提示", "请先上传数据！")

    def clearData(self):
        '''清空数据'''
        if not self.data.empty:
            if not self.table.horizontalHeaderItem(0):
                # 如果水平表头不存在，说明是第一次显示数据，设置水平表头
                self.table.setRowCount(0)
                self.table.setColumnCount(0)
                self.table.setHorizontalHeaderLabels([])
            else:
                # 如果水平表头已经存在，清除水平表头
                self.table.clearContents()
                self.table.setRowCount(0)
                self.table.setColumnCount(0)

            self.data = pd.DataFrame()
        else:
            QMessageBox.warning(self, "提示", "请先上传数据！")

    def showColumnOperationsDialog(self):
        if not self.data.empty:
            dialog = ColumnOperationsDialog(self.data.columns, self.data, self)
            result = dialog.exec_()

            if result == QDialog.Accepted:
                self.data = dialog.data  # Updated data from the dialog
                self.displayData(self.data)
                QMessageBox.information(self, "提示", "数据列修改完成！")
        else:
            QMessageBox.warning(self, "提示", "请先上传数据！")


    def openAnalysisWindow(self,model):
        if not self.data.empty:
            analysis_window_class = self.analysis_window_mapping.get(model)

            if analysis_window_class:
                analysis_window = analysis_window_class(self.data)
                analysis_window.exec_()
        else:
            QMessageBox.warning(self, "提示", "请先上传数据！")



    def centerOnScreen(self):
        '''屏幕中间显示'''
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())





if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
