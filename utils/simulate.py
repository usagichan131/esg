from vnstock3 import Vnstock
import pandas as pd
import numpy as np
from pandas.tseries.offsets import BDay
from .indicators import *
from .strategy import *
from .calculations import get_next_trading_day
from .config import *
def simulate_investment(
    ticker, sell_fraction, start_date, end_date, investment, f_star=1, signal='macd'
):
    try:
        # Initialize trade counters and portfolio metrics
        number_of_buying_trades = 0
        number_of_selling_trades = 0
        cash = investment
        holdings = 0
        portfolio_values = []

        # Load stock data and calculate indicators
        data = Vnstock().stock(symbol=ticker, source='VCI').quote.history(start=start_date, end=end_date)
        data = data.set_index(pd.DatetimeIndex(data['time'].values))
        if signal == 'macd':
            data = calculate_indicators_macd(data)
            data = macd_strategy(data)
        elif signal == 'bb':
            data = calculate_indicators_bb(data)
            data = bb_strategy(data)
        elif signal == 'obv':
            data = calculate_indicators_obv(data)
            data = obv_strategy(data)

        trading_days = data.index
        buy_signals = data[data['Signal'] == 1].index
        sell_signals = data[data['Signal'] == -1].index

        pending_buy_shares = {}
        pending_sell_revenue = {}
        
        data['close'] = data['close']*1000
        for i, current_date in enumerate(data.index):
            current_price = data['close'].iloc[i]

            # Handle pending T+2 settlements
            if current_date in pending_buy_shares:
                holdings += pending_buy_shares.pop(current_date)
            if current_date in pending_sell_revenue:
                cash += pending_sell_revenue.pop(current_date)

            # Avoid trades in January 2024
            if current_date.month == 1 and current_date.year == 2024:
                portfolio_values.append(cash + holdings * current_price)
                continue

            # Buy if there's a buy signal and cash allows
            if current_date in buy_signals:
                allocation = cash * f_star
                shares_to_buy = int(allocation // current_price)
                total_cost = shares_to_buy * current_price
                if shares_to_buy > 0 and cash >= total_cost:
                    cash -= total_cost
                    settlement_date = get_next_trading_day(current_date + BDay(2), trading_days)
                    pending_buy_shares[settlement_date] = pending_buy_shares.get(settlement_date, 0) + shares_to_buy
                    last_buy_price = current_price
                    number_of_buying_trades += 1

            # Sell if there's a sell signal and holdings allow
            if holdings > 0 and current_date in sell_signals:
                shares_to_sell = int(holdings * sell_fraction)
                revenue = shares_to_sell * current_price
                holdings -= shares_to_sell
                settlement_date = get_next_trading_day(current_date + BDay(2), trading_days)
                pending_sell_revenue[settlement_date] = pending_sell_revenue.get(settlement_date, 0) + revenue
                number_of_selling_trades += 1

            # Update portfolio value
            portfolio_values.append(cash + holdings * current_price)

        # Finalize portfolio values including pending settlements
        final_date = data.index[-1]
        while final_date <= data.index[-1] + BDay(2):
            if final_date in pending_buy_shares:
                holdings += pending_buy_shares.pop(final_date)
            if final_date in pending_sell_revenue:
                cash += pending_sell_revenue.pop(final_date)
            portfolio_values.append(cash + holdings * data['close'].iloc[-1])
            final_date += BDay(1)

        # Adjust portfolio values to match data index length
        if len(portfolio_values) > len(data.index):
            portfolio_values = portfolio_values[:len(data.index)]
        elif len(portfolio_values) < len(data.index):
            portfolio_values.extend([portfolio_values[-1]] * (len(data.index) - len(portfolio_values)))

        # Add portfolio values to data frame
        data['Portfolio_Value'] = portfolio_values
        data[f'value_{ticker}'] = portfolio_values
        data['Number_of_Buying_Trades'] = number_of_buying_trades
        data['Number_of_Selling_Trades'] = number_of_selling_trades
        # Ensure the column 'value' is directly modified in the original DataFrame
        data[f'value_{ticker}'] = data[f'value_{ticker}'].apply(lambda x: np.nan if pd.notna(x) and x < 1000000 else x)
        data[f'value_{ticker}'] = data[f'value_{ticker}'].ffill()

        data['Daily_Return'] = data[f'value_{ticker}'].pct_change()
        data['Accumulated_Profit'] = data[f'value_{ticker}'] - investment

        data['Running_Max'] = data[f'value_{ticker}'].cummax()  # Track the running max portfolio value
        data['Drawdown'] = (data[f'value_{ticker}'] - data['Running_Max']) / data['Running_Max']  # Calculate drawdown
        data = data.dropna(subset=['time'])
        data = data.drop_duplicates(subset=['time', 'open', 'high', 'low', 'close', 'volume'], keep='first')
        return data, number_of_buying_trades, number_of_selling_trades
        

    except Exception as e:
        print(f"Error occurred for {ticker}: {e}")
        return pd.DataFrame()
