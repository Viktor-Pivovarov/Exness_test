import requests
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import re
from datetime import datetime
import matplotlib.dates as mdates
import time
import sched
import os

class StockQuote:
    def __init__(self):
        # Test for attempt to connect to SQLite database
        try:
            self.db_conn = sqlite3.connect('test_db.db')
            cursor = self.db_conn.cursor()
            cursor.execute('SELECT SQLITE_VERSION()')
            print("SQLite database connected successfully.")
        except sqlite3.Error as error:
            print("Failed to connect to SQLite database, ", error)

        self.api_token = 'pk_fcf99243c62549b3aba572d2b23d9288'

    # Set the stock symbols after validation
    def set_symbols(self, symbols):
        # Ensure symbols only contain letters and commas
        for symbol in symbols:
            if not re.match(r'^[a-zA-Z,]*$', symbol):
                print("Invalid input. Please only enter latin letters and commas.")
                return False
        # Save the symbols after removing any non-alphabet characters
        self.symbols = [re.sub(r'[^a-zA-Z]', '', symbol) for symbol in symbols]
        return True

    # Retrieve the stock quote from the API
    def get_quote(self):
        symbol_string = ','.join(self.symbols)
        try:
            # Perform the API call and test response status codes
            r = requests.get(f'https://api.iex.cloud/v1/data/core/quote/{symbol_string}?token={self.api_token}')
            if r.status_code == 200:
                data = r.json()
                if data == [None]:
                    print("You entered a wrong symbol, please try again")
                    return None
            elif r.status_code == 403:
                print("The API key provided is not valid.")
                return None
            else:
                print("Service is busy, try again later")
                return None
        except Exception as e:
            print(str(e))
            return None
        return data

    # Retrieve all the data for a symbol from the database
    def get_from_db(self, symbol):
        cursor = self.db_conn.cursor()
        cursor.execute('SELECT * FROM quotes WHERE symbol = ?', (symbol,))
        rows = cursor.fetchall()
        return rows
    
    # Save the retrieved data to the SQLite database
    def save_to_db(self, data):
        df = pd.json_normalize(data)
        df['timestamp'] = datetime.now() 
        df.to_sql('quotes', self.db_conn, if_exists='append', index=False)

    # Plot the results
    def export_plot(self, rows, symbol):
        if os.getenv('EXPORT_PLOT', 'false').lower() == 'true':
            cursor = self.db_conn.cursor()
            cursor.execute('SELECT * FROM quotes WHERE symbol = ?', (symbol,))
            column_names = [column[0] for column in cursor.description]
            df = pd.DataFrame(rows, columns=column_names)

            # Convert 'latestUpdate' from Unix Time Stamp to date/time
            df['latestUpdate'] = pd.to_datetime(df['latestUpdate'], unit='ms')

            # Plot the stock prices and save the figure
            fig, ax = plt.subplots()
            ax.plot(df['latestUpdate'], df['latestPrice'])
            plt.title(f'Stock prices for {symbol}')
            plt.xlabel('Time')
            plt.ylabel('Price')

            # Set the date format
            date_format = mdates.DateFormatter('%d-%m-%Y %H:%M')
            ax.xaxis.set_major_formatter(date_format)

            # Ensure that the date labels don't overlap
            fig.autofmt_xdate()

            now = datetime.now()
            dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
            plt.savefig(f'/app/data/{symbol}_data.png')
            
            print(f'Successfully saved the plot for {symbol} to {symbol}_data.png')
            plt.close(fig)




    # Export the data from db to a CSV file
    def export_to_csv(self, rows, symbol):
        if os.getenv('EXPORT_CSV', 'false').lower() == 'true':
            cursor = self.db_conn.cursor()
            cursor.execute('SELECT * FROM quotes WHERE symbol = ?', (symbol,))
            column_names = [column[0] for column in cursor.description]
            df = pd.DataFrame(rows, columns=column_names)
            now = datetime.now()
            dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
            df.to_csv(f'/app/data/{symbol}_data.csv')

            print(f'Successfully exported the data for {symbol} to {symbol}_data.csv')


def main(*args, **kwargs):
    sq = StockQuote()

    # Get the stock symbols from the environment variable
    symbols = os.getenv('SYMBOLS', '').split(',')

    # If the symbols are valid, get the stock quote
    if sq.set_symbols(symbols):
        data = sq.get_quote()
        # If the stock quote was retrieved successfully, save the data and export it
        if data:
            sq.save_to_db(data)
            for symbol in symbols:
                rows = sq.get_from_db(symbol)
                if rows:
                    sq.export_to_csv(rows, symbol)
                    sq.export_plot(rows, symbol)

def worker(interval, function, scheduler, *args, **kwargs):
    function(*args, **kwargs)
    scheduler.enter(interval, 1, worker, (interval, function, scheduler) + args, kwargs)


if __name__ == "__main__":
    s = sched.scheduler(time.time, time.sleep)
    s.enter(300, 1, worker, (300, main, s)) #loop timer (now 300 sec)
    s.run()

 



