import qt
import io
import dis
import traceback
from code_conversion import code_to_json


class TextArea(qt.QPlainTextEdit):
    def __init__(self, no_wrap=False):
        super().__init__()

        font = qt.QFont()
        font.setFamily('Courier')
        font.setStyleHint(qt.QFont.Monospace)
        font.setFixedPitch(True)
        font.setPointSize(10)
        font_metrics = qt.QFontMetrics(font)

        self.setFont(font)
        self.setTabStopWidth(4 * font_metrics.width(' '))

        if no_wrap:
            self.setLineWrapMode(self.NoWrap)
            self.setWordWrapMode(qt.QTextOption.NoWrap)


class MainWindow(qt.QWidget):
    def __init__(self):
        super().__init__()

        self.hboxwidget = qt.QWidget()
        # self.hboxlayout = qt.QHBoxLayout(self.hboxwidget)
        self.splitter = qt.QSplitter()
        self.splitter.setOrientation(qt.constants.Horizontal)
        self.splitter.setStretchFactor(1, .75)
        self.vboxlayout = qt.QVBoxLayout(self)

        self.code_input = TextArea(True)
        self.dis_output = TextArea(True)

        self.json_compact_checkbox = qt.QCheckBox()
        self.json_compact_checkbox.setText('Compact')
        self.json_compact_checkbox.toggled.connect(self.compile)
        self.json_output_vboxwidget = qt.QWidget()
        self.json_output_vboxlayout = qt.QVBoxLayout(self.json_output_vboxwidget)
        self.json_output_vboxlayout.setContentsMargins(0, 0, 0, 0)
        self.json_output = TextArea()
        self.json_output_vboxlayout.addWidget(self.json_compact_checkbox)
        self.json_output_vboxlayout.addWidget(self.json_output)

        self.compile_button = qt.QPushButton()
        self.compile_button.setText('Compile')
        self.compile_button.clicked.connect(self.compile)

        self.splitter.addWidget(self.code_input)
        self.splitter.addWidget(self.dis_output)
        self.splitter.addWidget(self.json_output_vboxwidget)
        self.vboxlayout.addWidget(self.splitter)
        self.vboxlayout.addWidget(self.compile_button)

        self.setWindowTitle('dis tester')

    def keyPressEvent(self, event: qt.QKeyEvent):
        super().keyPressEvent(event)
        if event.key() == qt.constants.Key_F5:
            self.compile()

    def compile(self):
        code = self.code_input.toPlainText()
        dis_output = io.StringIO()

        try:
            dis.dis(code, file=dis_output)
            json_output = code_to_json(code, compact=self.json_compact_checkbox.isChecked())

        except:
            dis_output.write(traceback.format_exc())
            json_output = ''

        self.dis_output.setPlainText(dis_output.getvalue())
        self.json_output.setPlainText(json_output)


if __name__ == '__main__':
    def main():
        app = qt.QApplication([])
        main_window = MainWindow()
        main_window.show()
        app.exec()

    main()
