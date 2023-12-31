from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout


class Tab(QWidget):  # parent tab class
    def __init__(self):
        super().__init__()

        self.scene_layout = QVBoxLayout()
        self.sidebar_layout = QVBoxLayout()
        self.scene_layout.setContentsMargins(5, 5, 5, 5)
        self.sidebar_layout.setContentsMargins(5, 5, 5, 5)
        self.sidebar_layout.setSpacing(30)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(self.scene_layout, 7)
        layout.addLayout(self.sidebar_layout, 3)
        self.setLayout(layout)

    def setup_scale_bar(self):
        pass