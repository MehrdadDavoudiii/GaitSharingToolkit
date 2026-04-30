
from __future__ import annotations

import os
import platform
import sys
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QStackedWidget, QFrame, QMessageBox,
    QMenuBar, QMenu, QSizePolicy, QSpacerItem,
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QIcon, QPixmap, QPainter, QColor, QAction

from GaitSharing_config import (
    DB_PATH, DATA_DIR, PALETTE, USER_INFO, APP_DIR, USER_PHOTO_PATH,
)
from GaitSharing_database import Database
from GaitSharing_ui import (
    PatientsTab, ImportTab, SearchTab, ExportTab,
    AnonymizerTab, AIInterpreterTab, AboutWindow,
)
from GaitSharing_c3d import C3DExtractorTab
from GaitSharing_strides import StrideAnalysisTab
from GaitSharing_features import FeatureExtractorTab

#  GLOBAL QSS STYLESHEET

GLOBAL_QSS = f"""
/* ── Base ─────────────────────────────────────── */
QWidget {{
    font-family: "Segoe UI", "Inter", "SF Pro Display", "Helvetica Neue", Arial, sans-serif;
    font-size: 13px;
    color: {PALETTE['text']};
}}

QMainWindow {{
    background-color: {PALETTE['bg']};
}}

/* ── Buttons ──────────────────────────────────── */
QPushButton {{
    background-color: {PALETTE['surface']};
    border: 1px solid {PALETTE['border']};
    border-radius: 6px;
    padding: 7px 16px;
    font-weight: 600;
    color: {PALETTE['text']};
    min-height: 20px;
}}
QPushButton:hover {{
    background-color: #E8E8E8;
    border-color: #C0C0C0;
}}
QPushButton:pressed {{
    background-color: #D5D5D5;
}}
QPushButton:disabled {{
    background-color: #F0F0F0;
    color: #AAAAAA;
    border-color: #E0E0E0;
}}

QPushButton[cssClass="accent"] {{
    background-color: {PALETTE['accent']};
    color: white;
    border: none;
    font-weight: 700;
}}
QPushButton[cssClass="accent"]:hover {{
    background-color: {PALETTE['accent_dk']};
}}
QPushButton[cssClass="accent"]:pressed {{
    background-color: #6B8A08;
}}

QPushButton[cssClass="danger"] {{
    background-color: {PALETTE['warning']};
    color: white;
    border: none;
}}
QPushButton[cssClass="danger"]:hover {{
    background-color: #B71C1C;
}}

/* ── Inputs ───────────────────────────────────── */
QLineEdit, QSpinBox, QDoubleSpinBox {{
    background-color: {PALETTE['surface']};
    border: 1px solid {PALETTE['border']};
    border-radius: 6px;
    padding: 6px 10px;
    selection-background-color: {PALETTE['accent']};
    selection-color: white;
}}
QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {{
    border: 2px solid {PALETTE['accent']};
    padding: 5px 9px;
}}
QLineEdit:disabled {{
    background-color: #F5F5F5;
    color: #999999;
}}

QTextEdit, QPlainTextEdit {{
    background-color: {PALETTE['surface']};
    border: 1px solid {PALETTE['border']};
    border-radius: 6px;
    padding: 6px;
    selection-background-color: {PALETTE['accent']};
}}
QTextEdit:focus, QPlainTextEdit:focus {{
    border: 2px solid {PALETTE['accent']};
}}

/* ── ComboBox ─────────────────────────────────── */
QComboBox {{
    background-color: {PALETTE['surface']};
    border: 1px solid {PALETTE['border']};
    border-radius: 6px;
    padding: 6px 10px;
    min-width: 60px;
}}
QComboBox:hover {{
    border-color: #B0B0B0;
}}
QComboBox::drop-down {{
    border: none;
    width: 24px;
}}

/* ── GroupBox ──────────────────────────────────── */
QGroupBox {{
    background-color: {PALETTE['surface']};
    border: 1px solid {PALETTE['border']};
    border-radius: 10px;
    margin-top: 14px;
    padding: 16px 12px 12px 12px;
    font-weight: 600;
    font-size: 12px;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 14px;
    top: 2px;
    padding: 0 6px;
    background-color: {PALETTE['surface']};
    color: {PALETTE['primary']};
    font-weight: 700;
}}

/* ── Tables ───────────────────────────────────── */
QTableWidget, QTableView, QTreeWidget, QTreeView {{
    background-color: {PALETTE['surface']};
    alternate-background-color: {PALETTE['alt_row']};
    border: 1px solid {PALETTE['border']};
    border-radius: 8px;
    gridline-color: #EEF0F2;
    selection-background-color: {PALETTE['accent']};
    selection-color: white;
    font-size: 12px;
}}
QHeaderView::section {{
    background-color: {PALETTE['primary']};
    color: white;
    font-weight: 700;
    font-size: 11px;
    padding: 6px 8px;
    border: none;
    border-right: 1px solid rgba(255,255,255,0.15);
    border-bottom: 2px solid {PALETTE['accent']};
}}
QHeaderView::section:hover {{
    background-color: {PALETTE['primary_lt']};
}}

/* ── ScrollBars ───────────────────────────────── */
QScrollBar:vertical {{
    width: 8px;
    background: transparent;
    margin: 0;
}}
QScrollBar::handle:vertical {{
    background: #C0C0C0;
    border-radius: 4px;
    min-height: 30px;
}}
QScrollBar::handle:vertical:hover {{
    background: #A0A0A0;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}
QScrollBar:horizontal {{
    height: 8px;
    background: transparent;
}}
QScrollBar::handle:horizontal {{
    background: #C0C0C0;
    border-radius: 4px;
    min-height: 30px;
}}

/* ── ProgressBar ──────────────────────────────── */
QProgressBar {{
    border: none;
    border-radius: 4px;
    background-color: #E8ECF0;
    height: 8px;
    text-align: center;
    font-size: 0;
}}
QProgressBar::chunk {{
    background-color: {PALETTE['accent']};
    border-radius: 4px;
}}

/* ── CheckBox & RadioButton ───────────────────── */
QCheckBox, QRadioButton {{
    spacing: 8px;
    font-size: 13px;
}}
QCheckBox::indicator, QRadioButton::indicator {{
    width: 18px;
    height: 18px;
}}

/* ── Labels ───────────────────────────────────── */
QLabel[cssClass="muted"] {{
    color: {PALETTE['text_muted']};
    font-size: 12px;
}}
QLabel[cssClass="header"] {{
    font-size: 17px;
    font-weight: 700;
    color: {PALETTE['primary']};
}}
QLabel[cssClass="subheader"] {{
    font-size: 12px;
    color: {PALETTE['text_muted']};
}}
QLabel[cssClass="section"] {{
    font-size: 14px;
    font-weight: 700;
    color: {PALETTE['primary']};
}}

/* ── Log Console ──────────────────────────────── */
QTextEdit[cssClass="console"] {{
    background-color: {PALETTE['log_bg']};
    color: {PALETTE['log_fg']};
    border-radius: 8px;
    font-family: "Cascadia Code", "Fira Code", "Consolas", monospace;
    font-size: 12px;
    padding: 8px;
}}

/* ── Tab Widget (fallback for dialogs) ────────── */
QTabWidget::pane {{
    border: 1px solid {PALETTE['border']};
    border-radius: 8px;
    background: {PALETTE['surface']};
}}
QTabBar::tab {{
    padding: 8px 18px;
    font-weight: 600;
    border: none;
    background: transparent;
    color: {PALETTE['text_muted']};
}}
QTabBar::tab:selected {{
    color: {PALETTE['accent']};
    border-bottom: 3px solid {PALETTE['accent']};
}}
QTabBar::tab:hover {{
    color: {PALETTE['text']};
    background: rgba(0,0,0,0.03);
}}

/* ── Separator ────────────────────────────────── */
QFrame[cssClass="separator"] {{
    background-color: {PALETTE['border']};
    max-height: 1px;
}}

/* ── Tooltip ──────────────────────────────────── */
QToolTip {{
    background-color: {PALETTE['primary']};
    color: white;
    border: none;
    border-radius: 4px;
    padding: 6px 10px;
    font-size: 12px;
}}
"""

#  SIDEBAR NAVIGATION

NAV_ITEMS = [
    ("Patients",          "👥"),
    ("Import",            "📥"),
    ("Search",            "🔍"),
    ("Export",            "📤"),
    ("Anonymizer",        "🔒"),
    ("C3D Extractor",     "📊"),
    ("Stride Analysis",   "🦶"),
    ("Feature Extractor", "🧬"),
    ("AI Interpreter",    "🤖"),
]

class SidebarButton(QPushButton):

    def __init__(self, text: str, icon_text: str, parent=None):
        super().__init__(parent)
        self.setText(f"  {icon_text}   {text}")
        self.setCheckable(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(44)
        self.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: rgba(255,255,255,0.65);
                border: none;
                border-radius: 8px;
                text-align: left;
                padding: 0 14px;
                font-size: 13px;
                font-weight: 500;
                margin: 1px 8px;
            }}
            QPushButton:hover {{
                background-color: {PALETTE['sidebar_hover']};
                color: white;
            }}
            QPushButton:checked {{
                background-color: rgba(156, 190, 32, 0.18);
                color: {PALETTE['accent']};
                font-weight: 700;
                border-left: 3px solid {PALETTE['accent']};
                border-radius: 0 8px 8px 0;
                margin-left: 0;
                padding-left: 19px;
            }}
        """)

class Sidebar(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(210)
        self.setStyleSheet(f"""
            Sidebar {{
                background-color: {PALETTE['sidebar']};
                border-right: 1px solid rgba(255,255,255,0.08);
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 12)
        layout.setSpacing(0)

        # App Header
        header = QWidget()
        header.setFixedHeight(72)
        header.setStyleSheet(f"background-color: {PALETTE['sidebar']};")
        hlay = QVBoxLayout(header)
        hlay.setContentsMargins(18, 14, 14, 6)

        title = QLabel("Gait Sharing")
        title.setStyleSheet("color: white; font-size: 16px; font-weight: 800; letter-spacing: 0.5px;")
        hlay.addWidget(title)

        subtitle = QLabel("Clinical Gait Dataset Manager")
        subtitle.setStyleSheet(f"color: {PALETTE['accent']}; font-size: 10px; font-weight: 500;")
        hlay.addWidget(subtitle)

        layout.addWidget(header)

        # Separator
        sep = QFrame()
        sep.setFixedHeight(1)
        sep.setStyleSheet("background-color: rgba(255,255,255,0.1);")
        layout.addWidget(sep)
        layout.addSpacing(8)

        # Nav Section Label
        nav_label = QLabel("  NAVIGATION")
        nav_label.setStyleSheet(
            "color: rgba(255,255,255,0.35); font-size: 10px; "
            "font-weight: 700; letter-spacing: 1.5px; padding: 4px 14px;"
        )
        layout.addWidget(nav_label)
        layout.addSpacing(4)

        # Nav Buttons
        self.buttons: list[SidebarButton] = []
        for text, icon in NAV_ITEMS:
            btn = SidebarButton(text, icon)
            btn.clicked.connect(lambda checked, b=btn: self._on_click(b))
            self.buttons.append(btn)
            layout.addWidget(btn)

        layout.addStretch()

        # User Card
        sep2 = QFrame()
        sep2.setFixedHeight(1)
        sep2.setStyleSheet("background-color: rgba(255,255,255,0.1);")
        layout.addWidget(sep2)

        user_card = QWidget()
        user_card.setStyleSheet(f"background-color: {PALETTE['sidebar']};")
        uclay = QVBoxLayout(user_card)
        uclay.setContentsMargins(14, 10, 14, 4)
        uclay.setSpacing(1)

        name_lbl = QLabel(USER_INFO["name"])
        name_lbl.setStyleSheet("color: white; font-size: 12px; font-weight: 600;")
        uclay.addWidget(name_lbl)

        role_lbl = QLabel(f"{USER_INFO['title']}")
        role_lbl.setStyleSheet("color: rgba(255,255,255,0.5); font-size: 10px;")
        uclay.addWidget(role_lbl)

        inst_lbl = QLabel(USER_INFO["institution"])
        inst_lbl.setStyleSheet(f"color: {PALETTE['accent']}; font-size: 10px;")
        inst_lbl.setWordWrap(True)
        uclay.addWidget(inst_lbl)

        layout.addWidget(user_card)

    def _on_click(self, clicked_btn: SidebarButton):
        for btn in self.buttons:
            btn.setChecked(btn is clicked_btn)

    def select(self, index: int):
        if 0 <= index < len(self.buttons):
            self.buttons[index].setChecked(True)
            for i, btn in enumerate(self.buttons):
                if i != index:
                    btn.setChecked(False)

#  BACKUP HELPERS

def _trigger_backup(db):
    backup_dir = APP_DIR / "backups"
    try:
        path = db.create_backup(backup_dir)
        QMessageBox.information(None, "Backup Successful",
                                f"Database backed up to:\n{path}")
    except Exception as e:
        QMessageBox.critical(None, "Backup Failed", str(e))

def _open_backups_folder():
    backup_dir = APP_DIR / "backups"
    backup_dir.mkdir(exist_ok=True)
    if platform.system() == "Windows":
        os.startfile(backup_dir)
    elif platform.system() == "Darwin":
        os.system(f'open "{backup_dir}"')
    else:
        os.system(f'xdg-open "{backup_dir}"')

#  MAIN WINDOW

class GaitSharingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database(DB_PATH)

        self.setWindowTitle("Gait Sharing")
        
        # Set the Window Icon in Qt
        ico_path = APP_DIR / "user_photo.ico"
        if ico_path.exists():
            self.setWindowIcon(QIcon(str(ico_path)))
        
        self.setMinimumSize(960, 600)
        self.resize(1200, 820)

        # Menu Bar
        self._build_menu()

        # Central Widget
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        self.sidebar = Sidebar()
        main_layout.addWidget(self.sidebar)

        # Content Stack
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        self.stack = QStackedWidget()
        right_layout.addWidget(self.stack)

        # Status Bar
        self._build_status_bar(right_layout)

        main_layout.addWidget(right_panel)

        # Build Tabs
        self._selected_patient: dict | None = None
        self._build_pages()

        # Wire Sidebar
        for i, btn in enumerate(self.sidebar.buttons):
            btn.clicked.connect(lambda checked, idx=i: self.stack.setCurrentIndex(idx))
        self.sidebar.select(0)

        self.refresh_patients()

    def _build_menu(self):
        menubar = self.menuBar()

        fm = menubar.addMenu("File")
        fm.addAction("Exit", self.close)

        bm = menubar.addMenu("Backup")
        bm.addAction("💾  Create Database Backup",
                      lambda: _trigger_backup(self.db))
        bm.addAction("📂  Open Backups Folder", _open_backups_folder)

        am = menubar.addMenu("About")
        am.addAction("About / Acknowledgments",
                      lambda: AboutWindow(self).exec())

    def _build_pages(self):
        self.patients_tab = PatientsTab(self.db,
                                        on_select_cb=self._on_patient_selected)
        self.stack.addWidget(self.patients_tab)

        self.import_tab = ImportTab(self.db,
                                    refresh_patients_cb=self.refresh_patients)
        self.stack.addWidget(self.import_tab)

        self.search_tab = SearchTab(self.db, self.patients_tab)
        self.stack.addWidget(self.search_tab)

        self.export_tab = ExportTab(self.db)
        self.stack.addWidget(self.export_tab)
        self.search_tab.set_export_tab(self.export_tab)

        self.anon_tab = AnonymizerTab(
            get_selected_cb=lambda: self._selected_patient)
        self.stack.addWidget(self.anon_tab)

        self.c3d_tab = C3DExtractorTab()
        self.stack.addWidget(self.c3d_tab)
        self.stride_tab = StrideAnalysisTab()    
        self.stack.addWidget(self.stride_tab)

        self.feature_tab = FeatureExtractorTab()
        self.stack.addWidget(self.feature_tab)

        self.ai_tab = AIInterpreterTab(
            get_selected_cb=lambda: self._selected_patient)
        self.stack.addWidget(self.ai_tab)

    def _build_status_bar(self, parent_layout):
        bar = QFrame()
        bar.setFixedHeight(28)
        bar.setStyleSheet(f"""
            QFrame {{
                background-color: {PALETTE['surface']};
                border-top: 1px solid {PALETTE['border']};
            }}
            QLabel {{
                font-size: 11px;
                color: {PALETTE['text_muted']};
            }}
        """)
        blay = QHBoxLayout(bar)
        blay.setContentsMargins(12, 0, 12, 0)

        self._status_db_lbl = QLabel()
        blay.addWidget(self._status_db_lbl)
        blay.addStretch()
        self._status_count_lbl = QLabel()
        blay.addWidget(self._status_count_lbl)

        parent_layout.addWidget(bar)
        self._update_status_bar()

    def _update_status_bar(self):
        self._status_db_lbl.setText(f"DB: {DB_PATH}   ·   Data: {DATA_DIR}")
        count = self.db.count()
        self._status_count_lbl.setText(f"{count} active subject(s) in database")

    def _on_patient_selected(self, record: dict | None):
        self._selected_patient = record
        self.anon_tab.update_patient_label(record)
        self.ai_tab.update_patient_label(record)

    def refresh_patients(self):
        self.patients_tab.refresh()
        self._update_status_bar()

    def closeEvent(self, event):
        self.db.close()
        event.accept()

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(GLOBAL_QSS)

    # High DPI support
    app.setStyle("Fusion")

    window = GaitSharingApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
