import pandas as pd

df = pd.read_csv(
    "report1784771313929.csv",
    encoding="utf-8-sig"
)

df.columns = [
    "AccountName",
    "OpportunityName",
    "Stage",
    "LeadSource",
    "Type",
    "Probability",
    "Amount",
    "CloseDate",
    "Description"
]

print(df.head())
print()
print(df.info())

# 결측치 처리
df["AccountName"] = df["AccountName"].fillna("Unknown Account")
df["LeadSource"] = df["LeadSource"].fillna("Unknown")
df["Type"] = df["Type"].fillna("Unknown")
df["Description"] = df["Description"].fillna("")

# 전체 파이프라인 및 평균 딜 사이즈
total_pipeline = df["Amount"].sum()
average_deal_size = df["Amount"].mean()

print(f"Total Pipeline: KRW {total_pipeline:,.0f}")
print(f"Average Deal Size: KRW {average_deal_size:,.0f}")

# 리드 소스별 매출
lead_source_revenue = (
    df.groupby("LeadSource", dropna=False)["Amount"]
    .sum()
    .sort_values(ascending=False)
)

print(lead_source_revenue)

# 단계별 기회 수
stage_count = (
    df.groupby("Stage")
      .size()
      .sort_values(ascending=False)
)

print(stage_count)

# 단계별 매출
stage_revenue = (
    df.groupby("Stage")["Amount"]
      .sum()
      .sort_values(ascending=False)
)

# 단계별 매출 시각화
print(stage_revenue)

import matplotlib.pyplot as plt

stage_revenue.plot(
    kind="barh",
    figsize=(10,6)
)

plt.title("Pipeline Revenue by Stage")
plt.xlabel("Revenue (KRW)")
plt.tight_layout()

plt.show()

# 리드 소스별 매출 시각화
lead_source_revenue.plot(
    kind="barh",
    figsize=(10,6)
)

plt.title("Revenue by Lead Source")
plt.tight_layout()
plt.show()

# 단계별 매출 시각화
import matplotlib.pyplot as plt

plt.figure(figsize=(10,6))

stage_revenue.plot(kind="barh")

# 제목 설정
plt.title("Revenue by Stage")
plt.xlabel("Revenue (KRW)")
plt.ylabel("Stage")

plt.tight_layout()

plt.show()

# 단계별 기회 수 시각화
stage_count = (
    df.groupby("Stage")
      .size()
      .sort_values(ascending=False)
)

# 단계별 기회 수 시각화
print(stage_count)

plt.figure(figsize=(10,6))

stage_count.plot(kind="barh")

plt.title("Number of Opportunities by Stage")
plt.xlabel("Count")

plt.tight_layout()

plt.show()

# Won / Lost 데이터만 사용
closed_df = df[df["Stage"].isin(["Closed Won", "Closed Lost"])]

# 건수 계산
win_count = (closed_df["Stage"] == "Closed Won").sum()
lost_count = (closed_df["Stage"] == "Closed Lost").sum()

win_rate = win_count / (win_count + lost_count) * 100

print(f"Win Rate : {win_rate:.2f}%")

# 리드 소스별 승률
closed_df = df[df["Stage"].isin(["Closed Won", "Closed Lost"])]

lead_win = (
    closed_df
    .groupby(["LeadSource", "Stage"])
    .size()
    .unstack(fill_value=0)
)

lead_win["Win Rate"] = (
    lead_win["Closed Won"]
    / (lead_win["Closed Won"] + lead_win["Closed Lost"])
) * 100

print(lead_win)


import matplotlib.pyplot as plt

# Stage x Lead Source
pivot = pd.pivot_table(
    df,
    index="Stage",
    columns="LeadSource",
    values="Amount",
    aggfunc="sum",
    fill_value=0
)

print(pivot)

# Stage x Lead Source 시각화
plt.figure(figsize=(12,7))

plt.imshow(pivot, aspect="auto")

plt.colorbar(label="Revenue")

plt.xticks(range(len(pivot.columns)), pivot.columns, rotation=45)

plt.yticks(range(len(pivot.index)), pivot.index)

plt.title("Revenue by Stage and Lead Source")

plt.tight_layout()

plt.show()

# ==============================
# Average Deal Size by Lead Source
# ==============================

avg_deal = (
    df.groupby("LeadSource")["Amount"]
      .mean()
      .sort_values(ascending=False)
)

print("\nAverage Deal Size")
print(avg_deal)

# 평균 딜 사이즈 시각화
plt.figure(figsize=(10,6))

avg_deal.plot(
    kind="barh"
)

plt.title("Average Deal Size by Lead Source")

plt.xlabel("Average Deal Size (KRW)")

plt.tight_layout()

plt.show()

# 4분할 그래프
fig, axes = plt.subplots(
    2,
    2,
    figsize=(16,10)
)

plt.tight_layout()

# stage_revenue
stage_revenue.plot(
    kind="barh",
    ax=axes[0,0]
)

axes[0,0].set_title("Revenue by Stage")
axes[0,0].set_xlabel("KRW")

# lead_source_revenue
lead_source_revenue.plot(
    kind="barh",
    ax=axes[0,1]
)

axes[0,1].set_title("Revenue by Lead Source")
axes[0,1].set_xlabel("KRW")

# stage_count
stage_count.plot(
    kind="barh",
    ax=axes[1,0]
)

axes[1,0].set_title("Opportunity Count")
axes[1,0].set_xlabel("Count")

# avg_deal
avg_deal.plot(
    kind="barh",
    ax=axes[1,1]
)

axes[1,1].set_title("Average Deal Size")
axes[1,1].set_xlabel("KRW")

plt.tight_layout()

plt.show()


# %%
# Executive Dashboard
import matplotlib.pyplot as plt

# KPI
total_pipeline = df["Amount"].sum()
average_deal_size = df["Amount"].mean()
total_opportunities = len(df)

closed_df = df[df["Stage"].isin(["Closed Won", "Closed Lost"])]

won_count = (closed_df["Stage"] == "Closed Won").sum()
lost_count = (closed_df["Stage"] == "Closed Lost").sum()

win_rate = (
    won_count / (won_count + lost_count) * 100
    if won_count + lost_count > 0
    else 0
)

# 분석 데이터
stage_revenue = (
    df.groupby("Stage")["Amount"]
    .sum()
    .sort_values()
)

lead_source_revenue = (
    df.groupby("LeadSource")["Amount"]
    .sum()
    .sort_values()
)

stage_count = (
    df.groupby("Stage")
    .size()
    .sort_values()
)

avg_deal = (
    df.groupby("LeadSource")["Amount"]
    .mean()
    .sort_values()
)

# Dashboard canvas
fig = plt.figure(figsize=(18, 12))

grid = fig.add_gridspec(
    3,
    4,
    height_ratios=[0.7, 3, 3],
    hspace=0.45,
    wspace=0.4
)

# KPI cards
kpi_axes = [
    fig.add_subplot(grid[0, 0]),
    fig.add_subplot(grid[0, 1]),
    fig.add_subplot(grid[0, 2]),
    fig.add_subplot(grid[0, 3]),
]

kpi_values = [
    ("Total Pipeline", f"KRW {total_pipeline / 1_000_000:.1f}M"),
    ("Win Rate", f"{win_rate:.1f}%"),
    ("Average Deal Size", f"KRW {average_deal_size:,.0f}"),
    ("Total Opportunities", f"{total_opportunities:,}"),
]

for ax, (label, value) in zip(kpi_axes, kpi_values):
    ax.axis("off")
    ax.text(
        0.5,
        0.65,
        value,
        ha="center",
        va="center",
        fontsize=22,
        fontweight="bold"
    )
    ax.text(
        0.5,
        0.25,
        label,
        ha="center",
        va="center",
        fontsize=12
    )

# Revenue by Stage
ax1 = fig.add_subplot(grid[1, 0:2])
stage_revenue.plot(kind="barh", ax=ax1)
ax1.set_title("Revenue by Stage")
ax1.set_xlabel("Revenue (KRW)")
ax1.set_ylabel("")

# Revenue by Lead Source
ax2 = fig.add_subplot(grid[1, 2:4])
lead_source_revenue.plot(kind="barh", ax=ax2)
ax2.set_title("Revenue by Lead Source")
ax2.set_xlabel("Revenue (KRW)")
ax2.set_ylabel("")

# Opportunity Count by Stage
ax3 = fig.add_subplot(grid[2, 0:2])
stage_count.plot(kind="barh", ax=ax3)
ax3.set_title("Opportunity Count by Stage")
ax3.set_xlabel("Count")
ax3.set_ylabel("")

# Average Deal Size by Lead Source
ax4 = fig.add_subplot(grid[2, 2:4])
avg_deal.plot(kind="barh", ax=ax4)
ax4.set_title("Average Deal Size by Lead Source")
ax4.set_xlabel("Average Deal Size (KRW)")
ax4.set_ylabel("")

fig.suptitle(
    "Sales Strategy Executive Dashboard",
    fontsize=24,
    fontweight="bold",
    y=0.98
)

plt.savefig(
    "sales_strategy_dashboard.png",
    dpi=200,
    bbox_inches="tight"
)

plt.show()