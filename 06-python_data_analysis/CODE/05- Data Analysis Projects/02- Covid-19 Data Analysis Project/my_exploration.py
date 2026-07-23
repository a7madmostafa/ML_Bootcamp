
import plotly.express as px

def explore_uni_num(df, col):
    print(df[col].describe())
    fig1 = px.histogram(df, x=col)
    fig1.show()
    fig2 = px.box(df, y=col)
    fig2.show()

def explore_uni_cat(df, col):
    print(df[col].value_counts())
    fig = px.histogram(df, x=col)
    fig.show()
