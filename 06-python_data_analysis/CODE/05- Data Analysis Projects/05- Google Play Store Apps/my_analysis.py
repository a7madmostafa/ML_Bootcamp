
import pandas as pd
import plotly.express as px

def univariate_numerical(df, col):
    print(df.describe())
    fig = px.histogram(df, x=col, title=col)
    fig.show()
    fig2 = px.box(df, x=col, title=col)
    fig2.show()

def univariate_categorical(df, col):
    print(df[col].value_counts())
    print(df[col].nunique())
    fig = px.bar(df[col].value_counts(), title=col)
    fig.show()   
