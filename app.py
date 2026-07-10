import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(
    page_title="Insurance Analytics Dashboard",
    page_icon="🌸",
    layout="wide"
)

# 2. Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("insurance.csv")
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("Could not find 'insurance.csv'. Please make sure it's in the same folder as this script.")
    st.stop()

# 3. Title & Header
st.title("💖 Medical Insurance Insights Dashboard")
st.markdown("Explore how demographic and lifestyle factors influence insurance costs—*completely wrapped in pastel pink!*")
st.divider()

# 4. Sidebar Filters
st.sidebar.header("🌸 Filter & Customize")

smoker_filter = st.sidebar.multiselect(
    "Select Smoker Status:",
    options=df["smoker"].unique(),
    default=df["smoker"].unique()
)

region_filter = st.sidebar.multiselect(
    "Select Region:",
    options=df["region"].unique(),
    default=df["region"].unique()
)

filtered_df = df[
    (df["smoker"].isin(smoker_filter)) & 
    (df["region"].isin(region_filter))
]

# 5. Key Metrics Rows
metric1, metric2, metric3, metric4 = st.columns(4)

with metric1:
    st.metric(label="Total Records", value=len(filtered_df))
with metric2:
    st.metric(label="Avg Insurance Charge", value=f"${filtered_df['charges'].mean():,.2f}")
with metric3:
    st.metric(label="Avg BMI", value=f"{filtered_df['bmi'].mean():.1f}")
with metric4:
    st.metric(label="Avg Age", value=f"{filtered_df['age'].mean():.1f} years")

st.divider()

# Custom Pink & Magenta color scheme for Plotly charts (matches the theme background)
PINK_PALETTE = ["#FF69B4", "#C71585", "#FF1493", "#DB7093", "#FFB6C1"]

# 6. Interactive Visualizations
col1, col2 = st.columns(2)

with col1:
    st.subheader("Charges vs BMI")
    fig_scatter = px.scatter(
        filtered_df, 
        x="bmi", 
        y="charges", 
        color="smoker",
        color_discrete_sequence=["#FF69B4", "#8B008B"],
        hover_data=["age", "sex"],
        title="Impact of BMI & Smoking on Charges",
        labels={"bmi": "BMI", "charges": "Charges ($)"},
        template="plotly_white"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

with col2:
    st.subheader("Age Distribution vs Charges")
    fig_age = px.scatter(
        filtered_df, 
        x="age", 
        y="charges", 
        color="sex",
        color_discrete_sequence=["#FFB6C1", "#D33682"],
        trendline="ols", 
        title="How Charges Scale with Age",
        labels={"age": "Age", "charges": "Charges ($)"},
        template="plotly_white"
    )
    fig_age.update_traces(selector=dict(type='scatter', mode='lines'), line=dict(width=3))
    st.plotly_chart(fig_age, use_container_width=True)

# Row 2 of Visualizations
col3, col4 = st.columns(2)

with col3:
    st.subheader("📍 Average Charges by Region")
    df_region = filtered_df.groupby("region")["charges"].mean().reset_index()
    fig_bar = px.bar(
        df_region, 
        x="region", 
        y="charges", 
        color="region",
        color_discrete_sequence=PINK_PALETTE,
        title="Regional Cost Differences",
        labels={"region": "Region", "charges": "Avg Charges ($)"},
        template="plotly_white"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col4:
    st.subheader("🚬 Smoker Proportions")
    fig_pie = px.pie(
        filtered_df, 
        names="smoker", 
        title="Smoker vs. Non-Smoker Distribution",
        hole=0.4,
        color_discrete_sequence=["#FFC0CB", "#FF1493"],
        template="plotly_white"
    )
    st.plotly_chart(fig_pie, use_container_width=True)

st.divider()

# 7. Raw Data Viewer
st.subheader("♡ Raw Data Explorer ♡")
with st.expander("Click to view filtered dataset table"):
    st.dataframe(filtered_df, use_container_width=True)