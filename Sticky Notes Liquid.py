from PySide6.QtWidgets import (QApplication, QMainWindow, QTextEdit,
                              QVBoxLayout, QWidget, QPushButton, QHBoxLayout)
from PySide6.QtCore import Qt

def main():
    app = QApplication([])

    class NoteWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
            self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
            self.resize(300, 200)  # Default size

            central_widget = QWidget()
            self.setCentralWidget(central_widget)

            main_layout = QVBoxLayout(central_widget)

            # Top bar with close button
            top_bar = QWidget()
            top_bar_layout = QHBoxLayout(top_bar)
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
            top_bar_layout.addStretch()  # Push button to the right
            top_bar_layout.addWidget(close_button)
            main_layout.addWidget(top_bar)

            # Note editor
            self.note_edit = QTextEdit()
            self.note_edit.setStyleSheet("""
                background-color: rgba(255, 255, 255, 180);
                border: none;
                padding: 15px;
            """)
            main_layout.addWidget(self.note_edit)

        def mousePressEvent(self, event):
            if event.button() == Qt.MouseButton.LeftButton:
                self.drag_position = event.globalPosition().toPoint()
                self.window_position = self.pos()

        def mouseMoveEvent(self, event):
            if hasattr(self, 'drag_position'):
                delta = event.globalPosition().toPoint() - self.drag_position
                self.move(self.window_position + delta)

    window = NoteWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
