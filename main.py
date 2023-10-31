
from PyQt6.QtWidgets import (QApplication, QLabel, QWidget, QGridLayout,
                             QLineEdit, QPushButton, QMainWindow, QTableWidget,
                             QTableWidgetItem, QDialog, QVBoxLayout, QComboBox)
from PyQt6.QtGui import QAction
import sys
import sqlite3


# Define the main window class
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()  # Call the parent init method (QMainWindow)
        self.setWindowTitle("SQL App")

        # Create file and help menu items
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")

        # Create "Add Student" action and connect it to the "insert" method
        add_student_action = QAction("Add Student", self)
        add_student_action.triggered.connect(self.insert)

        # Add "Add Student" action to the file menu
        file_menu_item.addAction(add_student_action)

        # Create "About" action and add it to the help menu
        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)

        # Create a table to display student data
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("ID", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)  # Hide unnecessary column (above row numbers)
        self.setCentralWidget(self.table)

    # Method to load data into the table
    def load_data(self):
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)  # Avoid duplicating data
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()

    # Method to open the insert dialog
    def insert(self):
        dialog = InsertDialog()
        dialog.exec()


# Insert dialog class
class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Add student name widget
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Create a combo box for course
        self.course_name = QComboBox()
        courses = ["Biology", "Physics", "Chemistry"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        # Add mobile widget
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        # Create a submit button
        button_layout = QVBoxLayout()
        button = QPushButton("Submit")
        button.clicked.connect(self.add_student)
        button_layout.addWidget(button)

        # Add the button layout to the main layout
        layout.addLayout(button_layout)

        self.setLayout(layout)

    # Method to add a new student
    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)",
                       (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()


# Create the application
app = QApplication(sys.argv)

# Create an instance of the main window
age_calculator = MainWindow()
age_calculator.show()
age_calculator.load_data()

# Start the application event loop
sys.exit(app.exec())
