from PyQt6.QtWidgets import QApplication
import sys
from controller.HomeController import HomeController
from view.HomeView import HomeView
import os
import traceback

def main():
    _create_directory("./repo/")
    app = QApplication(sys.argv)  # Create a QApplication instance
    print("Starting application")
    # Create instances of the view, model, and controller
    HomeController()
    sys.exit(app.exec())  # Start the application event loop

def _create_directory(directory_path):
    try:
        # Create a directory if it doesn't exist
        if not os.path.exists(directory_path):
            try:
                os.makedirs(directory_path)
            except OSError as e:
                print(f"An error occurred while creating the directory: {str(e)}")
    except Exception as e:
        traceback.print_exc()

if __name__ == "__main__":
    main()
