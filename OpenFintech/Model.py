class MeanReversion:
    def __init__(self):
        return
    
    def runAlgorithmOnCandle(self):
        return
    
    def runAlgorithmOnCandleContainer(self):
        return

class Algorithm:
    def __init__(self):
        pass

    def runAlgorithmOnCandle(self):
        pass

    def runAlgorithmOnCandleContainer(self):
        pass

class TrendFollowing(Algorithm):
    def __init__(self):
        super().__init__()
    
    def runAlgorithmOnCandleContainer(self, df, short_ma, long_ma):
        df['short_ma'] = df['Close'].rolling(window=short_ma).mean()
        df['short_ma'] = df['Close'].rolling(window=short_ma).mean()
        df['Signal'] = np.where(df['short_ma'] > df['long_ma'], 1, -1)
        
        return df

    def runAlgorithmOnCandle(self, candle, short_ma, long_ma):
        if short_ma > long_ma:
            return 'Buy'
        elif short_ma < long_ma:
            return 'Sell'
        else:
            return 'Hold'
