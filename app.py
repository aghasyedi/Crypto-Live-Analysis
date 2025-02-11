from flask import Flask, render_template
import pandas as pd
from time import sleep
import threading
import cryptoApp as ca

app = Flask(__name__)

# Function to update Excel file with live data
def update_excel():
    while True:
        data = ca.fetch_crypto_data()
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
            print("Excel sheet updated successfully!")
        
        sleep(300)  # Update every 5 minutes

@app.route('/')
def index():
    try:
        # Read the data from the Excel file instead of fetching live data
        df = pd.read_excel("crypto_data.xlsx")
        analysis = ca.analyze_data(df)
        return render_template('index.html', data=df.to_dict('records'), analysis=analysis)
    except Exception as e:
        return f"Error reading Excel file: {str(e)}", 500

if __name__ == "__main__":
    # Start the Excel update thread
    thread = threading.Thread(target=update_excel)
    thread.daemon = True
    thread.start()
    
    # Run the Flask app
    app.run(debug=True)
