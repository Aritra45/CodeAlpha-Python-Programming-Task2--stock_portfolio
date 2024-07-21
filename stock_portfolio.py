import tkinter as tk
from tkinter import messagebox
import requests
import pandas as pd


API_KEY = 'TS8XWDDFZUKVMXT7'
BASE_URL = 'https://www.alphavantage.co/query'


portfolio = {}

def get_stock_price(symbol):
    """Fetch the current price of the stock."""
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': '1min',
        'apikey': API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    try:
        last_refreshed = data['Meta Data']['3. Last Refreshed']
        price = data['Time Series (1min)'][last_refreshed]['4. close']
        return float(price)
    except KeyError:
        return None

def add_stock():
    """Add a stock to the portfolio."""
    symbol = entry_symbol.get().upper()
    try:
        shares = int(entry_shares.get())
    except ValueError:
        messagebox.showerror("Invalid input", "Shares must be an integer.")
        return

    price = get_stock_price(symbol)
    if price:
        portfolio[symbol] = {'shares': shares, 'price': price}
        messagebox.showinfo("Success", f"Added {symbol} to portfolio with {shares} shares at ${price:.2f} per share.")
        update_portfolio_view()
        clear_entries()
    else:
        messagebox.showerror("Error", f"Failed to fetch price for {symbol}.")

def remove_stock():
    """Remove a stock from the portfolio."""
    symbol = entry_symbol.get().upper()
    if symbol in portfolio:
        del portfolio[symbol]
        messagebox.showinfo("Success", f"Removed {symbol} from portfolio.")
        update_portfolio_view()
        clear_entries()
    else:
        messagebox.showerror("Error", f"{symbol} not found in portfolio.")

def update_portfolio_view():
    """Update the portfolio view."""
    text_portfolio.delete(1.0, tk.END)
    if not portfolio:
        text_portfolio.insert(tk.END, "Portfolio is empty.\n")
        return

    text_portfolio.insert(tk.END, f"{'Symbol':<10}{'Shares':<10}{'Price':<10}{'Value':<10}\n")
    total_value = 0.0
    for symbol, data in portfolio.items():
        value = data['shares'] * data['price']
        total_value += value
        text_portfolio.insert(tk.END, f"{symbol:<10}{data['shares']:<10}{data['price']:<10.2f}{value:<10.2f}\n")
    text_portfolio.insert(tk.END, f"Total portfolio value: ${total_value:.2f}")

def save_portfolio():
    """Save the portfolio to a CSV file."""
    filename = 'portfolio.csv'
    df = pd.DataFrame.from_dict(portfolio, orient='index')
    df.to_csv(filename)
    messagebox.showinfo("Success", f"Portfolio saved to {filename}.")

def load_portfolio():
    """Load the portfolio from a CSV file."""
    global portfolio
    filename = 'portfolio.csv'
    try:
        df = pd.read_csv(filename, index_col=0)
        portfolio = df.to_dict('index')
        messagebox.showinfo("Success", f"Portfolio loaded from {filename}.")
        update_portfolio_view()
    except FileNotFoundError:
        messagebox.showerror("Error", f"{filename} not found.")

def clear_entries():
    """Clear the input entries."""
    entry_symbol.delete(0, tk.END)
    entry_shares.delete(0, tk.END)

def exit_program():
    """Exit the program."""
    root.destroy()


root = tk.Tk()
root.title("Stock Portfolio Tracker")


tk.Label(root, text="Stock Symbol:").grid(row=0, column=0, padx=10, pady=10)
entry_symbol = tk.Entry(root, width=20)
entry_symbol.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Shares:").grid(row=1, column=0, padx=10, pady=10)
entry_shares = tk.Entry(root, width=20)
entry_shares.grid(row=1, column=1, padx=10, pady=10)

tk.Button(root, text="Add Stock", command=add_stock, width=15).grid(row=2, column=0, padx=10, pady=10)
tk.Button(root, text="Remove Stock", command=remove_stock, width=15).grid(row=2, column=1, padx=10, pady=10)
tk.Button(root, text="Save Portfolio", command=save_portfolio, width=15).grid(row=3, column=0, padx=10, pady=10)
tk.Button(root, text="Load Portfolio", command=load_portfolio, width=15).grid(row=3, column=1, padx=10, pady=10)
tk.Button(root, text="Exit", command=exit_program, width=15).grid(row=4, column=0, columnspan=2, padx=10, pady=10)

text_portfolio = tk.Text(root, width=50, height=10)
text_portfolio.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

update_portfolio_view()


root.mainloop()
