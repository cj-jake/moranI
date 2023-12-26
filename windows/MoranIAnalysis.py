from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton, QTextEdit, QDesktopWidget

from utils.KnnImplementSpatialWeightMatrix import *
from utils.calculateMoranI import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class MoranIAnalysis(QDialog):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data

        self.initUI()

    def initUI(self):
        self.setWindowTitle("主用户界面")
        self.setGeometry(0, 0, 600, 600)
        self.centerOnScreen()
        layout = QVBoxLayout()

        # First label and dropdown
        label_1 = QLabel("选择要计算 Moran 指数的数据列：", self)
        self.column_dropdown = QComboBox(self)
        self.column_dropdown.addItems(self.data.columns)

        layout.addWidget(label_1)
        layout.addWidget(self.column_dropdown)

        # Second label and dropdown with the same data
        label_2 = QLabel("选择x坐标数据：", self)
        self.second_dropdown = QComboBox(self)
        self.second_dropdown.addItems(self.data.columns)  # Using the same data as the first dropdown
        layout.addWidget(label_2)
        layout.addWidget(self.second_dropdown)

        # Third label and dropdown with the same data
        label_3 = QLabel("选择y坐标数据：", self)
        self.third_dropdown = QComboBox(self)
        self.third_dropdown.addItems(self.data.columns)  # Using the same data as the first dropdown
        layout.addWidget(label_3)
        layout.addWidget(self.third_dropdown)

        self.result_text = QTextEdit(self)
        layout.addWidget(self.result_text)

        self.calculate_button = QPushButton("计算 Moran 指数", self)
        self.calculate_button.clicked.connect(self.calculateMoranI)
        layout.addWidget(self.calculate_button)

        self.setLayout(layout)
        self.setWindowTitle("MoranIAnalysis")

    def calculateMoranI(self):
        valueName = self.column_dropdown.currentText()
        xName = self.second_dropdown.currentText()
        yName=self.third_dropdown.currentText()
        value=self.data[valueName]
        coordinates = list(zip(self.data[xName], self.data[yName]))
        w = knn(coordinates, method=2)
        # 计算 Moran 指数
        data = np.array(value)
        data = data / data.sum(axis=0)  # 数据归一化
        moran_result = MoranI(w, data)
        print(moran_result)
        self.result_text.setPlainText(str(moran_result))
        # 提取局部检验数数据
        ZIi_data = moran_result['ZIi']['value']

        # 将数据分为 x、y、z 轴的数据
        x = range(len(ZIi_data))
        y = range(len(ZIi_data))
        z = ZIi_data

        # 创建 3D 图形对象
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # 绘制三维散点图
        ax.scatter(x, y, z)

        # 设置图表标题和轴标签
        ax.set_title('3D Scatter Plot of ZIi Data')
        ax.set_xlabel('X Axis')
        ax.set_ylabel('Y Axis')
        ax.set_zlabel('Z Axis')
        # 显示图形
        plt.show()



    def centerOnScreen(self):
            '''屏幕中间显示'''
            qr = self.frameGeometry()
            cp = QDesktopWidget().availableGeometry().center()
            qr.moveCenter(cp)
            self.move(qr.topLeft())
