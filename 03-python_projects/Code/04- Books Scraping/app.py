import streamlit as st
from scrape import scrape_books, get_categories

st.title('Books Scraping App')

categories = get_categories().keys()
selected_category = st.selectbox('Select a category:', categories)

if selected_category:
    books_df = scrape_books(selected_category)
    # Better display the DataFrame
    st.markdown(f"### Books in category: {selected_category}")
    st.markdown(books_df.to_markdown(index=False))
    
