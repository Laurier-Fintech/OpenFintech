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
    
    def runAlgorithmOnCandleContainer(self, candle_container, short_ma, long_ma, stop_loss, take_profit, assets):
        signals = []
        open_position = False
        position_type = None  # 'Buy' or 'Sell'
        purchase_price = None
        quantity = 0
        aum = assets

        for i in range(len(candle_container)):
            current_candle = candle_container[i]
            current_price = current_candle.close

            # Check if enough data is available for MA calculations
            if i < max(short_ma.periodLength, long_ma.periodLength):
                signals.append({"date":current_candle.datetime,"type":None})
                continue

            short_ma_value = short_ma.calculatedValues[i]
            long_ma_value = long_ma.calculatedValues[i]
            sell = False  # Declare sell here

            if not open_position:
                if short_ma_value > long_ma_value:
                    purchase_price = current_price
                    quantity = aum / purchase_price
                    total = purchase_price * quantity
                    aum -= total

                    data = {"date":current_candle.datetime,"type": "Buy", "price": purchase_price, "quantity": quantity, "total": total}
                    signals.append(data)
                    open_position = True
                    position_type = "Buy"
            else:
                stop_loss_point = purchase_price * (1 - stop_loss)
                take_profit_point = purchase_price * (1 + take_profit)
                if short_ma_value < long_ma_value or (current_price <= stop_loss_point) or (current_price >= take_profit_point):
                    sell = True
                    sale_price = current_price
                    total = quantity * sale_price
                    aum += total

                    data = {"date":current_candle.datetime,"type": "Close " + position_type, "price": sale_price, "quantity": quantity, "total": total}
                    signals.append(data)
                    open_position = False
                    position_type = None
                    quantity = 0

            if not sell and open_position:
                signals.append({"date":current_candle.datetime,"type": "Hold " + position_type})

        return signals, aum

class TrendFollowing(Algorithm):
    def __init__(self):
        super().__init__()
    
    def runAlgorithmOnCandle(self, candle, short_ma, long_ma):
        return

    def runAlgorithmOnCandleContainer(self, candle_container, short_ma, long_ma, stop_loss, take_profit, assets):
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
        quantity = 0
        aum = assets

        for i in range(len(candle_container)):
            current_candle = candle_container[i]
            current_price = current_candle.close

            # Check if enough data is available for MA calculations
            if i < max(short_ma.periodLength, long_ma.periodLength):
                signals.append({"date":current_candle.datetime,"type":None})
                continue

            short_ma_value = short_ma.calculatedValues[i]
            long_ma_value = long_ma.calculatedValues[i]
            long_ma_prev_value = long_ma.calculatedValues[i - 1]
            long_ma_derivative = long_ma_value - long_ma_prev_value

            # Buy Logic
            if short_ma_value > long_ma_value and long_ma_derivative > 0 and (position is None or position == 'Sell'):
                if position == 'Sell':
                    # Close Sell position
                    sale_price = current_price
                    total = quantity * sale_price
                    aum += total
                    signals.append({"date":current_candle.datetime,"type": "Close Sell", "price": sale_price, "quantity": quantity, "total": total})
                    quantity = 0

                # Open Buy position
                entry_price = current_price
                quantity = aum / entry_price
                total = entry_price * quantity
                aum -= total
                signals.append({"date":current_candle.datetime,"type": "Buy", "price": entry_price, "quantity": quantity, "total": total})
                position = 'Buy'

            # Sell Logic
            elif short_ma_value < long_ma_value and long_ma_derivative < 0 and (position is None or position == 'Buy'):
                if position == 'Buy':
                    # Close Buy position
                    sale_price = current_price
                    total = quantity * sale_price
                    aum += total
                    signals.append({"date":current_candle.datetime,"type": "Close Buy", "price": sale_price, "quantity": quantity, "total": total})
                    quantity = 0

                # Open Sell position
                entry_price = current_price
                quantity = aum / entry_price  # Assuming short selling is allowed
                total = entry_price * quantity
                aum -= total  # Assuming margin trading or short selling
                signals.append({"date":current_candle.datetime,"type": "Sell", "price": entry_price, "quantity": quantity, "total": total})
                position = 'Sell'

            # Check for stop loss or take profit
            elif position is not None:
                if (position == 'Buy' and (current_price <= entry_price * (1 - stop_loss) or current_price >= entry_price * (1 + take_profit))) or \
                   (position == 'Sell' and (current_price >= entry_price * (1 + stop_loss) or current_price <= entry_price * (1 - take_profit))):
                    # Close position
                    sale_price = current_price
                    total = quantity * sale_price
                    aum += total
                    signals.append({"date":current_candle.datetime,"type": "Close " + position, "price": sale_price, "quantity": quantity, "total": total})
                    position = None
                    entry_price = None
                    quantity = 0
                else:
                    signals.append({"date":current_candle.datetime,"type": "Hold " + position})

            else:
                signals.append({"date":current_candle.datetime,"type":None})

        return signals, aum
