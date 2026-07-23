
import pandas as pd
import plotly.express as px
import streamlit as st

def load_data():
    df = pd.read_csv('googleplaystore.csv')
    return df

def clean_data(df):
    df.drop_duplicates(subset='App', inplace=True)
    df.dropna(inplace=True)
    df['Price'] = df['Price'].apply(lambda x: x.replace('$', '') if '$' in str(x) else x).astype(float)
    df.Reviews = df.Reviews.astype(int)
    return df

df = load_data()
df = clean_data(df)

# Title
st.title('Google Play Store')

# Subtitle
st.subheader('Data Analysis')

# Top10 Category
top10_category = df.groupby(['Category']).agg({'App': 'count'}).nlargest(10, 'App')
fig1 =px.bar(top10_category, x=top10_category.index, y='App', title='Top 10 Category')

# Free vs Paid
free_vs_paid = df.groupby(['Type']).agg({'App': 'count'})
fig2 = px.pie(free_vs_paid, values='App', names=free_vs_paid.index, title='Free vs Paid')

# Top10 Genres
top10_genres = df.groupby(['Genres']).agg({'App': 'count'}).nlargest(10, 'App')
fig3 = px.bar(top10_genres, x=top10_genres.index, y='App', title='Top 10 Genres')

# Top10 Content Rating
top10_content_rating = df.groupby(['Content Rating']).agg({'App': 'count'}).nlargest(10, 'App')
fig4 = px.bar(top10_content_rating, x=top10_content_rating.index, y='App', title='Top 10 Content Rating')

# Top10 Installs
top10_installs = df.groupby(['Installs']).agg({'App': 'count'}).nlargest(10, 'App')
fig5 = px.bar(top10_installs, x=top10_installs.index, y='App', title='Top 10 Installs')

# Android Version
android_version = df.groupby(['Android Ver']).agg({'App': 'count'}).nlargest(10, 'App')
fig6 = px.bar(android_version, x=android_version.index, y='App', title='Android Version')

# Price vs Category
df_price = df[(df['Price']> 0) & (df['Price']< 100)]
fig7 = px.scatter(df_price, x='Price', y='Category', color='Type', title='Price vs Category')

fig8 = px.bar(df.nlargest(10, 'Reviews'), x='App', y='Reviews', title='Top 10 apps with most reviews', width=800, height=500)

# Layout
st.sidebar.title('Menu')
st.sidebar.subheader('Select a graph')
select_graph = st.sidebar.selectbox('Graph', ['Top 10 Category', 'Free vs Paid', 'Top 10 Genres', 'Top 10 Content Rating', 'Top 10 Installs', 'Android Version', ' Price vs Category', 'Show All'])

if select_graph == 'Top 10 Category':
    st.plotly_chart(fig1)
elif select_graph == 'Free vs Paid':
    st.plotly_chart(fig2)
elif select_graph == 'Top 10 Genres':
    st.plotly_chart(fig3)
elif select_graph == 'Top 10 Content Rating':
    st.plotly_chart(fig4)
elif select_graph == 'Top 10 Installs':
    st.plotly_chart(fig5)
elif select_graph == 'Android Version':
    st.plotly_chart(fig6)
elif select_graph == 'Price vs Category':
    st.plotly_chart(fig7)
elif select_graph == 'Show All':
    st.plotly_chart(fig1)
    st.plotly_chart(fig2)
    st.plotly_chart(fig3)
    st.plotly_chart(fig4)
    st.plotly_chart(fig5)
    st.plotly_chart(fig6)
    st.plotly_chart(fig7)
    st.plotly_chart(fig8)
  