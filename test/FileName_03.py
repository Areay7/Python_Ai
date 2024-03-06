import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QListWidget, QMessageBox


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

        self.btn_add_suffix = QPushButton('添加尺码后缀')
        self.btn_add_suffix.clicked.connect(lambda: self.modifyFileNames(add_suffix=True))
        layout.addWidget(self.btn_add_suffix)

        self.btn_remove_suffix = QPushButton('移除尺码后缀')
        self.btn_remove_suffix.clicked.connect(lambda: self.modifyFileNames(add_suffix=False))
        layout.addWidget(self.btn_remove_suffix)

        self.setLayout(layout)

    def selectFiles(self):
        files, _ = QFileDialog.getOpenFileNames(self, '选择文件', '')
        if files:
            self.file_list.clear()
            self.file_list.addItems(files)

    def modifyFileNames(self, add_suffix=True):
        if self.file_list.count() == 0:
            QMessageBox.warning(self, '警告', '请先选择文件')
            return

        for i in range(self.file_list.count()):
            file_path = self.file_list.item(i).text()
            file_name, file_extension = os.path.splitext(os.path.basename(file_path))

            # 处理文件名，不包含后缀名
            name_without_extension = file_name[:-(len(file_extension))] if len(file_extension) > 0 else file_name

            # 对文件名除后缀名以外的后三个字符进行操作
            if len(name_without_extension) >= 4:  # 确保文件名足够长
                suffix = name_without_extension[-3:]
                sizes = ['5XL', '4XL', '3XL', '2XL', 'XL', 'L5', 'L4', 'L3', 'L2', 'L', 'M', 'S']
                if suffix in sizes:
                    if add_suffix:
                        if name_without_extension[-4] != '-':
                            name_without_extension = name_without_extension[:-3] + '-' + name_without_extension[-3:]
                    else:
                        if name_without_extension[-4] == '-':
                            name_without_extension = name_without_extension[:-4] + name_without_extension[-3:]

                # 重新构建文件名，包含后缀名
                new_file_name = name_without_extension + file_extension

                try:
                    os.rename(file_path, os.path.join(os.path.dirname(file_path), new_file_name))
                except Exception as e:
                    QMessageBox.critical(self, '错误', f'重命名文件失败: {e}')
                    return
            else:
                QMessageBox.warning(self, '警告', f'文件名太短无法操作: {file_path}')

        QMessageBox.information(self, '提示', '文件重命名成功')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileRenameApp()
    ex.show()
    sys.exit(app.exec_())
