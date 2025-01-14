from .config import *
from .remove_sell import *
from .simulate import *
import pandas as pd
import numpy as np
from .calculations import calculate_sharpe_ratio, calculate_sortino_ratio, calculate_var
from scipy.stats import skew, kurtosis

def portfolio_only_buy(group, start_date, end_date, f_star=1, signal='macd', rf=0):
    initial_investment = 100_000_000
    n = len(group)
    results = pd.DataFrame()
    no_buying_trades = 0
    no_selling_trades = 0

    for ticker in group:
        # Simulate investment for each ticker with equal allocation
        result, buy= simulate_investment(
            ticker, start_date=start_date, end_date=end_date, investment=initial_investment / n, f_star=f_star, signal=signal
        )
        no_buying_trades += buy
        if not result.empty:
            results = pd.concat([results, result[f'value_{ticker}']], axis=1)

    # Calculate portfolio value as the sum of all stock values
    results['Portfolio_Value'] = results.sum(axis=1)
    results['Daily_Return'] = results['Portfolio_Value'].pct_change()
    results['Accumulated_Profit'] = results['Portfolio_Value'] - initial_investment

    # Calculate running max and drawdown
    results['Running_Max'] = results['Portfolio_Value'].cummax()
    results['Drawdown'] = (
        (results['Portfolio_Value'] - results['Running_Max']) 
        / results['Running_Max']
    )

    # Additional metrics
    sharpe_ratio = calculate_sharpe_ratio(results, rf)
    sortino_ratio = calculate_sortino_ratio(results, rf)
    VaR = calculate_var(results)
    RoR = results['Accumulated_Profit'].iloc[-1] / initial_investment*100
    MDD = results['Drawdown'].min()
    skewness = skew(results['Daily_Return'].dropna())
    kurt = kurtosis(results['Daily_Return'].dropna())

    # Create summary metrics table
    metrics = pd.DataFrame({
        'Sharpe Ratio': [sharpe_ratio],
        'Sortino Ratio': [sortino_ratio],
        'VaR': [VaR],
        'RoR': [RoR],
        'MDD': [MDD],
        'Skewness': [skewness],
        'Kurtosis': [kurt],
        'Buying Trades': [no_buying_trades],
        'Selling Trades': [no_selling_trades]
    })
    describe = results['Daily_Return'].describe().T
    if f_star ==1:
        metrics['Kelly'] = 'No'
        describe['Kelly'] = 'No'
    else:
        metrics['Kelly'] = 'Yes'
        describe['Kelly'] = 'Yes'
    
    #print(metrics)
    #print(results['Daily_Return'].describe().T)
    return results, describe, metrics

def portfolio_buy_sell(group, start_date, end_date, f_star=1, signal='macd', rf=0):
    initial_investment = 100_000_000
    n = len(group)
    results = pd.DataFrame()
    no_buying_trades = 0
    no_selling_trades = 0

    for ticker in group:
        # Simulate investment for each ticker with equal allocation
        result, buy,sell= simulate_investment_buy_sell(
            ticker, sell_fraction=1,  start_date=start_date, end_date=end_date, investment=initial_investment / n, f_star=f_star, signal=signal
        )
        no_buying_trades += buy
        no_selling_trades += sell
        if not result.empty:
            results = pd.concat([results, result[f'value_{ticker}']], axis=1)

    # Calculate portfolio value as the sum of all stock values
    results['Portfolio_Value'] = results.sum(axis=1)
    results['Daily_Return'] = results['Portfolio_Value'].pct_change()
    results['Accumulated_Profit'] = results['Portfolio_Value'] - initial_investment

    # Calculate running max and drawdown
    results['Running_Max'] = results['Portfolio_Value'].cummax()
    results['Drawdown'] = (
        (results['Portfolio_Value'] - results['Running_Max']) 
        / results['Running_Max']
    )

    # Additional metrics
    sharpe_ratio = calculate_sharpe_ratio(results, rf)
    sortino_ratio = calculate_sortino_ratio(results, rf)
    VaR = calculate_var(results)
    RoR = results['Accumulated_Profit'].iloc[-1] / initial_investment*100
    MDD = results['Drawdown'].min()
    skewness = skew(results['Daily_Return'].dropna())
    kurt = kurtosis(results['Daily_Return'].dropna())

    # Create summary metrics table
    metrics = pd.DataFrame({
        'Sharpe Ratio': [sharpe_ratio],
        'Sortino Ratio': [sortino_ratio],
        'VaR': [VaR],
        'RoR': [RoR],
        'MDD': [MDD],
        'Skewness': [skewness],
        'Kurtosis': [kurt],
        'Buying Trades': [no_buying_trades],
        'Selling Trades': [no_selling_trades]
    })
    describe = results['Daily_Return'].describe().T
    if f_star ==1:
        metrics['Kelly'] = 'No'
        describe['Kelly'] = 'No'
    else:
        metrics['Kelly'] = 'Yes'
        describe['Kelly'] = 'Yes'
    
    #print(metrics)
    #print(results['Daily_Return'].describe().T)
    return results, describe, metrics