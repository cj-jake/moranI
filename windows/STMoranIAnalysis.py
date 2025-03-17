"""
时空莫兰指数
"""

import os
from datetime import datetime

import imageio
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton, QTextEdit, QDesktopWidget, \
    QHBoxLayout, QSpinBox, QLineEdit

from utils.ImplementSpatialWeightMatrix import *
from utils.calculateMoranI import *


class STMoranIAnalysis(QDialog):
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
        label_1 = QLabel("选择要计算 时空Moran 指数的数据列：", self)
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

        label_4 = QLabel("选择时间数据：", self)
        self.fourth_dropdown = QComboBox(self)
        self.fourth_dropdown.addItems(self.data.columns)  # 使用和第一个下拉框相同的数据
        layout.addWidget(label_4)
        layout.addWidget(self.fourth_dropdown)

        hbox = QHBoxLayout()
        score_label = QLabel("输入时间阈值（天）：", self)
        self.score_input = QLineEdit(self)
        self.score_input.setText("1")
        hbox.addWidget(score_label)
        hbox.addWidget(self.score_input)
        layout.addLayout(hbox)

        self.result_text = QTextEdit(self)
        layout.addWidget(self.result_text)

        self.calculate_button = QPushButton("计算 Moran 指数", self)
        self.calculate_button.clicked.connect(self.calculateMoranI)
        layout.addWidget(self.calculate_button)

        self.setLayout(layout)
        self.setWindowTitle("STMoranIAnalysis")

    def calculateMoranI(self):

        valueName = self.column_dropdown.currentText()
        xName = self.second_dropdown.currentText()
        yName=self.third_dropdown.currentText()
        tName=self.fourth_dropdown.currentText()
        value=self.data[valueName]
        coordinates = list(zip(self.data[xName], self.data[yName],self.data[tName]))
        #获得时间阈值
        input_time_text = self.score_input.text()
        time_Threshold =float(input_time_text)
        w = STBuildWeightMatrix(coordinates, 3, 2, time_Threshold)
        # 计算 Moran 指数
        data = np.array(value)
        data = data / data.sum(axis=0)  # 数据归一化
        moran_result = STMoranI(w, data)
        # 格式化显示结果
        formatted_result = ""
        for key, value in moran_result.items():
            if isinstance(value, list):
                formatted_result += f"{key}:\n"
                for item in value:
                    formatted_result += f"{item}\n"
            else:
                formatted_result += f"{key}: {value}\n"

        # 将格式化的结果设置到文本框中
        self.result_text.setPlainText(formatted_result)
        # 提取局部检验数数据
        ZIi_data = moran_result['时空局部检z分数']

        # 将数据分为 x、y、z 轴的数据
        x = list(self.data[xName])
        y = list(self.data[yName])
        z = value
        dataValue=ZIi_data
        # 创建 3D 图形对象
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # 绘制散点图
        ax.scatter(x,y,z, c=dataValue, cmap='viridis')

        #设计标题
        ax.set_title('3D local ST z-score')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        # 修改为:
        try:
            plt.show(block=False)
        except AttributeError:
            # 在发生AttributeError时使用备选方法
            plt.savefig('moran_i_plot.png')
            # 可选：显示保存的图片
            from PIL import Image
            img = Image.open('moran_i_plot.png')
            img.show()
        # 保存
        current_time = datetime.now()
        year = current_time.year
        month = current_time.month
        day = current_time.day
        hour = current_time.hour
        minute = current_time.minute
        second = current_time.second
        date_string = f"{year}_{month}_{day}"
        current_directory = os.getcwd()+'\\result'
        file_path=os.path.join(current_directory,date_string)
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        filename = os.path.join(file_path,f"{hour}_{minute}_{second}STMoranI.gif")
        frames = []
        for i in range(0, 360, 2):
            ax.view_init(elev=i, azim=i)
            fig.canvas.draw()
            frame = np.array(fig.canvas.renderer.buffer_rgba())
            frames.append(frame)


        imageio.mimsave(filename, frames, duration=50)  # Set the duration in milliseconds per frame



    def centerOnScreen(self):
            '''屏幕中间显示'''
            qr = self.frameGeometry()
            cp = QDesktopWidget().availableGeometry().center()
            qr.moveCenter(cp)
            self.move(qr.topLeft())
