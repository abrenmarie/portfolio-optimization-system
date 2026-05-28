import pandas as pd
import requests
import apimoex
from datetime import datetime

def load_historical_data(tickers: list, start_date: str, end_date: str) -> pd.DataFrame:
    session = requests.Session()
    combined_data = {}

    for ticker in tickers:
        data = apimoex.get_market_candles(
            session, 
            security=ticker, 
            start=start_date, 
            end=end_date, 
            interval=24, 
            market='shares', 
            engine='stock'
        )
        
        if not data:
            print(f"Warning: No data available for this ticker {ticker}")
            continue
            
        df = pd.DataFrame(data)
        df['begin'] = pd.to_datetime(df['begin']).dt.date
        df.set_index('begin', inplace=True)
        
        combined_data[ticker] = df['close']

    final_df = pd.DataFrame(combined_data)
    
    returns = final_df.pct_change().dropna()
    return returns