from fbprophet import Prophet
from fbprophet.plot import plot_plotly, plot_components_plotly
import pandas_datareader.data as web

def stock_predict(symbol, start, end, period=60):
    #grabing and formating the data
    df=web.DataReader(symbol,'yahoo', start,end)
    df.reset_index(inplace=True)
    df = df[['Date', 'Close']]
    df = df.rename(columns = {"Date":"ds","Close":"y"}) 

    #setting up and training the model
    fbp = Prophet(daily_seasonality = True) 
    fbp.fit(df)
    fut = fbp.make_future_dataframe(periods=period) 
    forecast = fbp.predict(fut)

    return plot_plotly(fbp,forecast) #a plot to inject directly into our layout

