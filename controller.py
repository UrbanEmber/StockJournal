import re
from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox
from PyQt6.QtGui import QColor
import csv
import os
from PyQt6.QtCore import QDate

CSV_FILE = "trades.csv"

class TradeController:
    def __init__(self, ui):
        self.ui = ui
        self.trade_results = {}

        # Connect buttons to functions
        self.ui.save_button.clicked.connect(self.save_trade)

        # Load previous trades
        self.load_trades()

    def load_trades(self):
        """ Loads previous trades from CSV """
        if os.path.exists(CSV_FILE):
            with open(CSV_FILE, mode="r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 5:
                        trade_date, ticker, entry_price, exit_price, result_text = row

                        row_count = self.ui.trade_table.rowCount()
                        self.ui.trade_table.insertRow(row_count)

                        self.ui.trade_table.setItem(row_count, 0, QTableWidgetItem(trade_date))
                        self.ui.trade_table.setItem(row_count, 1, QTableWidgetItem(ticker))
                        self.ui.trade_table.setItem(row_count, 2, QTableWidgetItem(entry_price))
                        self.ui.trade_table.setItem(row_count, 3, QTableWidgetItem(exit_price))

                        result_item = QTableWidgetItem(result_text)
                        result_color = QColor("green") if "+" in result_text else QColor("red")
                        result_item.setBackground(result_color)
                        self.ui.trade_table.setItem(row_count, 4, result_item)

                        self.trade_results[trade_date] = (result_text, result_color.name())

    def is_valid_number(self, value: str) -> bool:
        """ Validates whether the input is a valid integer or float """
        return re.match(r"^-?\d+(\.\d+)?$", value) is not None

    def save_trade(self):
        """ Validates inputs, saves trade, and updates UI """
        ticker = self.ui.ticker_input.text().strip()
        entry_price = self.ui.entry_input.text().strip()
        exit_price = self.ui.exit_input.text().strip()
        trade_date = QDate.currentDate().toString("yyyy-MM-dd")

        # Validate entry & exit price
        if not self.is_valid_number(entry_price) or not self.is_valid_number(exit_price):
            self.show_error("Entry and Exit price must be valid numbers!")
            return  # Prevent execution on invalid input

        entry = float(entry_price)
        exit = float(exit_price)
        profit_loss = round(exit - entry, 2)
        result_text = f"{'+' if profit_loss >= 0 else '-'}${abs(profit_loss)}"
        result_color = QColor("green") if profit_loss >= 0 else QColor("red")
        self.trade_results[trade_date] = (result_text, result_color.name())

        # Save to CSV
        with open(CSV_FILE, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([trade_date, ticker, entry_price, exit_price, result_text])

        # Update Table UI
        row_count = self.ui.trade_table.rowCount()
        self.ui.trade_table.insertRow(row_count)

        self.ui.trade_table.setItem(row_count, 0, QTableWidgetItem(trade_date))
        self.ui.trade_table.setItem(row_count, 1, QTableWidgetItem(ticker))
        self.ui.trade_table.setItem(row_count, 2, QTableWidgetItem(entry_price))
        self.ui.trade_table.setItem(row_count, 3, QTableWidgetItem(exit_price))

        # Display profit/loss with colored background
        result_item = QTableWidgetItem(result_text)
        result_item.setBackground(result_color)
        self.ui.trade_table.setItem(row_count, 4, result_item)

        # Clear input fields
        self.ui.ticker_input.clear()
        self.ui.entry_input.clear()
        self.ui.exit_input.clear()

    def show_error(self, message: str):
        """ Displays an error message when invalid input is entered """
        error_dialog = QMessageBox()
        error_dialog