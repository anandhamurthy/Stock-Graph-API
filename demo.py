import pandas_datareader.data as web
import datetime as dt
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np


start_date = dt.datetime(2015, 1, 1)
end_date = dt.datetime.now()
df = web.DataReader("GOOG", 'yahoo', start_date, end_date)
df.reset_index(inplace=True)
df.set_index("Date", inplace=True)

close=df[['Close']]
future_days=25
close['Prediction']=close[['Close']].shift(-future_days)
X=np.array(close.drop(['Prediction'],1))[:-future_days]
y=np.array(close['Prediction'])[:-future_days]

from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test=train_test_split(X,y, test_size=0.25)

from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression

dtr=DecisionTreeRegressor()

dtr.fit(x_train, y_train)

x_future=close.drop(['Prediction'],1)[:-future_days]

x_future=x_future.tail(future_days)
x_future=np.array(x_future)

prediction_dtr=dtr.predict(x_future)
print(prediction_dtr)


