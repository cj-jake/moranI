import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QFileDialog, QTableWidget, \
    QTableWidgetItem, QWidget, QMessageBox, QHBoxLayout, QDesktopWidget, QDialog, QAction
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
        self.createMenuBar()



        layout = QVBoxLayout()
        # 创建一个水平布局来放置上传、清空和保存按钮
        button_layout1 = QHBoxLayout()

        self.upload_button = QPushButton("上传数据", self)
        self.upload_button.clicked.connect(self.uploadData)
        button_layout1.addWidget(self.upload_button)

        self.clear_button = QPushButton("清空数据", self)
        self.clear_button.clicked.connect(self.clearData)
        button_layout1.addWidget(self.clear_button)

        self.save_button = QPushButton("保存数据", self)
        self.save_button.clicked.connect(self.saveData)
        button_layout1.addWidget(self.save_button)

        # 将水平布局添加到垂直布局中
        layout.addLayout(button_layout1)

        # 创建一个QTableWidget对象，用于展示数据表格
        self.table = QTableWidget()

        # 将表格添加到布局中，使其在界面上可见
        layout.addWidget(self.table)

        self.column_operations_button = QPushButton("数据列操作", self)
        self.column_operations_button.clicked.connect(self.showColumnOperationsDialog)
        layout.addWidget(self.column_operations_button)

        # 创建一个水平布局来放置上传、清空和保存按钮
        button_layout2 = QHBoxLayout()

        models = ["SMoranI_LISA",  "TMoranI_LISA","STMoranI_LISA"]

        self.analysis_window_mapping = {
            "SMoranI_LISA": MoranIAnalysis,
            "TMoranI_LISA": TMoranIAnalysis,
            "STMoranI_LISA": STMoranIAnalysis
        }

        for model in models:
            analysis_button = QPushButton(f"{model}模型分析", self)
            analysis_button.clicked.connect(self.openAnalysisWindow)
            button_layout2.addWidget(analysis_button)



        layout.addLayout(button_layout2)


        # 创建一个QWidget对象作为容器，用于容纳上述的布局
        container = QWidget()
        # 将布局设置到容器中，这样容器就可以根据布局来调整其大小和位置
        container.setLayout(layout)
        # 将容器设置为窗口的中心部件，使其在窗口中居中显示
        self.setCentralWidget(container)



    def createMenuBar(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('文件')

        uploadAction = QAction('上传数据', self)
        uploadAction.triggered.connect(self.uploadData)
        fileMenu.addAction(uploadAction)

        saveAction = QAction('保存数据', self)
        saveAction.triggered.connect(self.saveData)
        fileMenu.addAction(saveAction)

        clearAction = QAction('清空数据', self)
        clearAction.triggered.connect(self.clearData)
        fileMenu.addAction(clearAction)
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
            max_rows = 100
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


    def openAnalysisWindow(self):
        if not self.data.empty:
            sender_button = self.sender()
            model = sender_button.text().split('模型')[0]


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
