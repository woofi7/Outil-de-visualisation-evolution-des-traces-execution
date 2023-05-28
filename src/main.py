from PyQt6.QtWidgets import QApplication
import sys
from view.HomeView import HomeView
from controller.HomeController import HomeController
from model.HomeModel import HomeModel

def main():
    app = QApplication(sys.argv)  # Create a QApplication instance

    # Create instances of the view, model, and controller
    homePage = HomeView()
    homeModel = HomeModel()
    homeController = HomeController(homePage, homeModel)

    sys.exit(app.exec())  # Start the application event loop

if __name__ == "__main__":
    main()
