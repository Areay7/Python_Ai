import sys
import os
import threading
import qrcode
from PyQt5.QtWidgets import QProgressBar
from PIL import Image, ImageDraw, ImageFont
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog, QMessageBox, QTextEdit, QHBoxLayout
from PyQt5.QtCore import pyqtSignal, QObject, Qt, QThread

class Communicate(QObject):
    finished = pyqtSignal(bool)

class RenameThread(threading.Thread):
    def __init__(self, path, match_rule1, replace_with1, match_rule2, replace_with2, output_path, parent=None):
        super(RenameThread, self).__init__(parent)
        self.path = path
        self.match_rule1 = match_rule1
        self.replace_with1 = replace_with1
        self.match_rule2 = match_rule2
        self.replace_with2 = replace_with2
        self.output_path = output_path
        self.communicate = Communicate()

    def run(self):
        try:
            for filename in os.listdir(self.path):
                new_name = filename.replace(self.match_rule1, self.replace_with1)
                new_name = new_name.replace(self.match_rule2, self.replace_with2)
                old_file_path = os.path.join(self.path, filename)
                new_file_path = os.path.join(self.output_path, new_name)
                os.rename(old_file_path, new_file_path)
            self.communicate.finished.emit(True)
        except Exception as e:
            self.communicate.finished.emit(False)

class QRCodeThread(QThread):
    progress_update = pyqtSignal(int)

    def __init__(self, file_name, qr_size, font_size, generate_path):
        super().__init__()
        self.file_name = file_name
        self.qr_size = qr_size
        self.font_size = font_size
        self.generate_path = generate_path

    def run(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(self.file_name)
        qr.make(fit=True)

        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_img = qr_img.resize((self.qr_size, self.qr_size))

        draw = ImageDraw.Draw(qr_img)
        font_path = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
        font = ImageFont.truetype(font_path, self.font_size)
        text_width, text_height = draw.textsize(self.file_name, font=font)

        # 计算文本位置，将文本放置在整张图的底部中间
        image_width, image_height = qr_img.size
        text_position = ((image_width - text_width) // 2, image_height - text_height - 10)

        draw.text(text_position, self.file_name, font=font, fill="black")

        save_path = os.path.join(self.generate_path, f"{self.file_name}.jpg")
        qr_img.save(save_path)
        print(f"二维码已生成至：{save_path}")

        self.progress_update.emit(100)

class ImageOverlayApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.threads = []

    def initUI(self):
        self.setWindowTitle('批量重命名工具、二维码生成器和图片叠加工具')

        layout = QVBoxLayout()

        # 批量重命名部分
        self.rename_layout = QVBoxLayout()
        self.rename_label = QLabel('批量重命名工具')
        self.rename_layout.addWidget(self.rename_label)

        self.path_label = QLabel('路径:')
        self.rename_layout.addWidget(self.path_label)
        self.path_input = QLineEdit()
        self.rename_layout.addWidget(self.path_input)
        self.path_button = QPushButton('选择路径')
        self.path_button.clicked.connect(self.choosePath)
        self.rename_layout.addWidget(self.path_button)

        # 增加匹配规则和替换为
        self.match_rule1_label = QLabel('匹配规则1:')
        self.rename_layout.addWidget(self.match_rule1_label)
        self.match_rule1_input = QLineEdit()
        self.rename_layout.addWidget(self.match_rule1_input)

        self.replace_with1_label = QLabel('替换为1:')
        self.rename_layout.addWidget(self.replace_with1_label)
        self.replace_with1_input = QLineEdit()
        self.rename_layout.addWidget(self.replace_with1_input)

        self.match_rule2_label = QLabel('匹配规则2:')
        self.rename_layout.addWidget(self.match_rule2_label)
        self.match_rule2_input = QLineEdit()
        self.rename_layout.addWidget(self.match_rule2_input)

        self.replace_with2_label = QLabel('替换为2:')
        self.rename_layout.addWidget(self.replace_with2_label)
        self.replace_with2_input = QLineEdit()
        self.rename_layout.addWidget(self.replace_with2_input)

        self.output_path_label = QLabel('输出路径:')
        self.rename_layout.addWidget(self.output_path_label)
        self.output_path_input = QLineEdit()
        self.rename_layout.addWidget(self.output_path_input)
        self.output_path_button = QPushButton('选择输出路径')
        self.output_path_button.clicked.connect(self.chooseOutputPath)
        self.rename_layout.addWidget(self.output_path_button)

        self.confirm_button = QPushButton('确认转换')
        self.confirm_button.clicked.connect(self.confirmRename)
        self.rename_layout.addWidget(self.confirm_button)

        layout.addLayout(self.rename_layout)

        # 二维码生成部分
        self.qr_layout = QVBoxLayout()
        self.qr_label = QLabel('二维码生成器')
        self.qr_layout.addWidget(self.qr_label)

        self.file_name_label = QLabel("文件名:")
        self.qr_layout.addWidget(self.file_name_label)
        self.file_name_input = QLineEdit()
        self.qr_layout.addWidget(self.file_name_input)
        self.qr_size_label = QLabel("二维码大小:")
        self.qr_layout.addWidget(self.qr_size_label)
        self.qr_size_input = QLineEdit()
        self.qr_layout.addWidget(self.qr_size_input)
        self.font_size_label = QLabel("字体大小:")
        self.qr_layout.addWidget(self.font_size_label)
        self.font_size_input = QLineEdit()
        self.qr_layout.addWidget(self.font_size_input)
        self.generate_path_label = QLabel("生成路径:")
        self.qr_layout.addWidget(self.generate_path_label)
        self.generate_path_input = QLineEdit()
        self.qr_layout.addWidget(self.generate_path_input)
        self.generate_path_button = QPushButton("浏览")
        self.generate_path_button.clicked.connect(self.open_file_dialog)
        self.qr_layout.addWidget(self.generate_path_button)
        self.generate_button = QPushButton("生成")
        self.generate_button.clicked.connect(self.generate_qr_code)
        self.qr_layout.addWidget(self.generate_button)
        self.progress_bar = QProgressBar()
        self.qr_layout.addWidget(self.progress_bar)

        layout.addLayout(self.qr_layout)

        # 图片叠加部分
        self.overlay_layout = QVBoxLayout()
        self.overlay_label = QLabel('图片叠加工具')
        self.overlay_layout.addWidget(self.overlay_label)

        self.folder_label = QLabel('选择文件夹:')
        self.overlay_layout.addWidget(self.folder_label)

        self.folder_button = QPushButton('浏览')
        self.folder_button.clicked.connect(self.getFolderPath)
        self.overlay_layout.addWidget(self.folder_button)

        self.input_layouts = []
        for i in range(7):
            input_layout = QHBoxLayout()
            self.overlay_layout.addLayout(input_layout)

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

        self.output_label = QLabel('选择输出路径:')
        self.overlay_layout.addWidget(self.output_label)
        self.output_button = QPushButton('浏览')
        self.output_button.clicked.connect(self.getOutputPath)
        self.overlay_layout.addWidget(self.output_button)

        self.output_text = QTextEdit()
        self.overlay_layout.addWidget(self.output_text)

        self.overlay_button = QPushButton('开始叠加')
        self.overlay_button.clicked.connect(self.overlayImages)
        self.overlay_layout.addWidget(self.overlay_button)

        layout.addLayout(self.overlay_layout)

        self.setLayout(layout)
        self.folder_path = None

    def confirmRename(self):
        path = self.path_input.text()
        match_rule1 = self.match_rule1_input.text()
        replace_with1 = self.replace_with1_input.text()
        match_rule2 = self.match_rule2_input.text()
        replace_with2 = self.replace_with2_input.text()
        output_path = self.output_path_input.text()

        if not all([path, match_rule1, replace_with1, match_rule2, replace_with2, output_path]):
            QMessageBox.warning(self, "警告", "请填写所有字段")
            return

        thread = RenameThread(path, match_rule1, replace_with1, match_rule2, replace_with2, output_path)
        thread.communicate.finished.connect(self.renameFinished)
        thread.start()

    # 增加一个新的槽函数renameFinished，用于处理重命名完成后的操作
    def renameFinished(self, success):
        if success:
            QMessageBox.information(self, "提示", "批量重命名完成")
        else:
            QMessageBox.warning(self, "警告", "批量重命名失败")

    def choosePath(self):
        directory = QFileDialog.getExistingDirectory(self, '选择路径')
        self.path_input.setText(directory)

    def chooseOutputPath(self):
        directory = QFileDialog.getExistingDirectory(self, '选择输出路径')
        self.output_path_input.setText(directory)

    def open_file_dialog(self):
        options = QFileDialog.Options()
        folder_path = QFileDialog.getExistingDirectory(self, "选择生成路径", options=options)
        if folder_path:
            self.generate_path_input.setText(folder_path)

    def generate_qr_code(self):
        self.generate_button.setEnabled(False)
        self.progress_bar.setValue(0)

        file_name = self.file_name_input.text()
        qr_size = int(self.qr_size_input.text() or 200)
        font_size = int(self.font_size_input.text() or 12)
        generate_path = self.generate_path_input.text()

        self.thread = QRCodeThread(file_name, qr_size, font_size, generate_path)
        self.thread.progress_update.connect(self.update_progress)
        self.thread.finished.connect(self.process_finished)
        self.thread.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def process_finished(self):
        self.generate_button.setEnabled(True)

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