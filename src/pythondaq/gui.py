import sys

from PySide6 import QtWidgets
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QDoubleSpinBox, QHBoxLayout, QLabel, QWidget, QComboBox

class UserInterface(QtWidgets.QMainWindow):
    pass


class UserInterface(QtWidgets.QMainWindow):
    def __init__(self):
        # initialise the parent class
        super().__init__()

        # create central widget
        # set central widget
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        # create vertical layout
        # set layout of central widget as vertical layout
        vbox = QtWidgets.QVBoxLayout()
        central_widget.setLayout(vbox)

        # create textbox
        # add textbox to vertical layout
        self.textedit = QtWidgets.QTextEdit()
        vbox.addWidget(self.textedit)

        # create horizontal layout
        # add horizontal layout to vertical layout
        hbox = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox)

        # create widgets
        # add widgets to horizontal layout
        clear_button = QtWidgets.QPushButton("Clear")
        hbox.addWidget(clear_button)
        add_text_button = QtWidgets.QPushButton("Add text")
        hbox.addWidget(add_text_button)
        combo = QComboBox()
        combo.addItems(["One", "Two", "Three"])
        hbox.addWidget(combo)

        ## LINE 1: start 
        layout_line_1 = QtWidgets.QHBoxLayout()
        vbox.addLayout(layout_line_1)

        label_1= QLabel("Start waarde (V)")
        spin_box_1 = QtWidgets.QDoubleSpinBox()
        spin_box_1.setRange(0.0, 3.31)
        spin_box_1.setSingleStep(0.01)
        spin_box_1.setValue(0.00)

        layout_line_1.addWidget(label_1)
        layout_line_1.addWidget(spin_box_1)

        ## LINE 2: stop
        layout_line_2 = QtWidgets.QHBoxLayout()
        vbox.addLayout(layout_line_2)

        label_2= QLabel("Stop waarde (V)")
        spin_box_2 = QtWidgets.QDoubleSpinBox()
        spin_box_2.setRange(0.0, 3.31)
        spin_box_2.setSingleStep(0.01)
        spin_box_2.setValue(3.31)

        layout_line_2.addWidget(label_2)
        layout_line_2.addWidget(spin_box_2)

        ## LINE 3: stap
        layout_line_3 = QtWidgets.QHBoxLayout()
        vbox.addLayout(layout_line_3)

        label_3= QLabel("Stapgrootte (V)")
        spin_box_3 = QtWidgets.QDoubleSpinBox()
        spin_box_3.setRange(0.0, 1.0)
        spin_box_3.setSingleStep(0.01)
        spin_box_3.setValue(0.01)

        layout_line_3.addWidget(label_3)
        layout_line_3.addWidget(spin_box_3)

        ## LINE 4: repeat
        layout_line_4 = QtWidgets.QHBoxLayout()
        vbox.addLayout(layout_line_4)

        label_4= QLabel("Herhaalmetingen")
        spin_box_4 = QtWidgets.QSpinBox()
        spin_box_4.setRange(0, 100)
        spin_box_4.setValue(5)

        layout_line_4.addWidget(label_4)
        layout_line_4.addWidget(spin_box_4)




        # slots and signals
        clear_button.clicked.connect(self.textedit.clear)
        add_text_button.clicked.connect(self.add_text_button_clicked)


    # decorate method with Slot function
    @Slot()
    def add_text_button_clicked(self):
        self.textedit.append("You clicked me.")

    


def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = UserInterface()
    ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

