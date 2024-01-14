class Algorithm:
    def __init__(self):
        pass

    def runAlgorithmOnCandle(self):
        pass

    def runAlgorithmOnCandleContainer(self):
        pass

class MeanReversion(Algorithm):
    def __init__(self):
        return
    
    def runAlgorithmOnCandle(self):
        return
    
    def runAlgorithmOnCandleContainer(self, candle_container, short_ma, long_ma, stop_loss, take_profit):
        signals = []
        open_position = False
        purchase_price = None
        quantity = 0
        aum = 10000  # Assuming an initial amount of assets under management

        for i in range(len(candle_container)):
            current_candle = candle_container[i]
            current_price = current_candle.close

            # Check if enough data is available for MA calculations
            if i < max(short_ma.nCandles, long_ma.nCandles):
                signals.append(None)
                continue

            short_ma_value = short_ma.indicators[i]
            long_ma_value = long_ma.indicators[i]

            if not open_position:
                if short_ma_value > long_ma_value:
                    purchase_price = current_price
                    quantity = aum / purchase_price
                    total = purchase_price * quantity
                    aum -= total

                    data = {"type": "Buy", "price": purchase_price, "quantity": quantity, "total": total}
                    signals.append(data)
                    open_position = True

            else:
                sell = False
                if short_ma_value < long_ma_value:
                    sell = True
                elif (current_price <= purchase_price * (1 - stop_loss)) or (current_price >= purchase_price * (1 + take_profit)):
                    sell = True

                if sell:
                    sale_price = current_price
                    total = quantity * sale_price
                    aum += total
                    quantity = 0
                    profitable = sale_price > purchase_price

                    data = {"type": "Sell", "price": sale_price, "quantity": quantity, "total": total, "profitable": profitable}
                    signals.append(data)
                    open_position = False

            if not sell and open_position:
                signals.append({"type": "Hold"})

        return signals

class TrendFollowing(Algorithm):
    def __init__(self):
        super().__init__()
    
    def runAlgorithmOnCandleContainer(self, candle_container, short_ma, long_ma, stop_loss, take_profit):
        """
        candle_container: CandleContainer
        short_ma: Indicator
        long_ma: Indicator

        returns: list of all buy and sell signals

        This function will run the trend following algorithm on a candle container.
        The trend following algorithm does the following:
            - Assuming a position is not currently held, if the short moving average is
                above the long moving average and the long moving average has a positive
                derivative, then buy
            - Assuming a position is not currently held, if the short moving average is
                below the long moving average and the long moving average has a negative derivative
                then sell
            - If neither, hold
            - If already in a position, hold until stop loss or take profit is hit
        """
        signals = []
        position = None  # None, 'Buy', or 'Sell'
        entry_price = None

        for i in range(len(candle_container)):
            current_candle = candle_container[i]
            current_price = current_candle.close  # Assuming we're considering the close price for decision

            # Check if enough data is available for MA calculations
            if i < max(short_ma.nCandles, long_ma.nCandles):
                signals.append(None)
                continue

            short_ma_value = short_ma.indicators[i]
            long_ma_value = long_ma.indicators[i]

            # Buy/long Logic
            if short_ma_value > long_ma_value and (position is None or position == 'Sell'):
                if position == 'Sell':
                    # Close Sell position
                    signals.append('Close Sell')
                # Open Buy position
                signals.append('Buy')
                position = 'Buy'
                entry_price = current_price
            # Sell/short Logic
            elif short_ma_value < long_ma_value and (position is None or position == 'Buy'):
                if position == 'Buy':
                    # Close Buy position
                    signals.append('Close Buy')
                # Open Sell position
                signals.append('Sell')
                position = 'Sell'
                entry_price = current_price
            # Check for stop loss or take profit
            elif position is not None:
                if (position == 'Buy' and (current_price <= entry_price * (1 - stop_loss) or current_price >= entry_price * (1 + take_profit))) or \
                   (position == 'Sell' and (current_price >= entry_price * (1 + stop_loss) or current_price <= entry_price * (1 - take_profit))):
                    signals.append('Close ' + position)
                    position = None
                    entry_price = None
                else:
                    signals.append('Hold ' + position)

            else:
                signals.append(None)

        return signals

    def runAlgorithmOnCandle(self, candle, short_ma, long_ma):
        if short_ma > long_ma:
            return 'Buy'
        elif short_ma < long_ma:
            return 'Sell'
        else:
            return 'Hold'
