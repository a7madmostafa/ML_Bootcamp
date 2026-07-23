# world_happiness_2021_app.py
# Streamlit dashboard for World Happiness Report 2021 (concise requirements)
# Run: streamlit run world_happiness_2021_app.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# -------------------------
# Helpers
# -------------------------
@st.cache_data
def load_data():
    df = pd.read_csv('world-happiness-report-2021.csv')

    # Drop columns if present (from your cleaning notes)
    drop_cols = [
        'Standard error of ladder score', 'upperwhisker', 'lowerwhisker',
        'Ladder score in Dystopia', 'Explained by: Log GDP per capita',
        'Explained by: Social support', 'Explained by: Healthy life expectancy',
        'Explained by: Freedom to make life choices', 'Explained by: Generosity',
        'Explained by: Perceptions of corruption', 'Dystopia + residual'
    ]
    df = df.drop(columns=[c for c in drop_cols if c in df.columns], errors='ignore')

    # Rename to canonical columns (if original column names exist)
    rename_map = {
        "Country name": "Country",
        "Regional indicator": "Region",
        "Ladder score": "Happiness",
        "Logged GDP per capita": "GDP",
        "Healthy life expectancy": "Life_Expectancy",
        "Freedom to make life choices": "Freedom",
        "Perceptions of corruption": "Corruption"
    }
    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

    # Keep relevant columns if present
    keep = ['Country', 'Region', 'Happiness', 'GDP', 'Social support',
            'Life_Expectancy', 'Freedom', 'Generosity', 'Corruption']
    present = [c for c in keep if c in df.columns]
    df = df[present].copy()

    # Clean numeric columns
    for c in ['Happiness', 'GDP', 'Social support', 'Life_Expectancy', 'Freedom', 'Generosity', 'Corruption']:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors='coerce')

    # Create Income Group by GDP tertiles (High / Middle / Low) for analysis
    if 'GDP' in df.columns:
        df['Income_Group'] = pd.qcut(df['GDP'].rank(method='first'), q=3, labels=['Low', 'Middle', 'High'])
    else:
        df['Income_Group'] = 'Unknown'

    # Drop rows with no country name
    df = df.dropna(subset=['Country']).reset_index(drop=True)
    return df

def corr_matrix(df: pd.DataFrame):
    numeric = df.select_dtypes(include=[np.number])
    return numeric.corr()

# -------------------------
# App
# -------------------------
def main():
    st.set_page_config(page_title="World Happiness 2021", layout="wide")
    st.title("World Happiness Report — 2021 (Concise Dashboard)")
    
    df = load_data()
    
    # Basic info
    st.sidebar.markdown(f"**Countries:** {df['Country'].nunique()}  ")
    if 'Region' in df.columns:
        st.sidebar.markdown(f"**Regions:** {df['Region'].nunique()}  ")

    # Region filter
    regions = ['All']
    if 'Region' in df.columns:
        regions += sorted(df['Region'].dropna().unique().tolist())
    region = st.sidebar.selectbox("Filter by Region", regions, index=0)

    # Country comparison selection (2-3)
    country_choices = sorted(df['Country'].unique())
    compare = st.sidebar.multiselect("Compare countries (2–3)", options=country_choices, default=country_choices[:2])
    if len(compare) > 3:
        compare = compare[:3]

    # Metric for ranking/map
    default_metric = 'Happiness' if 'Happiness' in df.columns else df.select_dtypes(include=[np.number]).columns[0]
    metric = st.sidebar.selectbox("Metric for ranking / map", options=[c for c in ['Happiness','GDP','Social support','Life_Expectancy','Freedom','Generosity','Corruption'] if c in df.columns], index=0)

    # Apply region filter
    if region != 'All' and 'Region' in df.columns:
        dff = df[df['Region'] == region].copy()
    else:
        dff = df.copy()

    # Layout: three columns on top
    c1, c2, c3 = st.columns([1, 1, 1])

    # Overview: average happiness
    with c1:
        st.metric("Average Happiness (global)", value=round(dff['Happiness'].mean(), 3) if 'Happiness' in dff.columns else "N/A")
        st.write("Top 10 (by Happiness)")
        if 'Happiness' in dff.columns:
            top10 = dff.sort_values('Happiness', ascending=False).head(10)
            st.dataframe(top10[['Country','Region','Happiness']].reset_index(drop=True))
        else:
            st.write("Happiness column not available.")

    # Top/Bottom quick small charts
    with c2:
        st.write("Top 10 — Horizontal bar")
        if metric in dff.columns:
            top = dff.sort_values(metric, ascending=False).head(10)
            fig = px.bar(top[::-1], x=metric, y='Country', orientation='h', height=320)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("Metric not available.")

    with c3:
        st.write("Bottom 10")
        if metric in dff.columns:
            bottom = dff.sort_values(metric, ascending=True).head(10)
            figb = px.bar(bottom, x=metric, y='Country', orientation='h', height=320)
            st.plotly_chart(figb, use_container_width=True)
        else:
            st.write("Metric not available.")

    st.markdown("---")

    # Key Drivers: scatter matrix, correlation, and single scatter with regression
    st.header("Key Drivers")
    driver_cols = [c for c in ['GDP','Social support','Life_Expectancy','Freedom','Generosity','Corruption'] if c in dff.columns]
    if 'Happiness' in dff.columns and driver_cols:
        colA, colB = st.columns([2,1])
        with colA:
            st.subheader("Happiness vs Key Factors (scatter)")
            factor = st.selectbox("Choose factor", options=driver_cols, index=0)
            fig = px.scatter(dff, x=factor, y='Happiness', hover_name='Country', trendline='ols', height=420)
            st.plotly_chart(fig, use_container_width=True)
        with colB:
            st.subheader("Correlation with Happiness")
            corr = corr_matrix(dff)
            if 'Happiness' in corr.columns:
                corrs = corr['Happiness'].drop('Happiness').sort_values(ascending=False)
                st.table(corrs.round(3).to_frame("Correlation"))
            else:
                st.write("Not enough numeric columns.")
    else:
        st.write("Not enough columns to show key drivers (need 'Happiness' and at least one factor).")

    st.markdown("---")

    # Regional Insights
    st.header("Regional Insights")
    if 'Region' in dff.columns:
        reg_avg = dff.groupby('Region')[['Happiness'] + [c for c in driver_cols if c in dff.columns]].mean().round(3).reset_index()
        st.subheader("Average by Region")
        fig_reg = px.bar(reg_avg.sort_values('Happiness', ascending=False), x='Happiness', y='Region', orientation='h', height=420)
        st.plotly_chart(fig_reg, use_container_width=True)

        st.subheader("Region table (select to view)")
        st.dataframe(reg_avg)
    else:
        st.write("No Region column available.")

    st.markdown("---")

    # Income Group analysis
    st.header("Income Group Comparison")
    if 'Income_Group' in dff.columns:
        ig = dff.groupby('Income_Group')[['Happiness'] + [c for c in driver_cols if c in dff.columns]].mean().round(3).reset_index()
        st.dataframe(ig)
        # plot happiness by income group
        fig_ig = px.bar(ig, x='Income_Group', y='Happiness', title='Average Happiness by Income Group', height=360)
        st.plotly_chart(fig_ig, use_container_width=True)
    else:
        st.write("Income grouping not available.")

    st.markdown("---")

    # Country Comparison
    st.header("Country Comparison")
    if compare and all([c in dff['Country'].values for c in compare]):
        comp_df = dff.set_index('Country').loc[compare, ['Happiness'] + [c for c in driver_cols if c in dff.columns]]
        st.subheader("Numeric comparison")
        st.dataframe(comp_df.round(3))

        st.subheader("Visual comparison")
        comp_long = comp_df.reset_index().melt(id_vars='Country', var_name='Metric', value_name='Value')
        fig_cmp = px.bar(comp_long, x='Metric', y='Value', color='Country', barmode='group', height=420)
        st.plotly_chart(fig_cmp, use_container_width=True)

        # Over/under performance vs GDP (simple residual from GDP->Happiness linear fit)
        if 'GDP' in dff.columns and 'Happiness' in dff.columns:
            import statsmodels.api as sm
            tmp = dff.dropna(subset=['GDP','Happiness'])
            X = sm.add_constant(tmp['GDP'])
            model = sm.OLS(tmp['Happiness'], X).fit()
            preds = model.predict(sm.add_constant(dff['GDP']))
            dff['_resid_vs_gdp'] = dff['Happiness'] - preds
            resid = dff.set_index('Country').loc[compare, '_resid_vs_gdp']
            st.subheader("Over/Under performance vs GDP (residual)")
            st.table(resid.round(3).to_frame("Resid_Happiness_minus_pred"))
    else:
        st.info("Select 2–3 countries in the sidebar to compare.")

    st.markdown("---")

    # Correlation heatmap (compact)
    st.header("Correlation Heatmap")
    corr = corr_matrix(dff)
    if not corr.empty:
        fig_corr = px.imshow(corr, text_auto=True, aspect="auto", height=520)
        st.plotly_chart(fig_corr, use_container_width=True)
    else:
        st.write("Not enough numeric data to compute correlations.")

    st.markdown("---")

    # Conclusions box
    st.header("Conclusions & Insights")
    st.markdown(
        """
        - **Strong drivers:** GDP, Social support, and Life Expectancy tend to have the highest correlations with Happiness.
        - **Secondary drivers:** Freedom usually contributes positively.
        - **Other factors:** Generosity and Corruption show weaker / variable relationships and require contextual interpretation.
        - **Policy lead:** Improving health and social support (networks/services) alongside economic stability is likely to yield gains in national happiness.
        """
    )

    st.sidebar.markdown("**Notes**")
    st.sidebar.write("- Dataset source: World Happiness Report 2021 (Kaggle).")
    st.sidebar.write("- Income groups created from GDP tertiles for this exercise.")
    st.sidebar.write("- For advanced work: try clustering countries or building a simple regression model.")

if __name__ == "__main__":
    main()
