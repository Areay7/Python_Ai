import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QLabel, QListWidget, QMessageBox

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

        options_layout = QHBoxLayout()

        self.btn_rename_option1 = QPushButton('选项1: 去除尺码前的 "-"')
        self.btn_rename_option1.clicked.connect(self.renameOption1)
        options_layout.addWidget(self.btn_rename_option1)

        self.btn_rename_option2 = QPushButton('选项2: 在尺码前添加 "-"')
        self.btn_rename_option2.clicked.connect(self.renameOption2)
        options_layout.addWidget(self.btn_rename_option2)

        layout.addLayout(options_layout)

        self.setLayout(layout)

    def selectFiles(self):
        files, _ = QFileDialog.getOpenFileNames(self, '选择文件', '')
        if files:
            self.file_list.clear()
            self.file_list.addItems(files)

    def renameOption1(self):
        self.renameFiles(option=1)

    def renameOption2(self):
        self.renameFiles(option=2)

    def renameFiles(self, option):
        if self.file_list.count() == 0:
            QMessageBox.warning(self, '警告', '请先选择文件')
            return

        for i in range(self.file_list.count()):
            file_path = self.file_list.item(i).text()
            file_name, file_extension = os.path.splitext(os.path.basename(file_path))

            if option == 1:
                new_file_name = file_name.replace('-XL', 'XL').replace('-L', 'L').replace('-M', 'M').replace('-S', 'S')
            elif option == 2:
                new_file_name = file_name.replace('XL', '-XL').replace('L', '-L').replace('M', '-M').replace('S', '-S')

            try:
                os.rename(file_path, os.path.join(os.path.dirname(file_path), new_file_name + file_extension))
            except Exception as e:
                QMessageBox.critical(self, '错误', f'重命名文件失败: {e}')
                return

        QMessageBox.information(self, '提示', '文件重命名成功')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileRenameApp()
    ex.show()
    sys.exit(app.exec_())
