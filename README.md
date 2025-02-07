# To-Do Desktop Application

A feature-rich, user-friendly to-do list desktop application built with Python, CustomTkinter, and tkcalendar. This application allows users to easily manage tasks with functionalities such as task creation, editing, deletion, and completion tracking.

## Features

- **Task Creation:**  
  - Add tasks with a title, description, due date (selectable via calendar), and priority.
- **Task Listing:**  
  - View all tasks in a scrollable list with details.
- **Task Editing:**  
  - Modify task details using a dedicated edit window.
- **Task Completion:**  
  - Mark tasks as completed with visual cues.
- **Task Deletion:**  
  - Remove unwanted tasks after confirmation.

## Installation

### Prerequisites

- [Python 3.x](https://www.python.org/downloads/) installed on your system.
- (Optional) A virtual environment is recommended.

### Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/bektas-sari/todo-app-desktop.git
   cd todo-app-desktop

2. **Create and activate a virtual environment (recommended):**
For Windows:
python -m venv venv
venv\Scripts\activate

Fro Mac/Linux:
python3 -m venv venv
source venv/bin/activate

3. **Install the required dependencies:**
pip install -r requirements.txt

## Usage
To run the application, simply execute:
python main.py
A window will open where you can add, edit, complete, and delete tasks using an intuitive interface.

## Building a Standalone Executable
For users who prefer a one-click solution without installing Python, you can convert the application to an executable using PyInstaller.

Install PyInstaller:

pip install pyinstaller
Build the executable:

From the project directory, run:

pyinstaller --onefile --windowed main.py
The --onefile flag packages the app into a single executable.
The --windowed flag ensures no console window opens (for GUI applications).

Find the executable:
After the build completes, the executable will be located in the dist folder. You can distribute this file to users, who can run it with a double-click.

## Contributing
Contributions, suggestions, and bug reports are welcome. Please feel free to open an issue or submit a pull request.

## License
This project is licensed under the MIT License.