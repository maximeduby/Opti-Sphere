import cv2
from PySide6.QtWidgets import QFileDialog

from ui.dialogs.SetupScaleDialog import SetupScaleDialog
from ui.tabs.Tab import Tab
from ui.widgets.ImageViewer import ImageViewer
from ui.widgets.SnapshotWidget import SnapshotWidget


class SnapshotTab(Tab):
    def __init__(self, frame, title):
        super().__init__()
        self.frame = frame
        self.title = title

        self.snapshot = ImageViewer()
        self.snapshot.gv.set_image(self.frame)

        self.ss_widget = SnapshotWidget(self)

        self.scene_layout.addWidget(self.snapshot)
        self.sidebar_layout.addWidget(self.ss_widget)

    def export(self):  # export snapshot to chosen location
        filename = QFileDialog.getSaveFileName(None, "Export Image", self.title, "Image (*.tiff *.jpg *.png)")
        if filename[0] == '':
            return
        cv2.imwrite(filename[0], self.frame)

    def get_dimensions(self):  # return snapshot's dimensions
        w = self.frame.shape[1]
        h = self.frame.shape[0]
        return f"{w} × {h}"

    def resizeEvent(self, event):  # update image size according to window size
        self.snapshot.gv.set_image(self.frame)

    def setup_scale_bar(self):  # set up the scale from the snapshot
        dlg = SetupScaleDialog(self.frame)
        if dlg.exec():
            self.snapshot.pix2mm = dlg.get_ratio()
            ImageViewer.is_scale_bar_visible = True
