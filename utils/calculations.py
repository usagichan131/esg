import numpy as np
from pandas.tseries.offsets import BDay
from .config import get_strategy_config
from scipy.stats import norm
import pandas as pd


def kelly_criterion(signal):
    strategy_config = get_strategy_config(signal.upper())
    if not strategy_config:
        raise ValueError(f"Strategy configuration for '{signal}' not found in config.")
    
    # Extract relevant parameters
    win_rate = strategy_config["win_rate"]
    loss_rate = strategy_config["loss_rate"]
    mean_profit = strategy_config["mean_profit"]
    mean_loss = strategy_config["mean_loss"]
    b = mean_profit / mean_loss
    f = (b * win_rate - loss_rate) / b
    if f < 0:
        return -1*f
    else:
        return f


def calculate_daily_risk_free_rate(annual_rate_decimal, trading_days=252):
    return (1 + annual_rate_decimal) ** (1 / trading_days) - 1


def calculate_sharpe_ratio(data, risk_free_rate=0.01):
    daily_returns = data['Daily_Return'].dropna()
    average_return = daily_returns.mean() * 252
    std_deviation = daily_returns.std() * np.sqrt(252)
    return (average_return - risk_free_rate) / std_deviation if std_deviation > 0 else np.nan


def calculate_sortino_ratio(data, risk_free_rate=0.01):
    daily_returns = data['Daily_Return'].dropna()
    average_return = daily_returns.mean() * 252
    downside_returns = daily_returns[daily_returns < 0]
    downside_deviation = downside_returns.std() * np.sqrt(252) if not downside_returns.empty else np.nan
    return (average_return - risk_free_rate) / downside_deviation if downside_deviation > 0 else np.nan


def calculate_var(data, alpha=0.05):
    daily_returns = data['Daily_Return'].dropna()
    mean = daily_returns.mean()
    std_dev = daily_returns.std()
    return norm.ppf(alpha, mean, std_dev)


def get_next_trading_day(date, trading_days):
    while date not in trading_days:
        date += BDay(1)
    return date
