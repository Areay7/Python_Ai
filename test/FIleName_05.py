import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QLabel, \
    QListWidget, QMessageBox


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

        self.btn_add_prefix = QPushButton('添加尺码前缀')
        self.btn_add_prefix.clicked.connect(self.addPrefix)
        layout.addWidget(self.btn_add_prefix)

        self.btn_remove_prefix = QPushButton('移除尺码前缀')
        self.btn_remove_prefix.clicked.connect(self.removePrefix)
        layout.addWidget(self.btn_remove_prefix)

        self.setLayout(layout)

    def selectFiles(self):
        files, _ = QFileDialog.getOpenFileNames(self, '选择文件', '')
        if files:
            self.file_list.clear()
            self.file_list.addItems(files)

    def addPrefix(self):
        self.modifyFileNames(add_prefix=True)

    def removePrefix(self):
        self.modifyFileNames(add_prefix=False)

    def modifyFileNames(self, add_prefix=True):
        if self.file_list.count() == 0:
            QMessageBox.warning(self, '警告', '请先选择文件')
            return

        for i in range(self.file_list.count()):
            file_path = self.file_list.item(i).text()
            file_name, file_extension = os.path.splitext(os.path.basename(file_path))

            # 提取尺码信息
            sizes = ['5XL', '4XL', '3XL', '2XL', 'XL', 'L5', 'L4', 'L3', 'L2', 'L', 'M', 'S']
            modified_file_name = file_name
            for size in sizes:
                if size in modified_file_name:
                    size_index = modified_file_name.index(size)
                    if add_prefix:
                        if modified_file_name[size_index - 1] != '-':
                            modified_file_name = modified_file_name[:size_index] + '-' + modified_file_name[size_index:]
                    else:
                        if modified_file_name[size_index - 1] == '-':
                            modified_file_name = modified_file_name[:size_index - 1] + modified_file_name[size_index:]

                    # 如果找到了尺码并进行了操作，跳出循环，继续下一个文件
                    break

            new_file_name = modified_file_name + file_extension

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
