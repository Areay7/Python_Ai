import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QFileDialog, QTextEdit
from PyQt5.QtCore import Qt


class ImageOverlayApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Image Overlay Tool')

        layout = QVBoxLayout()

        # 图片1选择
        self.image1_label = QLabel('选择第一张图片:')
        layout.addWidget(self.image1_label)

        self.image1_button = QPushButton('浏览')
        self.image1_button.clicked.connect(self.getImage1Path)
        layout.addWidget(self.image1_button)

        # 图片2选择
        self.image2_label = QLabel('选择第二张图片:')
        layout.addWidget(self.image2_label)

        self.image2_button = QPushButton('浏览')
        self.image2_button.clicked.connect(self.getImage2Path)
        layout.addWidget(self.image2_button)

        # x轴输入框
        self.x_label = QLabel('输入 x 轴偏移值:')
        layout.addWidget(self.x_label)

        self.x_input = QLineEdit()
        layout.addWidget(self.x_input)

        # y轴输入框
        self.y_label = QLabel('输入 y 轴偏移值:')
        layout.addWidget(self.y_label)

        self.y_input = QLineEdit()
        layout.addWidget(self.y_input)

        # 输出路径选择
        self.output_label = QLabel('选择输出路径:')
        layout.addWidget(self.output_label)

        self.output_button = QPushButton('浏览')
        self.output_button.clicked.connect(self.getOutputPath)
        layout.addWidget(self.output_button)

        # FFmpeg输出文本框
        self.output_text = QTextEdit()
        layout.addWidget(self.output_text)

        # 开始叠加按钮
        self.overlay_button = QPushButton('开始叠加')
        self.overlay_button.clicked.connect(self.overlayImages)
        layout.addWidget(self.overlay_button)

        self.setLayout(layout)

    def getImage1Path(self):
        file_path, _ = QFileDialog.getOpenFileName(self, '选择第一张图片')
        self.image1_path = file_path

    def getImage2Path(self):
        file_path, _ = QFileDialog.getOpenFileName(self, '选择第二张图片')
        self.image2_path = file_path

    def getOutputPath(self):
        directory = QFileDialog.getExistingDirectory(self, '选择输出路径')
        self.output_path = directory

    def overlayImages(self):
        x_offset = self.x_input.text()
        y_offset = self.y_input.text()

        if not os.path.exists(self.image1_path) or not os.path.exists(self.image2_path):
            self.output_text.append('请选择有效的图片路径')
            return

        if not x_offset or not y_offset:
            self.output_text.append('请输入有效的偏移值')
            return

        if not self.output_path:
            self.output_text.append('请选择输出路径')
            return

        output_file = os.path.join(self.output_path, 'output.jpg')

        ffmpeg_cmd = f'ffmpeg -i {self.image1_path} -i {self.image2_path} -filter_complex "overlay={x_offset}:{y_offset}" {output_file}'
        self.output_text.append(f'执行命令: {ffmpeg_cmd}')
        os.system(ffmpeg_cmd)
        self.output_text.append('图片叠加完成')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageOverlayApp()
    window.show()
    sys.exit(app.exec_())
