#PyQt5

import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar

class SinPlot(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置主窗口标题
        self.setWindowTitle('Sin Plot')

        # 创建主窗口中的组件
        self.central_widget = SinPlotWidget(self)
        self.setCentralWidget(self.central_widget)

        # 显示窗口
        self.show()

class SinPlotWidget(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        # 创建一个 Figure
        self.fig = Figure(figsize=(width, height), dpi=dpi)

        # 在 Figure 中添加一个 Axes
        self.ax = self.fig.add_subplot(111)

        # 初始化图形背景色为白色
        self.fig.set_facecolor('white')

        # 初始化图形区域的背景色为黄色
        self.ax.set_facecolor('yellow')

        # 调用 FigureCanvas 的构造函数
        super().__init__(self.fig)

        # 设置父窗口
        self.setParent(parent)

        # 开启交互模式
        self.setMouseTracking(True)

        # 绘制正弦曲线
        self.plot_sine_wave()

        # 定义文本标注
        self.annotation = self.ax.annotate('', xy=(0, 0), xytext=(20, 20),
                                           textcoords='offset points', ha='center', va='center',
                                           bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                                           arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

        # 为图形添加事件处理程序
        self.cid_motion = self.mpl_connect('motion_notify_event', self.on_mouse_motion)

    def plot_sine_wave(self):
        x = np.linspace(0, 2 * np.pi, 100)
        y = np.sin(x)

        # 绘制正弦曲线
        self.ax.plot(x, y)

        # 刷新图形
        self.draw()

    def on_mouse_motion(self, event):
        if event.inaxes == self.ax:
            x, y = event.xdata, event.ydata
            if x is not None and y is not None:
                value = f'x={x:.2f}, y={y:.2f}'
                self.annotation.set_text(value)
                self.annotation.xy = (x, y)
                self.annotation.set_visible(True)
                self.draw()
        else:
            self.annotation.set_visible(False)
            self.draw()

    def enterEvent(self, event):
        # 鼠标进入图形区域时将图形背景色设置为黄色
        self.fig.set_facecolor('yellow')
        self.ax.set_facecolor('yellow')
        self.draw()

    def leaveEvent(self, event):
        # 鼠标离开图形区域时将图形背景色恢复为白色
        self.fig.set_facecolor('white')
        self.ax.set_facecolor('white')
        self.annotation.set_visible(False)
        self.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = SinPlot()
    sys.exit(app.exec_())
