import pandas as pd
import plotly.express as px
import streamlit as st
from pymongo import MongoClient
from sqlalchemy import create_engine

# --- CONFIG HALAMAN & TEMA KALEM ---
st.set_page_config(
    page_title="Executive Multi-DBMS Dashboard", page_icon="📊", layout="wide"
)

st.markdown(
    """
    <style>
    .stApp { background-color: #F8F9FA; color: #2C3E50; }
    .card-1 { background: linear-gradient(135deg, #FF9A9E 0%, #FECFEF 100%); padding: 18px; border-radius: 14px; color: #4A4A4A; text-align: center; }
    .card-2 { background: linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%); padding: 18px; border-radius: 14px; color: #334E68; text-align: center; }
    .card-3 { background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%); padding: 18px; border-radius: 14px; color: #2D5B4F; text-align: center; }
    .card-4 { background: linear-gradient(135deg, #cfd9df 0%, #e2ebf0 100%); padding: 18px; border-radius: 14px; color: #334E68; text-align: center; }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("📊 Executive Multi-DBMS Analytics Dashboard")
st.markdown(
    "Arsitektur Data: **PostgreSQL (Neon Cloud)** $\\times$ **MongoDB (Atlas Cloud)**"
)

POSTGRES_URI = "postgresql+psycopg2://neondb_owner:npg_oHBA5uTty2dp@ep-round-mode-az9m403y-pooler.c-3.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"
MONGO_URI = "mongodb+srv://230660121085_db_user:vfkhXq7ZXGRkRhYL@gvioa.d7mdyg3.mongodb.net/?retryWrites=true&w=majority"


@st.cache_data
def load_data():
    pg_engine = create_engine(POSTGRES_URI)
    df_orders = pd.read_sql(
        "SELECT order_id, order_status FROM orders", pg_engine
    )

    mongo_client = MongoClient(MONGO_URI)
    db = mongo_client["gvioa_db"]
    df_reviews = pd.DataFrame(
        list(
            db["order_reviews"].find(
                {}, {"_id": 0, "order_id": 1, "review_score": 1}
            )
        )
    )

    return pd.merge(df_orders, df_reviews, on="order_id", how="inner")


# Tampilkan spinner loading saat ambil data
with st.spinner("Mengambil data dari PostgreSQL & MongoDB..."):
    df = load_data()

# --- SIDEBAR FILTER ---
st.sidebar.title("⚙️ Filter Control")
selected_status = st.sidebar.multiselect(
    "Pilih Status Pesanan:",
    options=df["order_status"].unique(),
    default=df["order_status"].unique(),
)

df_filtered = df[df["order_status"].isin(selected_status)]

# --- METRIC CARDS ---
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(
        f'<div class="card-1"><h3>📦 Total Pesanan</h3><h2>{len(df_filtered):,}</h2></div>',
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        f'<div class="card-2"><h3>⭐ Rata-rata Rating</h3><h2>{df_filtered["review_score"].mean():.2f} / 5.0</h2></div>',
        unsafe_allow_html=True,
    )
with c3:
    star5 = len(df_filtered[df_filtered["review_score"] == 5])
    st.markdown(
        f'<div class="card-3"><h3>🌸 Bintang 5</h3><h2>{star5:,}</h2></div>',
        unsafe_allow_html=True,
    )
with c4:
    deliv = len(df_filtered[df_filtered["order_status"] == "delivered"])
    st.markdown(
        f'<div class="card-4"><h3>🚚 Terkirim</h3><h2>{deliv:,}</h2></div>',
        unsafe_allow_html=True,
    )

st.write("")
st.divider()

# --- ROW 1 CHARTS ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("⭐ Distribusi Rating Pelanggan (MongoDB)")
    score_df = df_filtered["review_score"].value_counts().reset_index()
    score_df.columns = ["Rating", "Jumlah"]
    fig_bar = px.bar(
        score_df,
        x="Rating",
        y="Jumlah",
        color="Rating",
        color_continuous_scale="Tealgrn",
        text="Jumlah",
        template="plotly_white",
    )
    fig_bar.update_layout(showlegend=False, height=350)
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    st.subheader("🍩 Proporsi Status Pesanan (PostgreSQL)")
    status_df = df_filtered["order_status"].value_counts().reset_index()
    status_df.columns = ["Status", "Jumlah"]
    fig_pie = px.pie(
        status_df,
        values="Jumlah",
        names="Status",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel,
        template="plotly_white",
    )
    fig_pie.update_layout(height=350)
    st.plotly_chart(fig_pie, use_container_width=True)

# --- ROW 2 CHARTS ---
col3, col4 = st.columns(2)

with col3:
    st.subheader("📊 Performa Rating per Status Pesanan")
    avg_status = (
        df_filtered.groupby("order_status")["review_score"]
        .mean()
        .reset_index()
        .sort_values(by="review_score", ascending=False)
    )
    fig_status = px.bar(
        avg_status,
        x="order_status",
        y="review_score",
        color="review_score",
        color_continuous_scale="Purp",
        text_auto=".2f",
        template="plotly_white",
    )
    fig_status.update_layout(height=350, showlegend=False)
    st.plotly_chart(fig_status, use_container_width=True)

with col4:
    st.subheader("🧩 Treemap Komposisi Status Pesanan")
    fig_tree = px.treemap(
        status_df,
        path=["Status"],
        values="Jumlah",
        color="Jumlah",
        color_continuous_scale="Mint",
        template="plotly_white",
    )
    fig_tree.update_layout(height=350)
    st.plotly_chart(fig_tree, use_container_width=True)

# --- TABEL DATA ---
with st.expander("🔍 Lihat Detail Data Tergabung"):
    st.dataframe(df_filtered.head(100), use_container_width=True)