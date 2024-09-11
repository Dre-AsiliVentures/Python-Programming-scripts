from binance import Client
import datetime
import logging
import pandas as pd
import requests
import ta_py as ta
import time
def secrets():
    api_key = 'qra0tNWRSXXfHXVg8luYdVlmy1YbMKsNcGFzO9byJMgLddR1pmtgoB26k4vlPxgJ'
    api_secret = 'RTSJem2giaLfu5CV5ZCCX1xgk4OCQHdsCVJmka70MK14hGTNbHJq01R8iUdrTYFd'
    return api_key,api_secret
key,secret=secrets() #hostname -I
client = Client(key, secret)
tradingInterval=15*60
interval=Client.KLINE_INTERVAL_1MINUTE
support_interval=Client.KLINE_INTERVAL_30MINUTE
class binance_execution():
    def __init__(self,token):
        self.currentDatetime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.token=token
        self.symbol=f"{token}USDT"
        self.lastprice=round(float((self.datafetch(interval)['Close'].iloc[-1])),8)
        buy_bal = round(float(client.get_asset_balance('USDT')['free'])*0.97,3)
        self.buy_bal = int(buy_bal)
        #self.buy_bal = 13
        self.buy_quantity=int(self.buy_bal/self.lastprice) #e.g.,5/0.2547
        # sell_bal = int(float(client.get_asset_balance('ADA')['free']))
        # sell_quantity=int(round(float(sell_bal*0.99),2)) #e.g.,5*0.2547
        sell_bal = round(float(client.get_asset_balance(str(token))['free']),2)
        #sell_bal = round(float(client.get_asset_balance('ADA')['free']),2)
        with open('buy_quantity.txt', 'r') as file:
            # Read all lines into a list
            lines = file.readlines()
        # Check if there are any lines in the file
        if lines:
            # Extract and print the last line
            self.sell_quantity=float(lines[-1].strip())
        else:
            self.sell_quantity=5000000
        self.sell_quantity = int(sell_bal *0.99)
    def datafetch(self,interval):
        data=client.get_historical_klines(self.symbol,interval, "30 day ago")  #https://python-binance.readthedocs.io/en/latest/market_data.html?highlight=kline%20limit#id6
        data_table=pd.DataFrame(data)
        data_table=data_table.iloc[:,:6] # All rows and column upto 6
        # Naming the columns
        data_table.columns=['Time','Open','High','Low','Close','Volume']
        # Name the rows
        data_table=data_table.set_index('Time') # Note this is in ms
        # Convert this Time to readable form since this is time from 1970s
        data_table.index=pd.to_datetime(data_table.index,unit='ms')
        data_table=data_table.astype(float) # Convert values from strings to float
        #data_table=data_table[['Open','High','Low','Close','Volume']]
        return data_table
    def place_buy_order(self):
        if self.buy_bal <1.5:
            message=f'{self.currentDatetime} Buy Order skipped. Balance'
            try:
                self.send_telegram_Message(message)
            except:
                time.sleep(10)
                self.send_telegram_Message(message)
        else:
            try:
                order = client.create_order(symbol=self.symbol,side=Client.SIDE_BUY,type=Client.ORDER_TYPE_MARKET,quantity=self.buy_quantity)
                print(f"{self.currentDatetime} {self.symbol} Buy order placed")
                #selling_price=(float(order['fills'][0]['commission'])*float(order['fills'][0]['price']))+float(order['fills'][0]['price'])
                average_filled_price = float(order['fills'][0]['price'])  # Average filled price
                commission_in_usdt = float(order['fills'][0]['commission'])  # Commission in USDT
                filled_quantity = float(order['fills'][0]['qty'])  # Filled quantity
                # Calculate the selling price threshold
                total_cost = average_filled_price * filled_quantity
                total_cost_after_commission = total_cost + commission_in_usdt
                # Define the desired profit target
                desired_profit = 0.21 # Example 1 USDT Profit
                # Calculate the selling price threshold to achieve the desired profit
                with open('buy_quantity.txt', 'a') as file:
                    # Append content to the file
                    file.write(f"\n{filled_quantity}")
                    file.close()
                selling_price = (total_cost_after_commission + desired_profit) / filled_quantity
                with open('buy_trades.txt', 'a') as file:
                    # Append content to the file
                    file.write(f"\n{selling_price}")
                    file.close()
                message=f'{self.symbol} Buy Order executed. Order on {self.currentDatetime}'
                #message=f'{self.symbol} Buy Order executed. Order:{order} on {self.currentDatetime}'
                try:
                    self.send_telegram_Message(message)
                except:
                    time.sleep(10)
                    self.send_telegram_Message(message)
                with open('bot_trades.txt', 'a') as file:
                    # Append content to the file
                    
                    file.write(f"\nSuccessful Buy at {self.currentDatetime}. {self.symbol} Buy order:{order['fills']}")
                    file.close()
            except Exception as e:
                with open('error.txt', 'a') as file:
                    # Append content to the file
                    file.write(f"\n{self.symbol} Buy Error on {self.currentDatetime} {e}")
                    file.close()
                message=f'{self.symbol} Buy Order execution Error!! {e}'
                try:
                    if e.code == -1013:
                        pass
                except:
                    time.sleep(10)
                    self.send_telegram_Message(message)
    def place_sell_order(self):
        try:
            order = client.create_order(
            symbol=self.symbol,
            side=Client.SIDE_SELL,
            type=Client.ORDER_TYPE_MARKET,
            quantity=self.sell_quantity)
            #recvWindow=recv_window
            print(f"{self.currentDatetime} {self.symbol} Sell order placed")
            
            message=f'{self.symbol} Sell Order executed on {self.currentDatetime}'
            #message=f'{self.symbol} Sell Order executed {order} on {self.currentDatetime}'
            try:
                self.send_telegram_Message(message)
            except:
                time.sleep(10)
                self.send_telegram_Message(message)
            with open('bot_trades.txt', 'a') as file:
                # Append content to the file
                
                file.write(f"\n{self.symbol} Successful Sell at {self.currentDatetime}. Sell order:{order['fills']}")
            file.close()
        except Exception as e:
            with open('error.txt', 'a') as file:
                # Append content to the file
                file.write(f"\n{self.symbol} Sell Error on {self.currentDatetime} {e}")
                file.close()
            message=f'{self.symbol} Sell Order execution Error!! {e}'
            try:
                if e.code == -1013:
                    pass
                    #self.send_telegram_Message(message)
            except:
                time.sleep(10)
                self.send_telegram_Message(message)
    def send_telegram_Message(self,text):
        bot_token='6612911011:AAFKiJOPtItAR9CHLPTae9Rw0SgM-G_Avp0'
        chat_id='5082702188'
        url = f'https://api.telegram.org/bot{bot_token}/sendMessage' # URL to the Telegram Bot API for sending photos
        # Message to send
        # Parameters for the POST request
        params = {
            'chat_id': chat_id,
            'text': text}
        # Send the message
        response = requests.post(url, params=params)
    def support_resistance(self,data):
        # If lookback is None, use the default value of 15
        dataframeLength=len(data)
        #lookbackPeriod=(lookback/100)*dataframeLength
        lookbackPeriod=dataframeLength
        # Calculate support and resistance levels using ta-py module
        recent_low = ta.recent_low(data['Low'], lookbackPeriod)
        recent_high = ta.recent_high(data['High'],lookbackPeriod)

        support = ta.support(data['Low'], recent_low)
        resistance = ta.resistance(data['High'], recent_high)

        #return support['lowest'], resistance['highest']
        return support['calculate'](len(data)-support['index']), resistance['calculate'](len(data)-resistance['index'])
class rev_condition():
    def __init__(self,data):
        #self.rsi_7=ta.rsi,self.data.Close,length=7
        self.data=data
        self.ema_4=ta.ema(self.data.Close.values,3)
        #self.ema_4=self.I(ta.ema,self.data.Close,4)
    def entry(self):
        return (
            self.data.High[-1]<self.ema_4[-1] and self.data.Close[-1]<self.ema_4[-1]
        )
    def exit(self):
        return (
            self.data.Low[-1]>self.ema_4[-1] and self.data.Open[-1]>self.ema_4[-1] # L and O used instead H and C
        )
def buy_sell_check(coin):
        binance_Client=binance_execution(coin)
        with open('buy_trades.txt', 'r') as file:
            # Read all lines into a list
            lines = file.readlines()
        # Check if there are any lines in the file
        if lines:
            # Extract and print the last line
            selling_price=float(lines[-1].strip())
        else:
            selling_price=5000000
        try:
            current_data=binance_Client.datafetch(interval)
            reversion_condition=rev_condition(current_data)
            time.sleep(3)
            support_data=binance_Client.datafetch(support_interval)
            support_level,resistance_level=binance_Client.support_resistance(support_data)
            if reversion_condition.entry()==True and binance_Client.lastprice>support_level and binance_Client.lastprice<0.95*resistance_level:
                """Entry conditions.

                Conditions:
                1. Mean Revert Entry -- High lower than EMA, Close lower than EMA.
                2. Last price above Support level.
                3. Last price lower than 95% Resistance level -BL.
                """
                binance_Client.place_buy_order()
            #elif reversion_condition.exit()==True and binance_Client.lastprice>selling_price:
            elif binance_Client.lastprice>selling_price:
                binance_Client.place_sell_order()
        except Exception as e:
            message=f"{binance_Client.currentDatetime} Urgent inbox\n{e}\nLogin to your Bot soon\nAutomated Message by Code with Asili"
            binance_Client.send_telegram_Message(text=message)
            time.sleep(20)
if __name__=='__main__':
    while True:
        import warnings
        #To filter out all FutureWarnings (not recommended)
        warnings.simplefilter(action='ignore', category=FutureWarning)
        try:
            portfolio=['ADA','PHB','MANA']
            for coin in portfolio:
                buy_sell_check(coin)
                time.sleep(50)
        except:
            time.sleep(50)
            buy_sell_check(coin)
        time.sleep(30)
