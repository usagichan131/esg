import pandas as pd

rf = {'2019': 0.0451, '2020': 0.0286, '2021': 0.023, '2022': 0.0335, '2023': 0.0321}
rf = pd.Series(rf)
rf_cal = rf.mean()
rf_2022 = 0.0335

RSI_PERIOD = 14
RSI_OVERSOLD = 30
RSI_OVERBOUGHT = 70
#MACD
MACD_SLOW_PERIOD = 26
MACD_FAST_PERIOD = 12
MACD_SIGNAL_PERIOD = 9
initial_investment = 100_000_000
#OBV:
OBV_PERIOD = 5
#BB:

# config.py

# Configuration for different trading strategies
STRATEGY_CONFIG = {
    "MACD": {
        "win_rate": 0.5711907018,
        "loss_rate": 1 - 0.5711907018,
        "mean_profit": 0.3493357553,
        "mean_loss": 0.1397008027,
        "stop_loss": None  # Stop loss not defined for MACD
    },
    "OBV": {
        "win_rate": 0.525862069,
        "loss_rate": 1 - 0.525862069,
        "mean_profit": 0.1539675969,
        "mean_loss": 0.2086126,
        "stop_loss": 0.08  # Specific stop loss for OBV
    },
    "BB": {
        "win_rate": 0.7070060208,
        "loss_rate": 1 - 0.7070060208,
        "mean_profit": 0.1721618831,
        "mean_loss": 0.1082770633,
        "stop_loss": 0.08  # Specific stop loss for BB
    }
}

def get_strategy_config(strategy_name):
    """
    Retrieve the configuration for the specified strategy.

    Args:
        strategy_name (str): Name of the strategy (e.g., "MACD", "OBV", "BB").

    Returns:
        dict: Configuration dictionary for the strategy.
    """
    return STRATEGY_CONFIG.get(strategy_name, None)



