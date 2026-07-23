import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Sales Strategy Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("report1784771313929.csv", encoding="utf-8-sig")
    df.columns = [
        "AccountName",
        "OpportunityName",
        "Stage",
        "LeadSource",
        "Type",
        "Probability",
        "Amount",
        "CloseDate",
        "Description",
    ]
    df["AccountName"] = df["AccountName"].fillna("Unknown Account")
    df["LeadSource"] = df["LeadSource"].fillna("Unknown")
    df["Type"] = df["Type"].fillna("Unknown")
    df["Description"] = df["Description"].fillna("")
    return df

df = load_data()

st.title("Sales Strategy Executive Dashboard")

# 사이드바 필터
lead_sources = sorted(df["LeadSource"].unique())
selected_sources = st.sidebar.multiselect(
    "Lead Source", lead_sources, default=lead_sources
)
df = df[df["LeadSource"].isin(selected_sources)]

# KPI
total_pipeline = df["Amount"].sum()
average_deal_size = df["Amount"].mean()
total_opportunities = len(df)

closed_df = df[df["Stage"].isin(["Closed Won", "Closed Lost"])]
won_count = (closed_df["Stage"] == "Closed Won").sum()
lost_count = (closed_df["Stage"] == "Closed Lost").sum()
win_rate = won_count / (won_count + lost_count) * 100 if won_count + lost_count > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Pipeline", f"KRW {total_pipeline / 1_000_000:.1f}M")
col2.metric("Win Rate", f"{win_rate:.1f}%")
col3.metric("Average Deal Size", f"KRW {average_deal_size:,.0f}")
col4.metric("Total Opportunities", f"{total_opportunities:,}")

st.divider()

# 분석 데이터
stage_revenue = df.groupby("Stage")["Amount"].sum().sort_values()
lead_source_revenue = df.groupby("LeadSource")["Amount"].sum().sort_values()
stage_count = df.groupby("Stage").size().sort_values()
avg_deal = df.groupby("LeadSource")["Amount"].mean().sort_values()

row1_col1, row1_col2 = st.columns(2)
row2_col1, row2_col2 = st.columns(2)


def barh_chart(series, title, xlabel):
    fig, ax = plt.subplots(figsize=(6, 4))
    series.plot(kind="barh", ax=ax)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    fig.tight_layout()
    return fig


with row1_col1:
    st.pyplot(barh_chart(stage_revenue, "Revenue by Stage", "Revenue (KRW)"))

with row1_col2:
    st.pyplot(barh_chart(lead_source_revenue, "Revenue by Lead Source", "Revenue (KRW)"))

with row2_col1:
    st.pyplot(barh_chart(stage_count, "Opportunity Count by Stage", "Count"))

with row2_col2:
    st.pyplot(barh_chart(avg_deal, "Average Deal Size by Lead Source", "Average Deal Size (KRW)"))

st.divider()

# Stage x Lead Source 히트맵
st.subheader("Revenue by Stage and Lead Source")
pivot = pd.pivot_table(
    df, index="Stage", columns="LeadSource", values="Amount", aggfunc="sum", fill_value=0
)
fig, ax = plt.subplots(figsize=(10, 5))
im = ax.imshow(pivot, aspect="auto")
fig.colorbar(im, label="Revenue")
ax.set_xticks(range(len(pivot.columns)))
ax.set_xticklabels(pivot.columns, rotation=45, ha="right")
ax.set_yticks(range(len(pivot.index)))
ax.set_yticklabels(pivot.index)
fig.tight_layout()
st.pyplot(fig)

# 리드 소스별 승률
st.subheader("Win Rate by Lead Source")
lead_win = (
    closed_df.groupby(["LeadSource", "Stage"]).size().unstack(fill_value=0)
)
if "Closed Won" in lead_win.columns and "Closed Lost" in lead_win.columns:
    lead_win["Win Rate (%)"] = (
        lead_win["Closed Won"] / (lead_win["Closed Won"] + lead_win["Closed Lost"]) * 100
    )
st.dataframe(lead_win, use_container_width=True)

with st.expander("Raw Data"):
    st.dataframe(df, use_container_width=True)
