from PyQt5.QtWidgets import QToolBox


# 单机模式主要只有左侧的QToolBox，右侧界面由QToolBox的选项负责弹出，仅需在此.py文件中初始化
class SingleMode(QToolBox):

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        """单机加密模式，包含一个QToolBox"""
        pass
