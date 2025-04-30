import sys
from PyQt6.QtWidgets import QApplication
from gui import TradeJournalUI
from controller import TradeController

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = TradeJournalUI()
    controller = TradeController(ui)  # Connect UI with Controller
    ui.show()
    sys.exit(app.exec())
