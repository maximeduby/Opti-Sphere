from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QDoubleSpinBox, \
    QCheckBox

from core.threads.ScanningThread import ScanningThread
from ui.tabs.ScanTab import ScanTab
from ui.widgets.ProgressWidget import ProgressWidget


class ScanningTab(QWidget):
    def __init__(self, wnd):
        super().__init__()
        self.wnd = wnd
        self.scan_th = None
        self.scan_counter = 1

        layout = QVBoxLayout()

        method_layout = QHBoxLayout()
        method_legend = QLabel(text='Method', objectName='legend')
        method_legend.setFixedWidth(60)
        self.method = QComboBox()
        self.method.view().parentWidget().setStyleSheet('background-color: #151415; border-radius: 5px; padding: 1px;')
        self.method.addItems(["Frame by Frame"])
        self.method.activated.connect(self.change_method)
        method_layout.addWidget(method_legend)
        method_layout.addWidget(self.method)

        self.frame_method = QWidget(objectName="sub-widget-container")
        frame_method_layout = QHBoxLayout()
        frame_method_layout.setContentsMargins(0, 10, 0, 10)
        angle_legend = QLabel(text="Angle", objectName="legend")
        angle_legend.setFixedWidth(60)
        self.angle = QDoubleSpinBox()
        self.angle.setDecimals(1)
        self.angle.setRange(0.0, 90.0)
        self.angle.setValue(5.0)
        self.angle.setSuffix("°")
        auto_legend = QLabel(text="Auto Mode", objectName="legend")
        auto_legend.setFixedWidth(80)
        self.is_auto = QCheckBox(objectName="switch")
        self.is_auto.setChecked(True)
        frame_method_layout.addWidget(angle_legend)
        frame_method_layout.addWidget(self.angle)
        frame_method_layout.addStretch()
        frame_method_layout.addWidget(auto_legend)
        frame_method_layout.addWidget(self.is_auto)
        self.frame_method.setLayout(frame_method_layout)

        axis_layout = QHBoxLayout()
        axis_legend = QLabel(text='Axis', objectName='legend')
        axis_legend.setFixedWidth(60)
        self.axis = QComboBox()
        self.axis.view().parentWidget().setStyleSheet(
            'background-color: #151415; border-radius: 5px; padding: 1px 0px;')
        self.axis.update()

        self.axis.addItems(["Roll", "Pitch"])
        axis_layout.addWidget(axis_legend)
        axis_layout.addWidget(self.axis)

        self.scan_btn = QPushButton("Start Scanning", objectName="action-btn")
        self.scan_btn.clicked.connect(self.scan)

        self.scan_progress = ProgressWidget()
        self.scan_progress.setHidden(True)

        self.scan_widget = QWidget()
        scan_layout = QHBoxLayout()
        scan_layout.setContentsMargins(0, 10, 0, 10)
        self.capture_btn = QPushButton(text="Capture Frame", objectName="action-btn")
        self.capture_btn.clicked.connect(self.set_ready_for_frame)
        self.switch_auto_btn = QPushButton(text="Auto Mode", objectName="action-btn")
        self.switch_auto_btn.clicked.connect(self.switch_auto_mode)
        cancel_btn = QPushButton(text="Cancel", objectName="action-btn")
        cancel_btn.clicked.connect(self.cancel_scan)
        scan_layout.addWidget(self.capture_btn)
        scan_layout.addWidget(self.switch_auto_btn)
        scan_layout.addWidget(cancel_btn)
        self.scan_widget.setLayout(scan_layout)
        self.scan_widget.setHidden(True)

        layout.addLayout(method_layout)
        layout.addWidget(self.frame_method)
        layout.addLayout(axis_layout)
        layout.addWidget(self.scan_btn)
        layout.addWidget(self.scan_progress)
        layout.addWidget(self.scan_widget)
        layout.addStretch()
        self.setLayout(layout)

    @Slot()
    def scan(self):  # start new scan
        self.wnd.main_tab.set_action("scanning")
        self.scan_btn.setEnabled(False)
        self.scan_progress.setHidden(False)
        self.scan_widget.setHidden(False)
        self.capture_btn.setHidden(self.is_auto.isChecked())
        self.switch_auto_btn.setHidden(self.is_auto.isChecked())
        self.scan_th = ScanningThread(self.wnd,
                                      self.scan_progress,
                                      self.method.currentText(),
                                      self.axis.currentText(),
                                      self.angle.value(),
                                      self.is_auto.isChecked())
        self.scan_th.scan_signal.connect(self.add_scan_tab)
        self.scan_th.progress_signal.connect(self.scan_progress.update_progress)
        self.scan_th.start()
        self.scan_th.moveToThread(self.thread())
        self.scan_th.finished.connect(lambda: self.scan_btn.setEnabled(True))

    @Slot()
    def change_method(self):  # show/hide additional parameters according to current method
        self.frame_method.setHidden(self.method.currentIndex() != 0)

    @Slot()
    def add_scan_tab(self, frames, info):  # create new ScanTab to show result of scan
        self.wnd.main_tab.set_action("none")
        self.scan_progress.setHidden(True)
        self.scan_widget.setHidden(True)
        self.scan_progress.reset()
        title = f"scan{self.scan_counter}"
        scan_tab = ScanTab(frames, title, info)
        scan_tab.scan_widget.update_signal.connect(self.wnd.update_name)
        self.wnd.tabs.addTab(scan_tab, title)
        self.wnd.tabs.setCurrentWidget(scan_tab)
        self.scan_counter += 1

    @Slot()
    def set_ready_for_frame(self):  # frame ready to be captured [manual mode only]
        self.scan_th.ready_for_frame = True

    @Slot()
    def switch_auto_mode(self):  # finish current manual scan in automatic
        self.scan_th.is_auto = True
        self.capture_btn.setHidden(True)
        self.switch_auto_btn.setHidden(True)

    @Slot()
    def cancel_scan(self):  # cancel scan properly
        self.scan_th.is_canceled = True
        self.scan_th.running = False
        self.scan_progress.setHidden(True)
        self.scan_progress.reset()
        self.scan_widget.setHidden(True)
        self.wnd.main_tab.set_action("none")

