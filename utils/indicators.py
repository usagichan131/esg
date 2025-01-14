import ta
RSI_PERIOD = 14
RSI_OVERSOLD = 30
RSI_OVERBOUGHT = 70
#MACD
MACD_SLOW_PERIOD = 26
MACD_FAST_PERIOD = 12
MACD_SIGNAL_PERIOD = 9
#OBV:
OBV_PERIOD = 5

def calculate_indicators_macd(df):
    if df.empty:
        return df
    df['RSI'] = ta.momentum.RSIIndicator(df['close'], RSI_PERIOD).rsi()
    macd = ta.trend.MACD(df['close'], MACD_SLOW_PERIOD, MACD_FAST_PERIOD, MACD_SIGNAL_PERIOD)
    df['MACD'] = macd.macd()
    df['Signal_Line'] = macd.macd_signal()
    return df

def calculate_indicators_bb(df):
    if df.empty:
        return df
    df['RSI'] = ta.momentum.RSIIndicator(df['close'], RSI_PERIOD).rsi()
    df['Bollinger_high'] = ta.volatility.bollinger_hband(df['close'], window=15, window_dev=2)
    df['Bollinger_low'] = ta.volatility.bollinger_lband(df['close'], window=15, window_dev=2)
    df['Previous_RSI'] = df['RSI'].shift(1)
    df['Previous_RSI'].fillna(0, inplace=True)

    return df

def calculate_indicators_obv(df):
    if df.empty:
        return df
    
    df['RSI'] = ta.momentum.RSIIndicator(df['close'], RSI_PERIOD).rsi()
    df['OBV'] = ta.volume.OnBalanceVolumeIndicator(df['close'], df['volume']).on_balance_volume()
    df['OBV_Slope'] = df['OBV'].diff(periods=OBV_PERIOD)
    df['Previous_RSI'] = df['RSI'].shift(1)
    df['Previous_RSI'].fillna(0, inplace=True)

    return df