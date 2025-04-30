from PyQt6.QtWidgets import (
    QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QCalendarWidget, QTableWidgetItem
)

class TradeJournalUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Stock Trade Journal")
        self.setGeometry(100, 100, 700, 500)

        # Tab Widget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Creating Tabs
        self.trade_tab = QWidget()
        self.calendar_tab = QWidget()

        self.tabs.addTab(self.trade_tab, "Trades")
        self.tabs.addTab(self.calendar_tab, "Calendar")

        self.setup_trade_tab()
        self.setup_calendar_tab()

    def setup_trade_tab(self):
        """ Sets up the Trade Entry UI """
        layout = QVBoxLayout()

        self.ticker_label = QLabel("Ticker:")
        self.ticker_input = QLineEdit()
        self.entry_label = QLabel("Entry Price:")
        self.entry_input = QLineEdit()
        self.exit_label = QLabel("Exit Price:")
        self.exit_input = QLineEdit()

        layout.addWidget(self.ticker_label)
        layout.addWidget(self.ticker_input)
        layout.addWidget(self.entry_label)
        layout.addWidget(self.entry_input)
        layout.addWidget(self.exit_label)
        layout.addWidget(self.exit_input)

        # Save Button
        self.save_button = QPushButton("Save Trade")
        layout.addWidget(self.save_button)

        # Trade Table (Adds result column)
        self.trade_table = QTableWidget()
        self.trade_table.setColumnCount(5)
        self.trade_table.setHorizontalHeaderLabels(["Date", "Ticker", "Entry", "Exit", "Result"])
        layout.addWidget(self.trade_table)

        self.trade_tab.setLayout(layout)

    def setup_calendar_tab(self):
        """ Sets up the Calendar Tracking UI """
        layout = QVBoxLayout()

        self.calendar = QCalendarWidget()
        layout.addWidget(self.calendar)

        self.calendar_tab.setLayout(layout)
