"""
Modern stylesheet for Biometric Systems GUI.
"""
STYLESHEET = """
/* Global */
QWidget {
    background-color: #1e1e2e;
    color: #cdd6f4;
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 13px;
}

QMainWindow {
    background-color: #1e1e2e;
}

/* Group boxes */
QGroupBox {
    font-weight: bold;
    border: 1px solid #45475a;
    border-radius: 8px;
    margin-top: 12px;
    padding: 16px 12px 12px 12px;
    background-color: #313244;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 12px;
    padding: 2px 8px;
    background-color: #313244;
    color: #89b4fa;
    border-radius: 4px;
}

/* Buttons */
QPushButton {
    background-color: #45475a;
    color: #cdd6f4;
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
    min-height: 24px;
}

QPushButton:hover {
    background-color: #585b70;
}

QPushButton:pressed {
    background-color: #89b4fa;
    color: #1e1e2e;
}

QPushButton:disabled {
    background-color: #313244;
    color: #6c7086;
}

QPushButton#primaryButton {
    background-color: #89b4fa;
    color: #1e1e2e;
}

QPushButton#primaryButton:hover {
    background-color: #b4befe;
}

QPushButton#primaryButton:pressed {
    background-color: #cdd6f4;
}

QPushButton#dangerButton {
    background-color: #f38ba8;
    color: #1e1e2e;
}

QPushButton#dangerButton:hover {
    background-color: #eba0ac;
}

/* Line edits */
QLineEdit {
    background-color: #45475a;
    color: #cdd6f4;
    border: 1px solid #585b70;
    border-radius: 6px;
    padding: 8px 10px;
    selection-background-color: #89b4fa;
}

QLineEdit:focus {
    border-color: #89b4fa;
}

QLineEdit:disabled {
    background-color: #313244;
    color: #6c7086;
}

/* Combo box */
QComboBox {
    background-color: #45475a;
    color: #cdd6f4;
    border: 1px solid #585b70;
    border-radius: 6px;
    padding: 8px 12px;
    min-width: 120px;
}

QComboBox:hover {
    border-color: #89b4fa;
}

QComboBox::drop-down {
    border: none;
    width: 24px;
    background: transparent;
}

QComboBox::down-arrow {
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 6px solid #cdd6f4;
    margin-right: 8px;
    width: 0;
    height: 0;
}

QComboBox QAbstractItemView {
    background-color: #313244;
    color: #cdd6f4;
    selection-background-color: #89b4fa;
    selection-color: #1e1e2e;
}

/* List widget */
QListWidget {
    background-color: #313244;
    color: #cdd6f4;
    border: 1px solid #45475a;
    border-radius: 6px;
    padding: 4px;
    outline: none;
}

QListWidget::item {
    padding: 6px 8px;
    border-radius: 4px;
}

QListWidget::item:selected {
    background-color: #89b4fa;
    color: #1e1e2e;
}

QListWidget::item:hover:!selected {
    background-color: #45475a;
}

/* Table widget */
QTableWidget {
    background-color: #313244;
    color: #cdd6f4;
    gridline-color: #45475a;
    border: 1px solid #45475a;
    border-radius: 6px;
}

QTableWidget::item {
    padding: 6px 8px;
}

QTableWidget::item:selected {
    background-color: #89b4fa;
    color: #1e1e2e;
}

QHeaderView::section {
    background-color: #45475a;
    color: #89b4fa;
    padding: 8px;
    border: none;
    border-right: 1px solid #585b70;
    border-bottom: 1px solid #585b70;
}

/* Text edit (log) */
QTextEdit {
    background-color: #11111b;
    color: #a6e3a1;
    border: 1px solid #45475a;
    border-radius: 6px;
    padding: 8px;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 12px;
}

/* Labels */
QLabel {
    color: #cdd6f4;
}

QLabel#heading {
    font-size: 18px;
    font-weight: bold;
    color: #89b4fa;
}

/* Progress bar */
QProgressBar {
    background-color: #313244;
    border: none;
    border-radius: 4px;
    text-align: center;
    height: 20px;
}

QProgressBar::chunk {
    background-color: #89b4fa;
    border-radius: 4px;
}

/* Tab widget */
QTabWidget::pane {
    border: 1px solid #45475a;
    border-radius: 8px;
    top: -1px;
    background-color: #313244;
}

QTabBar::tab {
    background-color: #45475a;
    color: #cdd6f4;
    padding: 10px 20px;
    margin-right: 2px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
}

QTabBar::tab:selected {
    background-color: #313244;
    color: #89b4fa;
    border-bottom: 2px solid #89b4fa;
}

QTabBar::tab:hover:!selected {
    background-color: #585b70;
}

/* Scroll bars */
QScrollBar:vertical {
    background-color: #313244;
    width: 12px;
    border-radius: 6px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background-color: #585b70;
    border-radius: 6px;
    min-height: 24px;
}

QScrollBar::handle:vertical:hover {
    background-color: #89b4fa;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}

QScrollBar:horizontal {
    background-color: #313244;
    height: 12px;
    border-radius: 6px;
}

QScrollBar::handle:horizontal {
    background-color: #585b70;
    border-radius: 6px;
    min-width: 24px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #89b4fa;
}

/* Tool tip */
QToolTip {
    background-color: #313244;
    color: #cdd6f4;
    border: 1px solid #89b4fa;
    border-radius: 4px;
    padding: 4px 8px;
}

/* Menu bar */
QMenuBar {
    background-color: #1e1e2e;
    color: #cdd6f4;
}

QMenuBar::item:selected {
    background-color: #45475a;
    color: #89b4fa;
}

QMenu {
    background-color: #313244;
    color: #cdd6f4;
}

QMenu::item:selected {
    background-color: #89b4fa;
    color: #1e1e2e;
}

/* Status bar */
QStatusBar {
    background-color: #313244;
    color: #6c7086;
    border-top: 1px solid #45475a;
}

/* Footer */
QFrame#footer {
    background-color: #181825;
    border-top: 1px solid #45475a;
    border-radius: 0 0 6px 6px;
    padding: 4px 0;
}

QLabel#footerLabel {
    color: #6c7086;
    font-size: 12px;
    letter-spacing: 0.5px;
}

/* Preview area (modern card) */
QLabel#previewLabel {
    background-color: #181825;
    color: #6c7086;
    border-radius: 8px;
    border: 1px dashed #45475a;
    padding: 12px;
    font-style: italic;
}

/* Tab scroll area - show content and scrollbars */
QScrollArea#tabScrollArea {
    background-color: transparent;
    border: none;
}

QScrollArea#tabScrollArea > QWidget > QWidget {
    background-color: transparent;
}
"""
