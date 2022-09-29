from glob import glob
import os
import subprocess
import sys
from typing import List

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))


def get_kfb_file(root_path) -> List[str]:
    """获取文件夹下的所有kfb文件"""
    files = sorted(glob(os.path.join(root_path, "*.kfb")))
    return files


class MainWindow(QDialog):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.resize(400, 70)
        self.setWindowTitle("KFB转SVS")
        self.btn = QPushButton("点我选择文件夹", self)  # 点击按钮
        self.label = QLabel("处理进度")
        self.file_dialog = QFileDialog(self)  # 打开文件对话框
        self.createProgressBar()  # 进度条

        # 设置点击事件
        self.btn.clicked.connect(self.click_btn)

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.btn, 0, 0)
        mainLayout.addWidget(self.label, 1, 0)
        mainLayout.addWidget(self.progressBar, 3, 0)
        self.setLayout(mainLayout)

    def click_btn(self):
        root_path = self.file_dialog.getExistingDirectory(self, "选择文件夹路径", "./")
        # print(root_path)
        files = get_kfb_file(root_path)
        # print(files)
        file_cnt = len(files)
        print(f"一共找到 {file_cnt} 个 kfb 格式的文件")
        self.progressBar.setMaximum(file_cnt)

        dst_root_path = os.path.join(root_path, "svs")  # 转换后的svs文件根目录
        if not os.path.exists(dst_root_path):
            os.makedirs(dst_root_path)

        level = 9
        exe_path = os.path.join(BASE_DIR, "kfbio/x86/KFbioConverter.exe")  # 转换程序路径
        if not os.path.exists(exe_path):
            raise FileNotFoundError("找不到转换程序")

        ok_cnt = 0
        for kfb_file in files:
            print("-" * 42)
            print(f"正在转换第 {ok_cnt+1} 个文件, 一共有 {file_cnt} 个文件")
            svs_dest_path = kfb_file.replace(root_path, f"{root_path}/svs")
            svs_dest_path = svs_dest_path.replace(".kfb", ".svs")
            command = f'{exe_path} "{kfb_file}" "{svs_dest_path}" {level}'  # 加双引号避免文件路径有空格
            p = subprocess.Popen(command)
            p.wait()
            ok_cnt += 1
            self.progressBar.setValue(ok_cnt)
            self.advanceProgressBar()
            print()

        print("所有文件已经转换成功!!!")

    def advanceProgressBar(self):
        curVal = self.progressBar.value()
        maxVal = self.progressBar.maximum()
        self.progressBar.setValue(curVal + (maxVal - curVal) / 100)

    def createProgressBar(self):
        self.progressBar = QProgressBar()
        self.progressBar.setWindowTitle("处理进度")
        self.progressBar.setValue(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    print("当前程序根路径:", BASE_DIR)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
