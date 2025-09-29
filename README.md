# Daily Eisenhower Matrix Desktop App

A productivity desktop app for daily task management using the Eisenhower Matrix.

## Features
- Drag-and-drop task organization
- Auto-save tasks
- Undo/redo actions
- Custom UI with visually distinct quadrants
- Cross-platform installer
- Rapid onboarding for open-source contributions

## Screenshots


## Installation

1. Clone the repo:

git clone https://github.com/dhruvhptl/eisenhower-matrix.git

2. Install Python dependencies:

pip install customtkinter

3. Run the app:

python main.py

4. Optionally, build a standalone installer using PyInstaller:

pip install pyinstaller
pyinstaller main.py

(Or use the provided Makefile.)

## Usage
- Enter a task in the left panel, select “Important” or “Urgent,” and click "Add Task."
- Tasks appear in the corresponding quadrant, scattered for visual clarity.
- Click on a task to mark as completed/incomplete.
- Use "Clear Matrix" to reset tasks (and delete saved data).
- Closing the app autosaves your tasks.

## License
MIT

## Contributing
Open to feedback, pull requests, and suggestions!

