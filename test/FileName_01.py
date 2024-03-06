import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QLabel, QListWidget, QLineEdit, QMessageBox

class FileRenameApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('文件重命名工具')
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.btn_select_files = QPushButton('选择文件')
        self.btn_select_files.clicked.connect(self.selectFiles)
        layout.addWidget(self.btn_select_files)

        self.file_list = QListWidget()
        layout.addWidget(self.file_list)

        self.filter_layout = QHBoxLayout()
        self.lbl_new_suffix = QLabel('新文件后缀名前三个字符:')
        self.filter_layout.addWidget(self.lbl_new_suffix)
        self.txt_new_suffix = QLineEdit()
        self.filter_layout.addWidget(self.txt_new_suffix)
        layout.addLayout(self.filter_layout)

        self.lbl_filter_words = QLabel('过滤单词（用,分隔）:')
        layout.addWidget(self.lbl_filter_words)

        self.txt_filter_words = QLineEdit()
        layout.addWidget(self.txt_filter_words)

        self.btn_rename = QPushButton('重命名文件')
        self.btn_rename.clicked.connect(self.renameFiles)
        layout.addWidget(self.btn_rename)

        self.setLayout(layout)

    def selectFiles(self):
        files, _ = QFileDialog.getOpenFileNames(self, '选择文件', '')
        if files:
            self.file_list.clear()
            self.file_list.addItems(files)

    def renameFiles(self):
        if self.file_list.count() == 0:
            QMessageBox.warning(self, '警告', '请先选择文件')
            return

        new_suffix_prefix = self.txt_new_suffix.text().strip()
        if len(new_suffix_prefix) != 3:
            QMessageBox.warning(self, '警告', '新文件后缀名前三个字符长度必须为3')
            return

        filter_words = self.txt_filter_words.text().split(',')
        filter_words = [word.strip() for word in filter_words if word.strip()]

        for i in range(self.file_list.count()):
            file_path = self.file_list.item(i).text()
            file_name, file_extension = os.path.splitext(os.path.basename(file_path))
            if len(file_extension) < 3:
                QMessageBox.warning(self, '警告', '不是有效的文件')
                continue

            file_name_parts = file_name.split('.')
            new_file_name_parts = []
            for part in file_name_parts:
                if part in filter_words:
                    new_file_name_parts.append(part)
                else:
                    new_file_name_parts.append(part[:-3] + new_suffix_prefix)
            new_file_name = '.'.join(new_file_name_parts) + file_extension

            try:
                os.rename(file_path, os.path.join(os.path.dirname(file_path), new_file_name))
            except Exception as e:
                QMessageBox.critical(self, '错误', f'重命名文件失败: {e}')
                return

        QMessageBox.information(self, '提示', '文件重命名成功')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileRenameApp()
    ex.show()
    sys.exit(app.exec_())
