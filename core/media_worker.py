import os
from PySide6.QtCore import QObject, Signal, Slot
from core.general_function import GeneralFunction


class VideoWorker(QObject):
    row_loaded = Signal(dict)
    finished = Signal()

    def __init__(self, folder, extensions):
        super().__init__()
        self.folder = folder
        self.extensions = extensions
        self._running = True

    def stop(self):
        self._running = False

    @Slot()
    def run(self):
        if not os.path.exists(self.folder):
            self.finished.emit()
            return

        row = 0
        for filename in sorted(os.listdir(self.folder)):
            if not self._running:
                break

            if not filename.lower().endswith(self.extensions):
                continue

            path = os.path.join(self.folder, filename)

            try:
                size = os.path.getsize(path) / 1024 / 1024
            except Exception:
                size = 0

            video = {
                "row": row,
                "path": path,
                "name": filename,
                "duration": GeneralFunction.get_video_duration(path),
                "size": f"{size:.2f} MB",
                "thumbnail": GeneralFunction.get_video_thumbnail(path)
            }
            self.row_loaded.emit(video)
            row += 1

        self.finished.emit()


class ImageWorker(QObject):
    row_loaded = Signal(dict)
    finished = Signal()

    def __init__(self, folder, extensions):
        super().__init__()
        self.folder = folder
        self.extensions = extensions
        self._running = True

    def stop(self):
        self._running = False

    @Slot()
    def run(self):
        if not os.path.exists(self.folder):
            self.finished.emit()
            return

        row = 0
        for filename in sorted(os.listdir(self.folder)):
            if not self._running:
                break

            if not filename.lower().endswith(self.extensions):
                continue

            path = os.path.join(self.folder, filename)

            try:
                size = os.path.getsize(path) / 1024 / 1024
            except Exception:
                size = 0

            image = {
                "row": row,
                "path": path,
                "name": filename,
                "size": f"{size:.2f} MB",
                "thumbnail": GeneralFunction.get_image_thumbnail(path)
            }
            self.row_loaded.emit(image)
            row += 1

        self.finished.emit()