import sys
import os
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QFileDialog, QTextEdit
from PyQt5.QtCore import Qt


class ImageOverlayApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.threads = []

    def initUI(self):
        self.setWindowTitle('Image Overlay Tool')

        layout = QVBoxLayout()

        # 选择文件夹
        self.folder_label = QLabel('选择文件夹:')
        layout.addWidget(self.folder_label)

        self.folder_button = QPushButton('浏览')
        self.folder_button.clicked.connect(self.getFolderPath)
        layout.addWidget(self.folder_button)

        # 匹配字符和偏移值输入框
        self.input_layouts = []
        for i in range(7):
            input_layout = QHBoxLayout()
            layout.addLayout(input_layout)

            match_label = QLabel(f'匹配字符{i + 1}:')
            input_layout.addWidget(match_label)

            match_input = QLineEdit()
            input_layout.addWidget(match_input)

            x_label = QLabel('输入 x 轴偏移值:')
            input_layout.addWidget(x_label)

            x_input = QLineEdit()
            input_layout.addWidget(x_input)

            y_label = QLabel('输入 y 轴偏移值:')
            input_layout.addWidget(y_label)

            y_input = QLineEdit()
            input_layout.addWidget(y_input)

            self.input_layouts.append((match_input, x_input, y_input))

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
        self.folder_path = None

    def getFolderPath(self):
        folder_path = QFileDialog.getExistingDirectory(self, '选择文件夹')
        self.folder_path = folder_path

    def getOutputPath(self):
        directory = QFileDialog.getExistingDirectory(self, '选择输出路径')
        self.output_path = directory

    def overlayImages(self):
        if not self.folder_path:
            self.output_text.append('请选择文件夹')
            return

        if not self.output_path:
            self.output_text.append('请选择输出路径')
            return

        for match_input, x_input, y_input in self.input_layouts:
            match_text = match_input.text()
            x_offset = x_input.text()
            y_offset = y_input.text()

            if not match_text:
                self.output_text.append('请输入匹配字符')
                continue

            if not x_offset or not y_offset:
                self.output_text.append('请输入有效的偏移值')
                continue

            files_to_overlay = [filename for filename in os.listdir(self.folder_path) if match_text in filename]
            if len(files_to_overlay) < 2:
                self.output_text.append(f'未找到匹配字符"{match_text}"的文件或文件数量不足')
                continue

            first_image_path = os.path.join(self.folder_path, files_to_overlay[0])

            for filename in files_to_overlay[1:]:
                second_image_path = os.path.join(self.folder_path, filename)
                output_file = os.path.basename(first_image_path).split('.')[0] + "_overlay_" + os.path.basename(second_image_path)
                output_file_path = os.path.join(self.output_path, output_file)
                thread = threading.Thread(target=self.processImages, args=(first_image_path, second_image_path, x_offset, y_offset, output_file_path))
                thread.start()
                self.threads.append(thread)

        for thread in self.threads:
            thread.join()

        self.output_text.append('图片叠加完成')

    def processImages(self, first_image_path, second_image_path, x_offset, y_offset, output_file_path):
        ffmpeg_cmd = f'ffmpeg -i {first_image_path} -i {second_image_path} -filter_complex "overlay={x_offset}:{y_offset}" {output_file_path}'
        self.output_text.append(f'执行命令: {ffmpeg_cmd}')
        os.system(ffmpeg_cmd)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageOverlayApp()
    window.show()
    sys.exit(app.exec_())
