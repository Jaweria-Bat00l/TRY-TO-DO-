import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QLabel, 
                             QLineEdit, QCheckBox, QListWidgetItem, QCalendarWidget, QDialog, QTimeEdit, QInputDialog,
                             QFileDialog, QMessageBox)
from PyQt5.QtGui import QFont, QPixmap, QPainter, QBrush, QIcon
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import QFileDialog


class TodoApp(QWidget):
    def __init__(self, username, profile_picture_path=None):
        super().__init__()
        self.username = username
        self.profile_picture_path = profile_picture_path
        

        self.selected_date = None


        # Initialize tasks (empty list)
        self.scheduled_tasks = []

        # Main Window Configuration
        self.setWindowTitle("Try To Do")
        self.setGeometry(100, 100, 1100, 800)
        self.setStyleSheet("background-color: #9C88FF;")

        # Main Layout
        main_layout = QHBoxLayout(self)

        # Sidebar Layout
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(20, 20, 20, 20)
        sidebar_layout.setSpacing(15)

        # Sidebar Container
        sidebar_container = QWidget()
        sidebar_container.setStyleSheet("background-color: #FFFFFF; border-radius: 10px;")
        sidebar_container.setLayout(sidebar_layout)

        # Logo Label
        logo_label = QLabel()
        logo_pixmap = QPixmap("C:/Users/JAWERIA/Downloads/Try To Do/trytodo logo.png")
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(logo_label, alignment=Qt.AlignCenter)

        # Profile Picture Handling 
        if self.profile_picture_path:
            profile_pic_label = QLabel(self)
            profile_pic_label.setFixedSize(150, 150)

            # Load and mask the image
            pixmap = QPixmap(self.profile_picture_path).scaled(150, 150, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            circular_mask = QPixmap(150, 150)
            circular_mask.fill(Qt.transparent)

            painter = QPainter(circular_mask)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setBrush(QBrush(Qt.black))
            painter.drawEllipse(0, 0, 150, 150)
            painter.end()

            pixmap.setMask(circular_mask.mask())
            profile_pic_label.setPixmap(pixmap)
            profile_pic_label.setStyleSheet("margin-bottom: 20px; border: 2px solid #9C88FF;")
            sidebar_layout.addWidget(profile_pic_label, alignment=Qt.AlignCenter)

        # Username Label
        subtitle_label = QLabel(username)
        subtitle_label.setFont(QFont("Arial", 18, QFont.Bold))
        subtitle_label.setStyleSheet("color: #4A4A4A; margin-bottom: 30px;")
        sidebar_layout.addWidget(subtitle_label, alignment=Qt.AlignCenter)

        # Sidebar buttons for task categories
        filters = ["Rate Us"]  # Removed "Today tasks" filter
        self.filter_buttons = {}

        for filter_name in filters:
            filter_button = QPushButton(filter_name)
            filter_button.setFont(QFont("Arial", 12))
            filter_button.setStyleSheet(""" 
                QPushButton {
                    background-color: #9C88FF;
                    border: none;
                    text-align: left;
                    padding: 10px 20px;
                    border-radius: 10px;
                    margin-bottom: 10px;
                    color: #FFFFFF;
                }
                QPushButton:hover {
                    background-color: #8A7FFF;
                }
            """)
            # Link the button to the "Rate Us" dialog function
            filter_button.clicked.connect(self.open_rate_us_dialog)
            sidebar_layout.addWidget(filter_button)
            self.filter_buttons[filter_name] = filter_button

        # Add sidebar to main layout
        main_layout.addWidget(sidebar_container, 1)

        # Task Area Layout 
        self.task_layout = QVBoxLayout()
        self.task_layout.setContentsMargins(30, 30, 30, 30)

        focus_label = QLabel("Try To Do")
        focus_label.setFont(QFont("Arial", 20, QFont.Bold))
        focus_label.setStyleSheet("color: #FFFFFF; margin-bottom: 20px;")
        self.task_layout.addWidget(focus_label)

        # Task Input Box
        task_input_layout = QHBoxLayout()
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("What is your next task?")
        self.task_input.setFont(QFont("Arial", 12))
        self.task_input.setStyleSheet(""" 
            QLineEdit {
                background-color: #FFFFFF;
                padding: 10px;
                border: 1px solid #DDDDDD;
                border-radius: 10px;
                color: #4A4A4A;
            }
        """)
        task_input_layout.addWidget(self.task_input)

        # Calendar and Time input
        self.calendar_button = QPushButton("📅")
        self.calendar_button.setFont(QFont("Arial", 12))
        self.calendar_button.setStyleSheet("background-color: #FFFFFF; border-radius: 10px;")
        self.calendar_button.clicked.connect(self.show_calendar)
        task_input_layout.addWidget(self.calendar_button)

        self.time_input = QTimeEdit()
        self.time_input.setDisplayFormat("HH:mm")
        self.time_input.setFont(QFont("Arial", 12))
        self.time_input.setStyleSheet(""" 
            QTimeEdit {
                background-color: #FFFFFF;
                border-radius: 10px;
                color: #4A4A4A;
                padding: 5px;
            }
        """)
        task_input_layout.addWidget(self.time_input)

        add_task_button = QPushButton("+")
        add_task_button.setFont(QFont("Arial", 18))
        add_task_button.setStyleSheet(""" 
            QPushButton {
                background-color: #FFFFFF;
                padding: 5px;
                border: none;
                color: #888888;
                width: 40px;
                height: 40px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #EEEEEE;
            }
        """)
        add_task_button.clicked.connect(self.add_task)
        task_input_layout.addWidget(add_task_button)
        self.task_layout.addLayout(task_input_layout)

        # Task List
        self.task_list = QListWidget()
        self.task_list.setFont(QFont("Arial", 14))
        self.task_list.setStyleSheet(""" 
            QListWidget {
                background-color: #9C88FF;
                border: none;
                color: #4A4A4A;
            }
        """)
        self.task_layout.addWidget(self.task_list)

        main_layout.addLayout(self.task_layout, 3)
        self.setLayout(main_layout)


    def open_rate_us_dialog(self):
        """Open a dialog to rate the app with stars."""
        self.rate_dialog = QDialog(self)
        self.rate_dialog.setWindowTitle("Rate Us")
        self.rate_dialog.setGeometry(200, 200, 300, 200)
        self.rate_dialog.setStyleSheet("background-color: #FFFFFF;")
        
        layout = QVBoxLayout(self.rate_dialog)
        
        # Title Label
        title_label = QLabel("Rate Try To Do")
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        title_label.setStyleSheet("color: #4A4A4A; margin-bottom: 20px;")
        layout.addWidget(title_label, alignment=Qt.AlignCenter)
        
        # Star Buttons
        star_layout = QHBoxLayout()
        self.stars = []  # List to hold star buttons
        for i in range(1, 6):  # 5 stars
            star_button = QPushButton("★")
            star_button.setFont(QFont("Arial", 24))
            star_button.setFixedSize(40, 40)
            star_button.setStyleSheet(""" 
                QPushButton {
                    background-color: #FFFFFF;
                    border: none;
                    color: #FFD700;
                }
                QPushButton:hover {
                    color: #FFC107;
                }
            """)
            star_button.clicked.connect(lambda checked, rating=i: self.submit_rating(rating))
            self.stars.append(star_button)
            star_layout.addWidget(star_button)
        
        layout.addLayout(star_layout)

        # Close Button
        close_button = QPushButton("Close")
        close_button.setFont(QFont("Arial", 14))
        close_button.setStyleSheet(""" 
            QPushButton {
                background-color: #9C88FF;
                color: #FFFFFF;
                border-radius: 10px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #8A7FFF;
            }
        """)
        close_button.clicked.connect(self.rate_dialog.close)
        layout.addWidget(close_button, alignment=Qt.AlignCenter)

        self.rate_dialog.exec_()

    def submit_rating(self, rating):
        QMessageBox.information(self, "Thank You!", f"Thank you for rating us {rating} stars!")
        self.rate_dialog.close()

    def switch_task_view(self, filter_name):
        self.task_list.clear()
        if filter_name == "Rate Us":
            self.display_tasks("scheduled")

    def display_tasks(self, category):
        self.task_list.clear()
        if category == "scheduled":
            # Sort tasks by due date before displaying them
            self.insertion_sort_tasks(self.scheduled_tasks)
            for task in self.scheduled_tasks:
                self.create_task_item(task)



    def insertion_sort_tasks(self, tasks):
        """Sort tasks using insertion sort based on the due date."""
        for i in range(1, len(tasks)):
            key = tasks[i]
            j = i - 1
            # Compare due dates
            while j >= 0 and self.get_due_date(tasks[j]) > self.get_due_date(key):
                tasks[j + 1] = tasks[j]
                j -= 1
            tasks[j + 1] = key


    def add_task(self):
        task_text = self.task_input.text().strip()
        task_time = self.time_input.time().toString("HH:mm")
        if task_text:
            if self.selected_date:  # Scheduled task
                task_text += f" (Due: {self.selected_date}) at {task_time}"
                self.scheduled_tasks.append((task_text, self.selected_date))
            else:  # For unscheduled tasks
                task_text += f" (No due date) at {task_time}"
                self.scheduled_tasks.append((task_text, "9999-12-31"))  # Default far future date

            # Directly display the tasks after adding
            self.display_tasks("scheduled")
            self.task_input.clear()
            self.selected_date = None



    def create_task_item(self, task_data):
        task_text, due_date = task_data
        if due_date == "9999-12-31":
            due_date_display = "No due date"
        else:
            due_date_display = due_date
        task_text = f"{task_text.split('(')[0]} (Due: {due_date_display})"


        task_text, due_date = task_data
        task_item = QListWidgetItem()
        task_item.setTextAlignment(Qt.AlignLeft)
        task_widget = QWidget()
        task_layout = QHBoxLayout(task_widget)
        task_layout.setAlignment(Qt.AlignLeft)
         # Task Checkbox
        checkbox = QCheckBox()
        checkbox.setStyleSheet("QCheckBox { font-size: 18px; }")
        task_layout.addWidget(checkbox)
        # Task Label
        task_label = QLabel(task_text)
        task_label.setStyleSheet(""" 
            QLabel {
                font-size: 16px;
                background-color: white;
                padding: 20px;
                border-radius: 10px;
                color: #4A4A4A;
            }
        """)
        task_layout.addWidget(task_label)

         # Edit Button with Icon
        edit_button = QPushButton()
        edit_button.setFixedSize(27, 27)
        edit_button.setIcon(QIcon("C:/Users/JAWERIA/Downloads/Try To Do/edit.png"))  # Replace with your edit icon file
        edit_button.setIconSize(edit_button.size())  # Set icon size to match button
        edit_button.setStyleSheet(""" 
          QPushButton {
                background-color: #FFFFFF;
                 border-radius: 15px;
            }
        """)
        edit_button.clicked.connect(lambda: self.edit_task(task_label, task_item))
        task_layout.addWidget(edit_button)

         # Delete Button with Icon
        delete_button = QPushButton()
        delete_button.setFixedSize(27, 27)
        delete_button.setIcon(QIcon("C:/Users/JAWERIA/Downloads/Try To Do/delete.png"))
        delete_button.setIconSize(delete_button.size())  # Set icon size to match button
        delete_button.setStyleSheet(""" 
             QPushButton {
                background-color: #FFFFFF;
                border-radius: 15px;
            }
        """)
        delete_button.clicked.connect(lambda: self.delete_task(task_item))
        task_layout.addWidget(delete_button)

        task_item.setSizeHint(task_widget.sizeHint())
        task_widget.setLayout(task_layout)
        self.task_list.addItem(task_item)
        self.task_list.setItemWidget(task_item, task_widget)

 
    def edit_task(self, task_label, task_item):
        new_text, ok = QInputDialog.getText(self, "Edit Task", "Edit your task:", text=task_label.text())
        if ok and new_text:
             # Update the label text and the task data
            task_label.setText(new_text)
            
            # Update the corresponding task in the data structure
            task_index = self.get_task_index(task_item)
            if task_index is not None:
                self.scheduled_tasks[task_index] = (new_text, self.scheduled_tasks[task_index][1])
    
    def get_task_index(self, task_item):
        """ Helper function to get the task index """
        task_widget = self.task_list.itemWidget(task_item)
        task_label = task_widget.findChild(QLabel)
        task_text = task_label.text()
        
        # Find the task in scheduled tasks and return its index
        for idx, (task, _) in enumerate(self.scheduled_tasks):
            if task == task_text:
                return idx
        return None
    
    def delete_task(self, task_item):
        task_widget = self.task_list.itemWidget(task_item)
        task_label = task_widget.findChild(QLabel)
        task_text = task_label.text()

        # Remove task from the scheduled list
        task_index = self.get_task_index(task_item)
        if task_index is not None:
            del self.scheduled_tasks[task_index]

        # Remove from UI
        row = self.task_list.row(task_item)
        self.task_list.takeItem(row)

    def show_calendar(self):
        self.calendar_dialog = QDialog(self)
        self.calendar_dialog.setWindowTitle("Select Date")
        self.calendar_widget = QCalendarWidget(self.calendar_dialog)
        self.calendar_widget.clicked.connect(self.set_selected_date)
        self.calendar_dialog.setLayout(QVBoxLayout())
        self.calendar_dialog.layout().addWidget(self.calendar_widget)
        self.calendar_dialog.exec_()

    def set_selected_date(self, date):
        self.selected_date = date.toString("yyyy-MM-dd")
        self.task_input.setText(self.task_input.text() + f" (Due: {self.selected_date})")  # Display date in task input
        self.calendar_dialog.accept()

    def get_due_date(self, task_data):
        """ Helper function to extract and return due date for sorting """
        return task_data[1]  # task_data[1] contains the due date




class StartWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Try To Do")
        self.setGeometry(100, 100, 400, 300)  # Adjusted height for new elements
        layout = QVBoxLayout(self)

        # Title Label Styling
        title_label = QLabel("Try To Do")
        title_label.setFont(QFont("Arial", 24))
        title_label.setStyleSheet("color: #FFFFFF; margin-bottom: 20px;")
        layout.addWidget(title_label)

        # Username Input Box Styling
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Enter your name")
        self.username_input.setFont(QFont("Arial", 16))
        self.username_input.setStyleSheet("""
            QLineEdit {
                background-color: #FFFFFF;
                padding: 10px;
                border: 1px solid #DDDDDD;
                border-radius: 10px;
                color: #4A4A4A;
            }
        """)
        layout.addWidget(self.username_input)

        # Profile Picture Button and Preview
        self.profile_pic_button = QPushButton("Choose Profile Picture", self)
        self.profile_pic_button.setFont(QFont("Arial", 16))
        self.profile_pic_button.setStyleSheet("""
            QPushButton {
                background-color: #9C88FF;
                border: none;
                padding: 10px 20px;
                border-radius: 10px;
                color: #FFFFFF;
            }
            QPushButton:hover {
                background-color: #8A7FFF;
            }
        """)
        self.profile_pic_button.clicked.connect(self.select_profile_picture)
        layout.addWidget(self.profile_pic_button)

        self.profile_pic_preview = QLabel(self)
        self.profile_pic_preview.setFixedSize(100, 100)
        self.profile_pic_preview.setStyleSheet("background-color: #FFFFFF; border: 1px solid #DDDDDD;")
        self.profile_pic_preview.hide()  # This hides the white square box
        layout.addWidget(self.profile_pic_preview)


        # OK Button Styling
        self.ok_button = QPushButton("OK", self)
        self.ok_button.setFont(QFont("Arial", 16))
        self.ok_button.setStyleSheet("""
            QPushButton {
                background-color: #9C88FF;
                border: none;
                padding: 10px 20px;
                border-radius: 10px;
                color: #FFFFFF;
            }
            QPushButton:hover {
                background-color: #8A7FFF;
            }
        """)
        self.ok_button.clicked.connect(self.start_task_manager)
        layout.addWidget(self.ok_button)

        self.setStyleSheet("background-color: #9C88FF;")
        self.selected_picture_path = None  # To store selected image path

    def select_profile_picture(self):
        # Open a file dialog to select an image
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Profile Picture", "",
                                                "Images (*.png *.jpg *.jpeg *.bmp);;All Files (*)", options=options)
        if file_path:  # Check if the user selected a file
            pixmap = QPixmap(file_path)
            if pixmap.isNull():  # Check if the pixmap failed to load
                QMessageBox.warning(self, "Invalid Image", "The selected file is not a valid image.")
                return
            self.selected_picture_path = file_path
            self.profile_pic_button.setText("Picture Selected ✅")
        else:
            self.selected_picture_path = None
            self.profile_pic_button.setText("Choose Profile Picture")


    def start_task_manager(self):
        username = self.username_input.text()
        if username:
            self.hide()  # Hide the start window instead of closing it
            self.task_manager = TodoApp(username, self.selected_picture_path)  # Pass picture path
            self.task_manager.show()
        else:
            QMessageBox.warning(self, "Input Error", "Please enter a valid username.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StartWindow()
    window.show()  # Show StartWindow, instead of exec_()
    sys.exit(app.exec_())
