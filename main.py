import sqlite3
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, \
    QMainWindow, QTableWidget, QTableWidgetItem, QDialog, QComboBox, QToolBar, QStatusBar, QMessageBox
from PyQt6.QtGui import QAction, QIcon
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(800, 500)

        grid = QGridLayout()

        file_menu = self.menuBar().addMenu("&File")
        help_menu = self.menuBar().addMenu("&Help")
        edit_menu = self.menuBar().addMenu(("&Edit"))
        add_student_action = QAction(QIcon("icons/add.png"), "Add Student", self)
        add_student_action.triggered.connect(self.insert)

        file_menu.addAction(add_student_action)
        about_action = QAction("About", self)
        help_menu.addAction(about_action)

        search_action = QAction(QIcon("icons/search.png"), "Search", self)
        search_action.triggered.connect(self.search)
        edit_menu.addAction(search_action)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("ID", "Name", "Course", "Phone number"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)
        self.load_data()

        # Toolbar
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

        # Status bar
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Detect a cell clicked
        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        children = self.findChildren(QPushButton)
        if not children:
            self.statusbar.addWidget(edit_button)
            self.statusbar.addWidget(delete_button)

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def load_data(self):
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        self.table

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        dialog = SearchDialog()
        dialog.exec()
class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete student data")
        layout = QGridLayout()
        confirmation = QLabel("Are you sure you want to delete this record?")
        yes = QPushButton("Yes")
        no = QPushButton("No")
        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no, 1, 1)
        self.setLayout(layout)

        yes.clicked.connect(self.delete_student)
    def delete_student(self):
        #Get student id
        index = main_Window.table.currentRow()
        self.student_id = main_Window.table.item(index, 0).text()

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        cursor.execute("DELETE from students WHERE  id = ?", (self.student_id, ))
        connection.commit()
        cursor.close()
        connection.close()
        main_Window.load_data()

        self.close()
        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("The record was deleted successfully")
        confirmation_widget.exec()

class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update student data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Edit student name
        index = main_Window.table.currentRow()
        current_name = main_Window.table.item(index, 1).text()

        self.student_id = main_Window.table.item(index, 0).text()

        self.student_name = QLineEdit(current_name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Add course
        current_course = main_Window.table.item(index,2).text()
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Physics", "Astronomy"]
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(current_course)
        layout.addWidget(self.course_name)

        # Add phone number
        current_phone = main_Window.table.item(index,3).text()
        self.phone_number = QLineEdit(current_phone)
        self.phone_number.setPlaceholderText("Phone number:")
        layout.addWidget(self.phone_number)

        # Add submit button
        button = QPushButton("Update")
        button.clicked.connect(self.update_student)
        layout.addWidget(button)

        self.setLayout(layout)
    def update_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.phone_number.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        cursor.execute("UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?", (name, course, mobile, self.student_id))
        connection.commit()
        cursor.close()
        connection.close()
        main_Window.load_data()

class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert student data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Add student name
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name:")
        layout.addWidget(self.student_name)

        # Add course
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Physics", "Astronomy"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        # Add phone number
        self.phone_number = QLineEdit()
        self.phone_number.setPlaceholderText("Phone number:")
        layout.addWidget(self.phone_number)

        # Add submit button
        button = QPushButton("Register")
        button.clicked.connect(self.add_Student)
        layout.addWidget(button)

        self.setLayout(layout)

    def add_Student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.phone_number.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)",
                       (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        main_Window.load_data()

class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Seach student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        self.search_name = QLineEdit()
        self.search_name.setPlaceholderText("Name")
        layout.addWidget(self.search_name)

        # Add search button
        button = QPushButton("Search")
        button.clicked.connect(self.search)
        layout.addWidget(button)

        self.setLayout(layout)

    def search(self):
        name = self.search_name.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM students WHERE name =?", (name,))
        rows = list(result)
        print(rows)
        items = main_Window.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            print(item)
            main_Window.table.item(item.row(), 1).setSelected(True)
        cursor.close()
        connection.close()


app = QApplication(sys.argv)
main_Window = MainWindow()
main_Window.show()
sys.exit(app.exec())
