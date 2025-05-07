import re
from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox, QCalendarWidget, QStyledItemDelegate
from PyQt6.QtGui import QColor, QTextCharFormat
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

    def validate_csv_row(self, row):
        print(f"Validating row: {row}")  # ✅ Debug output

        if len(row) != 5:
            print("Row length is incorrect!")
            return False

        trade_date, ticker, entry_price, exit_price, result_text = [item.strip() for item in row]

        # Validate date format
        if not QDate.fromString(trade_date, "yyyy-MM-dd").isValid():
            print("Invalid date format!")
            return False

        # Validate entry/exit prices
        try:
            entry = round(float(entry_price.replace(",", ".")), 2)
            exit = round(float(exit_price.replace(",", ".")), 2)
        except ValueError:
            print("Invalid price format!")
            return False

        # Validate profit/loss format (removing $ and +)
        cleaned_result = result_text.replace("$", "").replace("+", "")
        try:
            profit_loss = round(float(cleaned_result), 2)
        except ValueError:
            print("Invalid profit/loss format!")
            return False

        print("Row is valid!")
        return True

    def load_trades(self):
        """ Loads and displays previous trades from CSV safely """
        if not os.path.exists(CSV_FILE):
            print(f"{CSV_FILE} does not exist!")  # Debug output
            return

        with open(CSV_FILE, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                print(f"Loaded row: {row}")  # ✅ Debugging: See if rows are being read

                if not self.validate_csv_row(row):
                    print(f"Skipping invalid row: {row}")  # ✅ Debugging: If row fails validation
                    continue

                trade_date, ticker, entry_price, exit_price, result_text = [item.strip() for item in row]

                row_count = self.ui.trade_table.rowCount()
                self.ui.trade_table.insertRow(row_count)

                self.ui.trade_table.setItem(row_count, 0, QTableWidgetItem(trade_date))
                self.ui.trade_table.setItem(row_count, 1, QTableWidgetItem(ticker))
                self.ui.trade_table.setItem(row_count, 2, QTableWidgetItem(f"{float(entry_price):.2f}"))
                self.ui.trade_table.setItem(row_count, 3, QTableWidgetItem(f"{float(exit_price):.2f}"))

                # Format profit/loss correctly
                cleaned_result = result_text.replace("$", "").replace("+", "")
                profit_loss = round(float(cleaned_result), 2)

                result_item = QTableWidgetItem(f"${profit_loss:.2f}")
                result_color = QColor("green") if profit_loss >= 0 else QColor("red")
                result_item.setBackground(result_color)
                self.ui.trade_table.setItem(row_count, 4, result_item)

                self.trade_results[trade_date] = profit_loss

        # ✅ Force table refresh
        self.ui.trade_table.viewport().update()

    def is_valid_number(self, value: str) -> bool:
        """ Checks if the input is a valid float or integer """
        try:
            float(value)  # Try converting to float
            return True
        except ValueError:
            return False

    def save_trade(self):
        """ Saves trade to CSV, updates UI, and prevents crashes """
        ticker = self.ui.ticker_input.text().strip().upper()
        entry_price = self.ui.entry_input.text().strip().replace(',', '.')
        exit_price = self.ui.exit_input.text().strip().replace(',', '.')
        trade_date = QDate.currentDate().toString("yyyy-MM-dd")

        # Validate prices
        if not self.is_valid_number(entry_price) or not self.is_valid_number(exit_price):
            self.show_error("Entry and Exit price must be valid numbers!")
            return

        try:
            entry = round(float(entry_price), 2)
            exit = round(float(exit_price), 2)
            profit_loss = round(exit - entry, 2)
        except ValueError:
            self.show_error("Invalid number format!")
            return

        result_text = f"{'+' if profit_loss >= 0 else '-'}${abs(profit_loss):.2f}"
        result_color = QColor("green") if profit_loss >= 0 else QColor("red")

        # **Safe CSV Handling**
        try:
            with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([trade_date, ticker, f"{entry:.2f}", f"{exit:.2f}", result_text])
        except Exception as e:
            with open("error_log.txt", "a") as log_file:
                log_file.write(f"Error writing to CSV: {e}\n")
            self.show_error(f"An error occurred while saving: {e}")

        # **Update Table UI**
        row_count = self.ui.trade_table.rowCount()
        self.ui.trade_table.insertRow(row_count)

        self.ui.trade_table.setItem(row_count, 0, QTableWidgetItem(trade_date))
        self.ui.trade_table.setItem(row_count, 1, QTableWidgetItem(ticker))
        self.ui.trade_table.setItem(row_count, 2, QTableWidgetItem(f"{entry:.2f}"))
        self.ui.trade_table.setItem(row_count, 3, QTableWidgetItem(f"{exit:.2f}"))

        result_item = QTableWidgetItem(result_text)
        result_item.setBackground(result_color)
        self.ui.trade_table.setItem(row_count, 4, result_item)

        # **Clear input fields**
        self.ui.ticker_input.clear()
        self.ui.entry_input.clear()
        self.ui.exit_input.clear()

        # **Update calendar UI**
        self.update_calendar_colors()

    def update_calendar_colors(self):
        """ Updates the calendar to show profit/loss per day using red and green colors. """

        # Reset all text formats before applying new ones
        default_format = QTextCharFormat()
        self.ui.calendar.setDateTextFormat(QDate(), default_format)  # Reset all

        for trade_date, total_profit_loss in self.trade_results.items():
            formatted_date = QDate.fromString(trade_date, "yyyy-MM-dd")

            if formatted_date.isValid():
                text_format = QTextCharFormat()
                color = QColor("green") if total_profit_loss > 0 else QColor("red")
                text_format.setBackground(color)

                result_text = f"{'+' if total_profit_loss >= 0 else '-'}${abs(total_profit_loss)}"
                self.ui.calendar.setDateTextFormat(formatted_date, text_format)

        # Force calendar refresh
        self.ui.calendar.update()

    def show_error(self, message: str):
        """ Displays an error message when invalid input is entered """
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Icon.Warning)
        error_dialog.setText(message)
        error_dialog.setWindowTitle("Input Error")
        error_dialog.exec()