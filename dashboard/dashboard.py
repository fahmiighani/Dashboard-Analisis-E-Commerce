from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

sns.set_theme(style="whitegrid")
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
TAHUN = 2017

st.set_page_config(page_title="Dashboard E-Commerce Olist 2017", page_icon="🛒", layout="wide")


# ---------------------------------------------------------------- DATA
@st.cache_data
def load_data():
    orders = pd.read_csv(
        DATA_DIR / "orders_dataset.csv",
        parse_dates=[
            "order_purchase_timestamp",
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
        ],
    )
    items = pd.read_csv(DATA_DIR / "order_items_dataset.csv")
    products = pd.read_csv(DATA_DIR / "products_dataset.csv")
    trans = pd.read_csv(DATA_DIR / "product_category_name_translation.csv", encoding="utf-8-sig")
    reviews = pd.read_csv(DATA_DIR / "order_reviews_dataset.csv")

    # Hanya pesanan delivered tahun 2017
    orders = orders[
        (orders["order_status"] == "delivered")
        & (orders["order_purchase_timestamp"].dt.year == TAHUN)
    ].dropna(subset=["order_delivered_customer_date"]).copy()
    orders["bulan"] = orders["order_purchase_timestamp"].dt.month

    # Revenue per kategori
    rev = (
        items.merge(orders[["order_id", "bulan"]], on="order_id")
        .merge(products[["product_id", "product_category_name"]], on="product_id", how="left")
        .merge(trans, on="product_category_name", how="left")
    )
    rev["kategori"] = (
        rev["product_category_name_english"]
        .fillna(rev["product_category_name"])
        .fillna("unknown")
    )

    # Keterlambatan & review (1 review per order)
    reviews = reviews.sort_values("review_answer_timestamp").drop_duplicates("order_id", keep="last")
    rv = orders.merge(reviews[["order_id", "review_score"]], on="order_id").dropna(subset=["review_score"])
    rv["selisih_hari"] = (
        rv["order_delivered_customer_date"] - rv["order_estimated_delivery_date"]
    ).dt.total_seconds() / 86400
    rv["status"] = rv["selisih_hari"].gt(0).map({True: "Terlambat", False: "Tepat Waktu"})
    rv["kelompok"] = pd.cut(
        rv["selisih_hari"],
        bins=[-float("inf"), 0, 3, 7, 14, float("inf")],
        labels=["Tepat waktu", "Telat 1-3 hari", "Telat 4-7 hari", "Telat 8-14 hari", "Telat >14 hari"],
    )
    return rev, rv


rev_df, rv_df = load_data()

# ---------------------------------------------------------------- SIDEBAR
st.sidebar.title("🛒 Filter")
bulan_min, bulan_max = st.sidebar.slider("Rentang bulan (2017)", 1, 12, (1, 12))
threshold = st.sidebar.slider("Ambang kontribusi revenue (%)", 1, 20, 10)
top_n = st.sidebar.slider("Jumlah kategori ditampilkan", 5, 20, 10)
skor_batas = st.sidebar.slider("Ambang rata-rata skor ulasan", 1.0, 5.0, 2.5, 0.1)

rev_f = rev_df[rev_df["bulan"].between(bulan_min, bulan_max)]
rv_f = rv_df[rv_df["bulan"].between(bulan_min, bulan_max)]

# ---------------------------------------------------------------- HEADER
st.title("Dashboard Analisis E-Commerce Olist - 2017")
st.caption("Pesanan berstatus *delivered* | Fokus: kontribusi revenue kategori & dampak keterlambatan terhadap ulasan")

total_rev = rev_f["price"].sum()
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Revenue", f"R$ {total_rev:,.0f}")
c2.metric("Jumlah Pesanan", f"{rev_f['order_id'].nunique():,}")
c3.metric("Rata-rata Skor Review", f"{rv_f['review_score'].mean():.2f}")
c4.metric("% Pesanan Terlambat", f"{(rv_f['status'] == 'Terlambat').mean() * 100:.1f}%")

tab1, tab2 = st.tabs(["💰 Pertanyaan 1: Revenue Kategori", "🚚 Pertanyaan 2: Keterlambatan vs Review"])

# ---------------------------------------------------------------- TAB 1
with tab1:
    st.subheader(f"Kategori dengan kontribusi revenue > {threshold}% (2017)")
    share = (
        rev_f.groupby("kategori")["price"].sum().sort_values(ascending=False).to_frame("revenue")
    )
    share["persen"] = share["revenue"] / share["revenue"].sum() * 100
    top = share.head(top_n).reset_index()

    fig, ax = plt.subplots(figsize=(10, 5.5))
    colors = ["#1f77b4" if p > threshold else "#c7c7c7" for p in top["persen"]]
    sns.barplot(data=top, x="persen", y="kategori", palette=colors, hue="kategori", legend=False, ax=ax)
    ax.axvline(threshold, color="red", linestyle="--", label=f"Ambang {threshold}%")
    for i, v in enumerate(top["persen"]):
        ax.text(v + 0.1, i, f"{v:.1f}%", va="center")
    ax.set_xlabel("Kontribusi terhadap total revenue (%)")
    ax.set_ylabel("")
    ax.legend()
    st.pyplot(fig)

    lolos = share[share["persen"] > threshold]
    if lolos.empty:
        st.warning(
            f"Tidak ada kategori yang melampaui {threshold}% pada rentang yang dipilih. "
            f"Kategori teratas: **{share.index[0]}** ({share['persen'].iloc[0]:.2f}%)."
        )
    else:
        st.success("Kategori di atas ambang: " + ", ".join(lolos.index))

    with st.expander("Lihat tabel lengkap"):
        st.dataframe(share.round(2))

# ---------------------------------------------------------------- TAB 2
with tab2:
    st.subheader("Rata-rata skor ulasan: tepat waktu vs terlambat")
    ringkas = rv_f.groupby("status")["review_score"].agg(["mean", "count"]).reset_index()
    kel = rv_f.groupby("kelompok", observed=True)["review_score"].agg(["mean", "count"]).reset_index()

    col_a, col_b = st.columns(2)
    with col_a:
        fig, ax = plt.subplots(figsize=(5.5, 4.5))
        sns.barplot(data=ringkas, x="status", y="mean", hue="status",
                    palette={"Tepat Waktu": "#2ca02c", "Terlambat": "#d62728"}, legend=False, ax=ax)
        ax.axhline(skor_batas, color="black", linestyle="--", label=f"Ambang {skor_batas}")
        for i, r in ringkas.iterrows():
            ax.text(i, r["mean"] + 0.05, f"{r['mean']:.2f}\n(n={int(r['count']):,})", ha="center")
        ax.set_ylim(0, 5.5)
        ax.set_xlabel("")
        ax.set_ylabel("Rata-rata skor (1-5)")
        ax.legend()
        st.pyplot(fig)
    with col_b:
        fig, ax = plt.subplots(figsize=(6.5, 4.5))
        sns.barplot(data=kel, x="kelompok", y="mean", color="#ff7f0e", ax=ax)
        ax.axhline(skor_batas, color="black", linestyle="--")
        for i, r in kel.iterrows():
            ax.text(i, r["mean"] + 0.05, f"{r['mean']:.2f}", ha="center")
        ax.set_ylim(0, 5.5)
        ax.set_xlabel("")
        ax.set_ylabel("Rata-rata skor (1-5)")
        plt.xticks(rotation=20)
        st.pyplot(fig)

    terlambat = ringkas.loc[ringkas["status"] == "Terlambat", "mean"]
    if not terlambat.empty:
        nilai = terlambat.iloc[0]
        if nilai < skor_batas:
            st.error(f"Rata-rata skor pesanan terlambat **{nilai:.2f}** berada di bawah ambang {skor_batas}.")
        else:
            st.info(f"Rata-rata skor pesanan terlambat **{nilai:.2f}**, belum di bawah ambang {skor_batas}.")

st.caption("Sumber data: Brazilian E-Commerce Public Dataset by Olist")
