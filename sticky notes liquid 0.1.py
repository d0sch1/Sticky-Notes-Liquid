import os
import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QTextEdit,
                             QVBoxLayout, QWidget, QPushButton, QHBoxLayout,
                             QSizeGrip, QColorDialog)
from PySide6.QtCore import Qt

NOTES_DIR = "notes"
os.makedirs(NOTES_DIR, exist_ok=True)

class NoteWindow(QMainWindow):
    def __init__(self, file_path=None, parent=None):
        super().__init__(parent)
        self.file_path = file_path or os.path.join(NOTES_DIR, f"note_{id(self)}.txt")
        self.setWindowTitle("Note")
        self.setMinimumSize(200, 150)

        # Corrected window flags on a single line for clarity
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint |
                          Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Top bar with buttons
        top_bar = QWidget()
        top_bar_layout = QHBoxLayout(top_bar)

        color_button = QPushButton("...")
        color_button.setToolTip("Change note color")
        color_button.setStyleSheet("QPushButton { background-color: transparent; }")
        color_button.clicked.connect(self.change_color)
        top_bar_layout.addWidget(color_button)

        close_button = QPushButton("X")
        close_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 0, 0, 100);
                color: white;
                border: none;
                border-radius: 3px;
                padding: 0 5px;
            }
            QPushButton:hover {
                background-color: rgba(255, 0, 0, 150);
            }
        """)
        close_button.setMaximumWidth(30)
        close_button.clicked.connect(self.close)

        top_bar_layout.addStretch()
        top_bar_layout.addWidget(color_button)
        top_bar_layout.addWidget(close_button)

        top_bar.setStyleSheet("background-color: rgba(0, 0, 0, 30);")
        main_layout.addWidget(top_bar)

        # Note editor
        self.note_edit = QTextEdit()
        self.note_edit.setStyleSheet("""
            QTextEdit {
                background-color: rgba(255, 255, 255, 180);
                border: none;
                padding: 15px;
                border-radius: 0;
            }
        """)
        main_layout.addWidget(self.note_edit)

        # Resize grip
        resize_grip = QSizeGrip(self)
        resize_grip.setStyleSheet("background-color: transparent;")

        bottom_corner = QWidget()
        bottom_layout = QHBoxLayout(bottom_corner)
        bottom_layout.addStretch()
        bottom_layout.addWidget(resize_grip)

        main_layout.addWidget(bottom_corner)

        # Load note content
        self.load_note()

    def load_note(self):
        try:
            with open(self.file_path, 'r') as f:
                content = f.read()
                self.note_edit.setText(content)
        except FileNotFoundError:
            pass

    def closeEvent(self, event):  # Fixed indentation here
        try:
            with open(self.file_path, 'w') as f:
                f.write(self.note_edit.toPlainText())
        except Exception as e:  # Properly aligned with 'try'
            print(f"Error saving note: {e}")
        super().closeEvent(event)  # Correct level for method

    def change_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.note_edit.setStyleSheet(f"""
                QTextEdit {{
                    background-color: rgba({color.red()}, {color.green()}, {color.blue()}, 180);
                    border: none;
                    padding: 15px;
                    border-radius: 0;
                }}
            """)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint()
            self.window_position = self.pos()

    def mouseMoveEvent(self, event):
        if hasattr(self, 'drag_position'):
            delta = event.globalPosition().toPoint() - self.drag_position
            self.move(self.window_position + delta)

def create_application():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = NoteWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    create_application()
