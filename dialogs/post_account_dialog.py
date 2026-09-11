from PySide6.QtWidgets import (
    QCheckBox, QRadioButton, QSpinBox, QDoubleSpinBox,
    QTextEdit, QLineEdit, QLabel, QPlainTextEdit,
    QFileDialog, QDialog, QTableWidgetItem, QHeaderView
)
from PySide6.QtCore import Qt, QTimer, Signal, QThread
import os
from PySide6.QtGui import QPixmap, QImage
from ui.set_post_account_dialog import Ui_Post
from core.media_worker import VideoWorker, ImageWorker


class PostAccountDialog(QDialog):
    data_saved = Signal(dict)

    def __init__(self, parent=None, data_manager=None, general_function=None):
        super().__init__(parent)
        self.data_manager = data_manager
        self.general_function = general_function
        self.ui = Ui_Post()
        self.ui.setupUi(self)

        # 🟢 FIX: Added index 3 for the Story tab state tracking
        self.loaded_tabs = {1: False, 2: False, 3: False}
        
        # Thread management dictionary
        self.media_threads = {}

        self.VIDEO_EXTENSIONS = (".mp4", ".mov", ".avi", ".mkv", ".webm")
        self.IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp", ".webp")
        self.acc_ids = []
        self.new_settings = {}
        self.first_id = None
        self.data = {}

        # ---------------------------------------------------------
        # DEFINING KEYS (Matches your exact UI variable names)
        # ---------------------------------------------------------
        self.REELS_KEYS = [
            "post", "total_posts", "tag", "tag_from", "tag_to", "ai_label_reels", 
            "use_tittle_from_videos", "use_fixed_tittle", "tittle_text", "hastag", 
            "use_fixed_hastag", "use_random_hastag", "post_reels_hastag", 
            "share_to_group", "share_to_group_from", "share_to_group_to", 
            "share_to_group_tittle", "share_to_group_use_by_suggest", "share_to_group_use_by_seleted", 
            "use_fixed_share_group_tittle", "use_random_share_group_tittle", "share_to_group_word", 
            "comments", "comments_use_fixed", "comments_use_random", "comments_text", 
            "check_in", "check_in_word", "videos_reel_path", "videos_reel_post_ready"
        ]
        
        self.VIDEOS_KEYS = [
            "post_video", "total_posts_video", "video_tag", "video_tag_from", "video_tag_to", 
            "ai_label_videos", "video_use_tittle_from_videos", "video_use_fixed_tittle", "video_tittle_text", 
            "hastag_video", "video_use_fixed_hastag", "video_use_random_hastag", "post_videos_hastag",
            "share_to_group_video", "share_to_group_from_video", "share_to_group_to_video", 
            "share_to_group_tittle_videos", "share_to_group_use_by_suggest_video", "share_to_group_use_by_seleted_video", 
            "use_fixed_share_group_tittle_videos", "use_random_share_group_tittle_videos", "share_group_tittle_videos_words", 
            "video_comments", "video_comments_use_fixed", "video_comments_use_random", "video_comments_text", 
            "video_check_in", "video_check_in_word", "videos_tab_videos_path", "videos_post_ready", "use_feeling_video", "feeling_random_video",
            "feeling_happy_video", "feeling_blessed_video", "feeling_loved_video", "feeling_sad_video", "feeling_lovely_video", "feeling_crazy_video",
            "feeling_thankful_video", "feeling_inlove_video", "feeling_excited_video"
        ]
        
        self.IMAGES_KEYS = [
            "post_image", "total_posts_image", "ai_label_image", "tag_image", "tag_from_image", 
            "tag_to_image", "total_per_post_image", "use_tittle_from_image", "use_fixed_tittle_image", 
            "tittle_image_word", "hastag_image", "use_fixed_hastag_image", "use_random_hastag_image", "image_hastag_word",
            "share_to_group_image", "share_to_group_from_image", "share_to_group_to_image", 
            "share_to_group_tittle_image", "share_to_group_use_by_suggest_image", "share_to_group_use_by_seleted_image", 
            "use_fixed_share_group_tittle_image", "use_random_share_group_tittle_image", "share_to_group_word_image", 
            "comments_image", "comments_use_fixed_image", "comments_use_random_image", "comments_image_word", 
            "check_in_image", "check_in_image_word", "image_path", "images_post_ready",
            "use_feeling_image", "feeling_random_image", "classic", "column", "banner", "frame_layout",
            "feeling_happy_image", "feeling_blessed_image", "feeling_loved_image", "feeling_sad_image", "feeling_lovely_image", "feeling_crazy_image",
            "feeling_thankful_image", "feeling_inlove_image", "feeling_excited_image"
        ]
        
        self.STORY_KEYS = ["post_story", "total_post_story", "story_path", "story_already_post"]

        self._setup_connections()
        self._setup_ui_defaults()


    def _setup_connections(self):
        """Maps all button clicks and table interactions using universal helpers."""
        # 1. Group Tables setup (Notice Story is completely excluded)
        group_tables = [
            (self.ui.post_reels_group, self.ui.post_reels_group.horizontalHeader()),
            (self.ui.post_videos_group, self.ui.post_videos_group.horizontalHeader()),
            (self.ui.post_image_group, self.ui.post_image_group.horizontalHeader())
        ]
        for table, header in group_tables:
            header.sectionClicked.connect(lambda idx, t=table: self._toggle_all_groups(t, idx))
            table.cellClicked.connect(lambda r, c, t=table: self._on_group_table_clicked(t, r, c))

        # 2. Media Buttons setup
        media_buttons = [
            # Reels Tab
            (self.ui.browse_video_reel_path, self.ui.refresh_video_reel_path, self.ui.open_location_videos_reel,
             self.ui.videos_reel_path, self.ui.videos_reel_post_ready, self.ui.video_reel_table, "video", "reels"),
            # Videos Tab
            (self.ui.browse_video_path, self.ui.refresh_video_path, self.ui.open_location_videos,
             self.ui.videos_tab_videos_path, self.ui.videos_post_ready, self.ui.video_table, "video", "videos"),
            # Images Tab
            (self.ui.browse_image_path, self.ui.refresh_image_path, self.ui.open_location_image,
             self.ui.image_path, self.ui.images_post_ready, self.ui.images_table, "image", "images"),
            # Story Tab (Using "story" type to trigger mixed media)
            (self.ui.browse_story_path, self.ui.refresh_story_path, self.ui.open_location_story,
             self.ui.story_path, self.ui.story_post_ready, self.ui.story_table, "story", "storys")
        ]
        
        for browse, refresh, open_loc, path_ui, ready_ui, table_ui, media_type, thread_id in media_buttons:
            browse.clicked.connect(lambda checked=False, p=path_ui, r=ready_ui, t=table_ui, m=media_type, tid=thread_id: self._browse_media(p, r, t, m, tid))
            refresh.clicked.connect(lambda checked=False, p=path_ui, r=ready_ui, t=table_ui, m=media_type, tid=thread_id: self._refresh_media(p, r, t, m, tid))
            open_loc.clicked.connect(lambda checked=False, p=path_ui: self.general_function.go_to_location(p.text()))

        # Tab changing
        self.ui.tabWidget.currentChanged.connect(self.handle_tab_change)

    def _setup_ui_defaults(self):
        """Sets default sizes for UI tables."""
        # 🟢 FIX: Added self.ui.story_table to media tables
        for table in [self.ui.video_reel_table, self.ui.video_table, self.ui.images_table, self.ui.story_table]:
            table.setColumnWidth(0, 0)
            table.setColumnWidth(2, 200)
            table.verticalHeader().setDefaultSectionSize(70)

        for group_table in [self.ui.post_reels_group, self.ui.post_videos_group, self.ui.post_image_group]:
            group_table.verticalHeader().setDefaultSectionSize(40)


    # =====================================================================
    # SMART DATA BINDING (Read/Write JSON automatically)
    # =====================================================================
    def _get_widget_value(self, widget):
        if isinstance(widget, (QCheckBox, QRadioButton)): return widget.isChecked()
        if isinstance(widget, (QSpinBox, QDoubleSpinBox)): return widget.value()
        if isinstance(widget, (QTextEdit, QPlainTextEdit)): return widget.toPlainText()
        if isinstance(widget, (QLineEdit, QLabel)): return widget.text()
        return None

    def _set_widget_value(self, widget, value):
        if isinstance(widget, (QCheckBox, QRadioButton)):
            widget.setChecked(bool(value))
        elif isinstance(widget, (QSpinBox, QDoubleSpinBox)):
            widget.setValue(int(value) if value else 0)
        elif isinstance(widget, (QTextEdit, QPlainTextEdit)):
            widget.blockSignals(True)
            widget.setPlainText(str(value) if value else "")
            widget.blockSignals(False)
        elif isinstance(widget, (QLineEdit, QLabel)):
            widget.setText(str(value) if value else "")

    def _extract_section_data(self, key_list):
        data = {}
        for key in key_list:
            widget = getattr(self.ui, key, None)
            if widget:
                data[key] = self._get_widget_value(widget)
        return data

    def _inject_section_data(self, key_list, saved_data):
        for key in key_list:
            widget = getattr(self.ui, key, None)
            if widget:
                self._set_widget_value(widget, saved_data.get(key))


    # =====================================================================
    # MAIN DATA FLOW
    # =====================================================================
    def selected_ids(self, acc_ids):
        self.acc_ids = acc_ids
        QTimer.singleShot(0, self.load_data_to_ui)

    def load_data_to_ui(self):
        if not self.acc_ids: return
        
        self.first_id = self.acc_ids[0]
        self.data = self.data_manager.get_post_setting_by_id(self.first_id) or {}

        # 1. Inject settings for all tabs (This is fast, keep it here)
        self._inject_section_data(self.REELS_KEYS, self.data.get("post_reels", {}))
        self._inject_section_data(self.VIDEOS_KEYS, self.data.get("post_videos", {}))
        self._inject_section_data(self.IMAGES_KEYS, self.data.get("post_images", {}))
        self._inject_section_data(self.STORY_KEYS, self.data.get("post_storys", {}))

        # 2. Load ONLY the active tab
        current_index = self.ui.tabWidget.currentIndex()
        self._load_tab_data(current_index)

    def _load_tab_data(self, index):
        """Loads data/media only for the specified tab index."""
        if self.loaded_tabs.get(index, False):
            return

        if index == 0:  # Reels
            self._load_groups_to_table(self.ui.post_reels_group, self.data.get("post_reels", {}).get("groups_to_post", []))
            folder = self.data.get("post_reels", {}).get("videos_reel_path", "")
            if folder and os.path.exists(folder):
                self._refresh_media(self.ui.videos_reel_path, self.ui.videos_reel_post_ready, self.ui.video_reel_table, "video", "reels")

        elif index == 1:  # Videos
            videos_data = self.data.get("post_videos", {})
            self._load_groups_to_table(self.ui.post_videos_group, videos_data.get("groups_to_post_videos", []))
            folder = videos_data.get("videos_tab_videos_path", "")
            if folder and os.path.exists(folder):
                self._refresh_media(self.ui.videos_tab_videos_path, self.ui.videos_post_ready, self.ui.video_table, "video", "videos")

        elif index == 2:  # Images
            images_data = self.data.get("post_images", {})
            self._load_groups_to_table(self.ui.post_image_group, images_data.get("groups_to_post_image", []))
            folder = images_data.get("image_path", "")
            if folder and os.path.exists(folder):
                self._refresh_media(self.ui.image_path, self.ui.images_post_ready, self.ui.images_table, "image", "images")

        elif index == 3:  # Storys
            storys_data = self.data.get("post_storys", {})
            folder = storys_data.get("story_path", "")
            if folder and os.path.exists(folder):
                # 🟢 FIX: Call standard refresh without group logic
                self._refresh_media(self.ui.story_path, self.ui.story_post_ready, self.ui.story_table, "story", "storys")
        
        self.loaded_tabs[index] = True

    def update_data(self):
        self.new_settings = {
            "post_reels": self._extract_section_data(self.REELS_KEYS),
            "post_videos": self._extract_section_data(self.VIDEOS_KEYS),
            "post_images": self._extract_section_data(self.IMAGES_KEYS),
            "post_storys": self._extract_section_data(self.STORY_KEYS),
        }
        
        # Inject custom array data (Selected Groups) - Story is excluded from this!
        self.new_settings["post_reels"]["groups_to_post"] = self._get_selected_groups(self.ui.post_reels_group)
        self.new_settings["post_videos"]["groups_to_post_videos"] = self._get_selected_groups(self.ui.post_videos_group)
        self.new_settings["post_images"]["groups_to_post_image"] = self._get_selected_groups(self.ui.post_image_group)


    # =====================================================================
    # TAB HANDLING
    # =====================================================================
    def handle_tab_change(self, index):
        self._load_tab_data(index)


    # =====================================================================
    # UNIVERSAL GROUP TABLE HELPERS
    # =====================================================================
    def _load_groups_to_table(self, table_widget, saved_groups):
        table_widget.setUpdatesEnabled(False)
        table_widget.setSortingEnabled(False)
        table_widget.setColumnWidth(0, 10)

        all_groups = self.data_manager._load_json("groups", {})
        account_groups = all_groups.get(str(self.first_id), [])

        table_widget.setRowCount(0)
        for row, group_name in enumerate(account_groups):
            table_widget.insertRow(row)

            # Checkbox
            item_check = QTableWidgetItem()
            item_check.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            item_check.setCheckState(Qt.Checked if group_name in saved_groups else Qt.Unchecked)
            table_widget.setItem(row, 0, item_check)

            # Name
            name_item = QTableWidgetItem(group_name)
            name_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable) 
            table_widget.setItem(row, 1, name_item)

        table_widget.setUpdatesEnabled(True)
        table_widget.setSortingEnabled(True)

    def _on_group_table_clicked(self, table_widget, row, column):
        if column == 1:
            item = table_widget.item(row, 0)
            if item:
                new_state = Qt.Unchecked if item.checkState() == Qt.Checked else Qt.Checked
                item.setCheckState(new_state)

    def _toggle_all_groups(self, table_widget, logicalIndex):
        if logicalIndex == 0:
            header = table_widget.horizontalHeaderItem(0)
            new_state = Qt.Checked if header.checkState() == Qt.Unchecked else Qt.Unchecked
            header.setCheckState(new_state)
            
            for row in range(table_widget.rowCount()):
                item = table_widget.item(row, 0)
                if item: item.setCheckState(new_state)

    def _get_selected_groups(self, table_widget):
        selected = []
        for row in range(table_widget.rowCount()):
            item = table_widget.item(row, 0)
            if item and item.checkState() == Qt.Checked:
                name_item = table_widget.item(row, 1)
                if name_item: selected.append(name_item.text())
        return selected


    # =====================================================================
    # UNIVERSAL MEDIA HANDLING
    # =====================================================================
    def _browse_media(self, path_ui, ready_ui, table_ui, media_type, thread_id):
        folder_path = QFileDialog.getExistingDirectory(self, f"Select Folder")
        if folder_path and os.path.exists(folder_path):
            path_ui.setText(folder_path)
            self._refresh_media(path_ui, ready_ui, table_ui, media_type, thread_id)

    def _refresh_media(self, path_ui, ready_ui, table_ui, media_type, thread_id):
        folder_path = path_ui.text()
        if folder_path and os.path.exists(folder_path):
            
            # 🟢 FIX: Do NOT use '+=', it mutates the global tuple!
            if media_type == "video":
                exts = self.VIDEO_EXTENSIONS    
            elif media_type == 'image':
                exts = self.IMAGE_EXTENSIONS
            else: # Used for "story" which supports both!
                exts = self.IMAGE_EXTENSIONS + self.VIDEO_EXTENSIONS

            info = self.general_function.get_media_folder_info(folder_path, exts)
            ready_ui.setText(f"{info['post_already_count']}/{info['total']}")
            self._start_media_thread(thread_id, folder_path, media_type, table_ui)

    def _start_media_thread(self, thread_id, folder, media_type, table_ui):
        table_ui.setSortingEnabled(False)
        table_ui.setRowCount(0)

        if thread_id in self.media_threads:
            old_thread, old_worker = self.media_threads[thread_id]
            try:
                if old_thread and old_thread.isRunning():
                    old_worker.stop()
                    old_thread.quit()
                    old_thread.wait()
            except RuntimeError:
                pass 

        thread = QThread()
        
        # 🟢 FIX: Select the right worker based on combined extensions
        if media_type == "image":
            exts = self.IMAGE_EXTENSIONS
            worker = ImageWorker(folder, exts)
        else:
            # VideoWorker generally supports both image and video thumbnail extraction
            exts = self.VIDEO_EXTENSIONS if media_type == "video" else self.IMAGE_EXTENSIONS + self.VIDEO_EXTENSIONS
            worker = VideoWorker(folder, exts)

        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        
        # 🟢 FIX: Added safe row connection for Story
        if thread_id == "reels":
            worker.row_loaded.connect(self._add_video_reel_row_safe)
        elif thread_id == "videos":
            worker.row_loaded.connect(self._add_video_row_safe)
        elif thread_id == "images":
            worker.row_loaded.connect(self._add_image_row_safe)
        elif thread_id == "storys":
            worker.row_loaded.connect(self._add_story_row_safe)
        
        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(lambda: table_ui.setSortingEnabled(True))
        thread.finished.connect(thread.deleteLater)

        self.media_threads[thread_id] = (thread, worker)
        thread.start()

    def _add_media_table_row(self, table_ui, media_data, is_video):
        row = table_ui.rowCount()
        table_ui.insertRow(row)

        id_item = QTableWidgetItem(str(row + 1))
        id_item.setData(Qt.UserRole, media_data["path"])
        table_ui.setItem(row, 0, id_item)

        label = QLabel()
        label.setAlignment(Qt.AlignCenter)
        
        if media_data.get("thumbnail"): 
            thumb_data = media_data["thumbnail"]
            if isinstance(thumb_data, QImage):
                label.setPixmap(QPixmap.fromImage(thumb_data))
            else:
                label.setPixmap(thumb_data) 
                
        table_ui.setCellWidget(row, 1, label)
        table_ui.setItem(row, 2, QTableWidgetItem(media_data["name"]))
        
        # 🟢 FIX: Smart column logic! 
        # Prevents UI misalignment if a table supports 6 columns (mixed media) 
        # but the current file is an image with no "duration".
        if table_ui.columnCount() == 6:
            if is_video:
                table_ui.setItem(row, 3, QTableWidgetItem(media_data.get("duration", "")))
            else:
                table_ui.setItem(row, 3, QTableWidgetItem("N/A")) # Fill duration slot cleanly
            
            table_ui.setItem(row, 4, QTableWidgetItem(media_data.get("size", "")))
            table_ui.setItem(row, 5, QTableWidgetItem("Ready"))
        else:
            # Standard 5-column Image-only table
            table_ui.setItem(row, 3, QTableWidgetItem(media_data.get("size", "")))
            table_ui.setItem(row, 4, QTableWidgetItem("Ready"))


    # =====================================================================
    # THREAD-SAFE UI WRAPPERS
    # =====================================================================
    def _add_video_reel_row_safe(self, media_data):
        self._add_media_table_row(self.ui.video_reel_table, media_data, is_video=True)
        
    def _add_video_row_safe(self, media_data):
        self._add_media_table_row(self.ui.video_table, media_data, is_video=True)
        
    def _add_image_row_safe(self, media_data):
        self._add_media_table_row(self.ui.images_table, media_data, is_video=False)
        
    # 🟢 FIX: Added safe row handler for mixed Story media
    def _add_story_row_safe(self, media_data):
        ext = os.path.splitext(media_data["path"])[1].lower()
        is_video = ext in self.VIDEO_EXTENSIONS
        self._add_media_table_row(self.ui.story_table, media_data, is_video=is_video)


    # =====================================================================
    # CLEANUP & CLOSE
    # =====================================================================
    def closeEvent(self, event):
        self.update_data()
        self.data_manager.update_post_settings(self.acc_ids, self.new_settings)
        self.acc_ids = []

        # Safe Thread Cleanup
        for thread_id, (thread, worker) in self.media_threads.items():
            try:
                if thread and thread.isRunning():
                    worker.stop()
                    thread.quit()
                    thread.wait()
            except RuntimeError:
                pass
        self.media_threads.clear()

        # UI Cleanup
        self.loaded_tabs = {1: False, 2: False, 3: False}
        for path_ui in [self.ui.videos_reel_path, self.ui.videos_tab_videos_path, self.ui.image_path, self.ui.story_path]:
            path_ui.clear()
            
        for table in [self.ui.video_reel_table, self.ui.video_table, self.ui.images_table, self.ui.story_table,
                      self.ui.post_reels_group, self.ui.post_videos_group, self.ui.post_image_group]:
            table.setRowCount(0)

        self.data_saved.emit(self.new_settings)
        super().closeEvent(event)




from PySide6.QtWidgets import QDialog, QVBoxLayout, QComboBox, QPushButton, QLabel, QHBoxLayout



class SelectAccountDialog(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWindowTitle("Select Reference Account")

        self.selected_id = None

       

        self.layout = QVBoxLayout()

        self.layout.addWidget(QLabel("Multiple accounts selected.\nSelect one to load settings FROM:"))

       

        self.combo = QComboBox()

        self.layout.addWidget(self.combo)

       

        btn_layout = QHBoxLayout()

        ok_btn = QPushButton("OK")

        ok_btn.clicked.connect(self.accept_selection)

        btn_layout.addWidget(ok_btn)

       

        self.layout.addLayout(btn_layout)

        self.setLayout(self.layout)



    # 🟢 This method is automatically called by your show_custom_dialog helper

    def set_data(self, acc_ids):

        self.combo.addItems(acc_ids)



    def accept_selection(self):

        self.selected_id = self.combo.currentText()

        self.accept()











