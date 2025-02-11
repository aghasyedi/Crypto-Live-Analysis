import requests
import pandas as pd
from time import sleep

# Function to fetch cryptocurrency data
def fetch_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 50,
        "page": 1,
        "sparkline": "false"
    }
    response = requests.get(url, params=params)
    print(response)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching data:", response.status_code)
        return []

# Function to perform basic data analysis
# Function to perform basic data analysis
def analyze_data(df):
    top_5 = df.nlargest(5, "Market Capitalization")
    avg_price = df["Current Price (USD)"].mean()
    highest_change = df.loc[df["24h Price Change (%)"].idxmax()]
    lowest_change = df.loc[df["24h Price Change (%)"].idxmin()]
    
    analysis = {
        "top_5": top_5[["Cryptocurrency Name", "Market Capitalization"]].to_dict('records'),
        "avg_price": round(avg_price, 2),
        "highest_change": {
            "name": highest_change["Cryptocurrency Name"],
            "change": highest_change["24h Price Change (%)"]
        },
        "lowest_change": {
            "name": lowest_change["Cryptocurrency Name"],
            "change": lowest_change["24h Price Change (%)"]
        }
    }
    return analysis
# Function to update Excel file with live data
def update_excel():
    while True:
        data = fetch_crypto_data()
        if data:
            df = pd.DataFrame(data, columns=[
                "name", "symbol", "current_price", "market_cap", 
                "total_volume", "price_change_percentage_24h"
            ])
            df.rename(columns={
                "name": "Cryptocurrency Name",
                "symbol": "Symbol",
                "current_price": "Current Price (USD)",
                "market_cap": "Market Capitalization",
                "total_volume": "24h Trading Volume",
                "price_change_percentage_24h": "24h Price Change (%)"
            }, inplace=True)
            
            df.to_excel("crypto_data.xlsx", index=False)
            analyze_data(df)
            print("Excel sheet updated successfully!")
        
        sleep(300)  # Update every 5 minutes

# if __name__ == "__main__":
#     update_excel()