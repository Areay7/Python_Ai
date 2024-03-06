import sys
import os
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal, QObject

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


class BatchRenameApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('批量重命名工具')
        layout = QVBoxLayout()

        self.path_label = QLabel('路径:')
        layout.addWidget(self.path_label)
        self.path_input = QLineEdit()
        layout.addWidget(self.path_input)
        self.path_button = QPushButton('选择路径')
        self.path_button.clicked.connect(self.choosePath)
        layout.addWidget(self.path_button)

        self.match_rule1_label = QLabel('匹配规则1:')
        layout.addWidget(self.match_rule1_label)
        self.match_rule1_input = QLineEdit()
        layout.addWidget(self.match_rule1_input)

        self.replace_with1_label = QLabel('替换为1:')
        layout.addWidget(self.replace_with1_label)
        self.replace_with1_input = QLineEdit()
        layout.addWidget(self.replace_with1_input)

        self.match_rule2_label = QLabel('匹配规则2:')
        layout.addWidget(self.match_rule2_label)
        self.match_rule2_input = QLineEdit()
        layout.addWidget(self.match_rule2_input)

        self.replace_with2_label = QLabel('替换为2:')
        layout.addWidget(self.replace_with2_label)
        self.replace_with2_input = QLineEdit()
        layout.addWidget(self.replace_with2_input)

        self.output_path_label = QLabel('输出路径:')
        layout.addWidget(self.output_path_label)
        self.output_path_input = QLineEdit()
        layout.addWidget(self.output_path_input)
        self.output_path_button = QPushButton('选择输出路径')
        self.output_path_button.clicked.connect(self.chooseOutputPath)
        layout.addWidget(self.output_path_button)

        self.confirm_button = QPushButton('确认转换')
        self.confirm_button.clicked.connect(self.startRenameThread)
        layout.addWidget(self.confirm_button)

        self.setLayout(layout)

    def choosePath(self):
        directory = QFileDialog.getExistingDirectory(self, '选择路径')
        self.path_input.setText(directory)

    def chooseOutputPath(self):
        directory = QFileDialog.getExistingDirectory(self, '选择输出路径')
        self.output_path_input.setText(directory)

    def startRenameThread(self):
        path = self.path_input.text()
        match_rule1 = self.match_rule1_input.text()
        replace_with1 = self.replace_with1_input.text()
        match_rule2 = self.match_rule2_input.text()
        replace_with2 = self.replace_with2_input.text()
        output_path = self.output_path_input.text()
        if not os.path.exists(path):
            QMessageBox.warning(self, '警告', '路径不存在！')
            return
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        thread = RenameThread(path, match_rule1, replace_with1, match_rule2, replace_with2, output_path)
        thread.communicate.finished.connect(self.showMessageBox)
        thread.start()

    def showMessageBox(self, success):
        if success:
            QMessageBox.information(self, '提示', '转换成功')
        else:
            QMessageBox.critical(self, '错误', '转换失败')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BatchRenameApp()
    window.show()
    sys.exit(app.exec_())
