RSI_PERIOD = 14
RSI_OVERSOLD = 30
RSI_OVERBOUGHT = 70
def macd_strategy(df):
    if df.empty:
        return df
    df['Signal'] = 0
    df.loc[(df['MACD'] > df['Signal_Line']) & (df['RSI'] > RSI_OVERSOLD), 'Signal'] = 1
    df.loc[(df['MACD'] < df['Signal_Line']) & (df['RSI'] < RSI_OVERBOUGHT), 'Signal'] = -1
    return df

def bb_strategy(df):
    if df.empty:
        return df
    
    df['Signal'] = 0

    # Buy signals: RSI cross above 30 and MACD cross above Signal line
    df.loc[
        (df['close'] <= df['Bollinger_low']) &
        (df['RSI'] <= RSI_OVERSOLD), 'Signal'] = 1

    # Sell Signals: 
    df.loc[
        (df['RSI'] >= RSI_OVERBOUGHT) &
        (df['close'] >= df['Bollinger_high']), 'Signal'] = -1

    return df

def obv_strategy(df):
    if df.empty:
        return df
    
    df['Signal'] = 0

    # Buy signals: RSI across 30 and OBV rise
    df.loc[(df['Previous_RSI'] < RSI_OVERSOLD) & (df['RSI'] >= RSI_OVERSOLD) & (df['OBV_Slope'] > 0), 'Signal'] = 1

    #Sell Signals: RSI across 70 and OBV down 
    df.loc[(df['Previous_RSI'] > RSI_OVERBOUGHT) & (df['RSI'] <= RSI_OVERBOUGHT) & (df['OBV_Slope'] < 0), 'Signal'] = -1

    return df