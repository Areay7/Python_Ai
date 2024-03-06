import os
import sys
import qrcode
from PIL import Image, ImageDraw, ImageFont
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFileDialog, QProgressBar
from PyQt5.QtCore import QThread, pyqtSignal

class QRCodeGenerator(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QR Code Generator")
        self.setGeometry(100, 100, 400, 250)

        self.file_name_label = QLabel("文件名:")
        self.file_name_input = QLineEdit()
        self.qr_size_label = QLabel("二维码大小:")
        self.qr_size_input = QLineEdit()
        self.font_size_label = QLabel("字体大小:")
        self.font_size_input = QLineEdit()
        self.generate_path_label = QLabel("生成路径:")
        self.generate_path_input = QLineEdit()
        self.generate_path_button = QPushButton("浏览")
        self.generate_button = QPushButton("生成")
        self.progress_bar = QProgressBar()

        layout = QVBoxLayout()
        layout.addWidget(self.file_name_label)
        layout.addWidget(self.file_name_input)
        layout.addWidget(self.qr_size_label)
        layout.addWidget(self.qr_size_input)
        layout.addWidget(self.font_size_label)
        layout.addWidget(self.font_size_input)
        layout.addWidget(self.generate_path_label)
        layout.addWidget(self.generate_path_input)
        layout.addWidget(self.generate_path_button)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.progress_bar)

        self.generate_path_button.clicked.connect(self.open_file_dialog)
        self.generate_button.clicked.connect(self.generate_qr_code)

        self.setLayout(layout)

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QRCodeGenerator()
    window.show()
    sys.exit(app.exec_())
