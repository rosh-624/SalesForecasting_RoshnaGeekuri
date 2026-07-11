# import streamlit as st
# import pandas as pd
# import numpy as np
# import plotly.express as px
# import os
# from prophet import Prophet
# from sklearn.metrics import mean_absolute_error, mean_squared_error

# st.set_page_config(
#     page_title="Intelligent Sales Forecasting Dashboard",
#     page_icon="📊",
#     layout="wide"
# )

# st.title("📊 Intelligent Sales Forecasting Dashboard")
# st.write("Welcome to the Sales Forecasting Dashboard!")
# st.caption("Developed by Roshna Geekuri")

# # -----------------------------
# # Load Dataset
# # -----------------------------
# df = pd.read_csv("train.csv")

# # Fix Date Format
# df["Order Date"] = pd.to_datetime(
#     df["Order Date"],
#     dayfirst=True,
#     format="mixed",
#     errors="coerce"
# )

# df = df.dropna(subset=["Order Date"])

# # Create Year & Month Columns
# df["Year"] = df["Order Date"].dt.year
# df["Month"] = df["Order Date"].dt.to_period("M").astype(str)

# # -----------------------------
# # Sidebar
# # -----------------------------
# st.sidebar.title("Navigation")

# page = st.sidebar.radio(
#     "Go To",
#     [
#         "Sales Overview",
#         "Forecast Explorer",
#         "Anomaly Report",
#         "Demand Segments"
#     ]
# )

# # ==================================================
# # PAGE 1 : SALES OVERVIEW
# # ==================================================

# if page == "Sales Overview":

#     st.header("📈 Sales Overview Dashboard")

#     region = st.sidebar.selectbox(
#         "Region",
#         ["All"] + sorted(df["Region"].unique())
#     )

#     category = st.sidebar.selectbox(
#         "Category",
#         ["All"] + sorted(df["Category"].unique())
#     )

#     filtered_df = df.copy()

#     if region != "All":
#         filtered_df = filtered_df[
#             filtered_df["Region"] == region
#         ]

#     if category != "All":
#         filtered_df = filtered_df[
#             filtered_df["Category"] == category
#         ]

#     # KPI Cards

#     total_sales = filtered_df["Sales"].sum()

#     total_orders = filtered_df["Order ID"].nunique()

#     avg_order = filtered_df["Sales"].mean()

#     c1, c2, c3 = st.columns(3)

#     c1.metric(
#         "Total Sales",
#         f"${total_sales:,.0f}"
#     )

#     c2.metric(
#         "Orders",
#         total_orders
#     )

#     c3.metric(
#         "Average Order Value",
#         f"${avg_order:.2f}"
#     )

#     st.divider()

#     # -----------------------------
#     # Sales by Year
#     # -----------------------------
#     yearly = (
#         filtered_df
#         .groupby("Year")["Sales"]
#         .sum()
#         .reset_index()
#     )

#     fig1 = px.bar(
#         yearly,
#         x="Year",
#         y="Sales",
#         text_auto=True,
#         title="Total Sales by Year"
#     )

#     st.plotly_chart(fig1, use_container_width=True)

#     # -----------------------------
#     # Monthly Trend
#     # -----------------------------

#     monthly = (
#         filtered_df
#         .groupby("Month")["Sales"]
#         .sum()
#         .reset_index()
#     )

#     fig2 = px.line(
#         monthly,
#         x="Month",
#         y="Sales",
#         markers=True,
#         title="Monthly Sales Trend"
#     )

#     st.plotly_chart(fig2, use_container_width=True)
#     # ==================================================
# # PAGE 2 : FORECAST EXPLORER
# # ==================================================

# elif page == "Forecast Explorer":

#     st.header("📈 Forecast Explorer")

#     forecast_type = st.selectbox(
#         "Forecast By",
#         ["Category", "Region"]
#     )

#     if forecast_type == "Category":
#         selected = st.selectbox(
#             "Select Category",
#             sorted(df["Category"].unique())
#         )

#         temp = df[df["Category"] == selected]

#     else:
#         selected = st.selectbox(
#             "Select Region",
#             sorted(df["Region"].unique())
#         )

#         temp = df[df["Region"] == selected]

#     months = st.slider(
#         "Forecast Horizon (Months)",
#         min_value=1,
#         max_value=3,
#         value=1
#     )

#     monthly_sales = (
#         temp
#         .groupby("Month")["Sales"]
#         .sum()
#         .reset_index()
#     )

#     monthly_sales["Month"] = pd.to_datetime(monthly_sales["Month"])

#     # Simple Forecast (using average of last 3 months)
#     last3 = monthly_sales["Sales"].tail(3).mean()

#     future_dates = pd.date_range(
#         monthly_sales["Month"].max() + pd.offsets.MonthBegin(),
#         periods=months,
#         freq="MS"
#     )

#     forecast_df = pd.DataFrame({
#         "Month": future_dates,
#         "Forecast Sales": [last3] * months
#     })

#     fig = px.line(
#         monthly_sales,
#         x="Month",
#         y="Sales",
#         title="Historical Sales"
#     )

#     fig.add_scatter(
#         x=forecast_df["Month"],
#         y=forecast_df["Forecast Sales"],
#         mode="lines+markers",
#         name="Forecast"
#     )

#     st.plotly_chart(fig, use_container_width=True)

#     st.subheader("Forecast Values")

#     st.dataframe(forecast_df)

#     st.subheader("Model Performance")

#     mae = 128.54
#     rmse = 182.91

#     c1, c2 = st.columns(2)

#     c1.metric("MAE", f"{mae:.2f}")
#     c2.metric("RMSE", f"{rmse:.2f}")

#     st.info(
#         "Replace this simple forecast with your best model "
#         "(SARIMA / Prophet / XGBoost) if available."
#     )
#     # ==================================================
# # PAGE 3 : ANOMALY REPORT
# # ==================================================

# elif page == "Anomaly Report":

#     from sklearn.ensemble import IsolationForest

#     st.header("🚨 Sales Anomaly Report")

#     # Weekly Sales
#     weekly_sales = (
#         df
#         .set_index("Order Date")
#         .resample("W")["Sales"]
#         .sum()
#         .reset_index()
#     )

#     # -----------------------------
#     # Isolation Forest
#     # -----------------------------

#     model = IsolationForest(
#         contamination=0.05,
#         random_state=42
#     )

#     weekly_sales["Anomaly"] = model.fit_predict(
#         weekly_sales[["Sales"]]
#     )

#     weekly_sales["Type"] = weekly_sales["Anomaly"].map(
#         {
#             1: "Normal",
#             -1: "Anomaly"
#         }
#     )

#     fig = px.line(
#         weekly_sales,
#         x="Order Date",
#         y="Sales",
#         title="Weekly Sales with Detected Anomalies"
#     )

#     anomaly_points = weekly_sales[
#         weekly_sales["Type"] == "Anomaly"
#     ]

#     fig.add_scatter(
#         x=anomaly_points["Order Date"],
#         y=anomaly_points["Sales"],
#         mode="markers",
#         marker=dict(
#             color="red",
#             size=10
#         ),
#         name="Anomaly"
#     )

#     st.plotly_chart(
#         fig,
#         width="stretch"
#     )

#     st.subheader("Detected Anomalies")

#     st.dataframe(

#         anomaly_points[
#             [
#                 "Order Date",
#                 "Sales"
#             ]
#         ]

#     )

#     # -----------------------------
#     # Z-Score Detection
#     # -----------------------------

#     rolling_mean = (
#         weekly_sales["Sales"]
#         .rolling(
#             window=4,
#             center=True
#         )
#         .mean()
#     )

#     rolling_std = (
#         weekly_sales["Sales"]
#         .rolling(
#             window=4,
#             center=True
#         )
#         .std()
#     )

#     zscore = (
#         weekly_sales["Sales"] -
#         rolling_mean
#     ) / rolling_std

#     weekly_sales["ZScore"] = zscore

#     weekly_sales["Z_Anomaly"] = (
#         abs(zscore) > 2
#     )

#     st.subheader("Z-Score Detected Weeks")

#     st.dataframe(

#         weekly_sales[
#             weekly_sales["Z_Anomaly"]
#         ][
#             [
#                 "Order Date",
#                 "Sales",
#                 "ZScore"
#             ]
#         ]

#     )

#     st.success(
#         "Isolation Forest captures multivariate outliers, "
#         "while Z-Score flags statistical deviations. "
#         "Comparing both methods improves confidence in anomaly detection."
#     )
#     # ==================================================
# # PAGE 4 : PRODUCT DEMAND SEGMENTS
# # ==================================================

# elif page == "Demand Segments":

#     from sklearn.preprocessing import StandardScaler
#     from sklearn.cluster import KMeans
#     from sklearn.decomposition import PCA

#     st.header("📦 Product Demand Segmentation")

#     # ---------------------------------------------
#     # Monthly Sales
#     # ---------------------------------------------

#     monthly = df.copy()

#     monthly["YearMonth"] = (
#         monthly["Order Date"]
#         .dt.to_period("M")
#         .astype(str)
#     )

#     monthly_sales = (

#         monthly

#         .groupby(

#             ["Sub-Category", "YearMonth"]

#         )["Sales"]

#         .sum()

#         .reset_index()

#     )

#     # ---------------------------------------------
#     # Feature Engineering
#     # ---------------------------------------------

#     feature_df = (

#         monthly_sales

#         .groupby("Sub-Category")

#         .agg(

#             Total_Sales=("Sales", "sum"),

#             Avg_Monthly_Sales=("Sales", "mean"),

#             Sales_Volatility=("Sales", "std")

#         )

#         .fillna(0)

#         .reset_index()

#     )

#     avg_order = (

#         df

#         .groupby("Sub-Category")["Sales"]

#         .mean()

#         .reset_index(name="Average_Order_Value")

#     )

#     feature_df = feature_df.merge(

#         avg_order,

#         on="Sub-Category"

#     )

#     # Simple Growth Rate

#     growth = (

#         monthly_sales

#         .groupby("Sub-Category")

#         .apply(

#             lambda x:

#             (

#                 x["Sales"].iloc[-1]

#                 -

#                 x["Sales"].iloc[0]

#             )

#             /

#             max(

#                 x["Sales"].iloc[0],

#                 1

#             )

#         )

#         .reset_index(name="Growth_Rate")

#     )

#     feature_df = feature_df.merge(

#         growth,

#         on="Sub-Category"

#     )

#     # ---------------------------------------------
#     # Scaling
#     # ---------------------------------------------

#     X = feature_df.drop(

#         columns=["Sub-Category"]

#     )

#     scaler = StandardScaler()

#     X_scaled = scaler.fit_transform(X)

#     # ---------------------------------------------
#     # KMeans
#     # ---------------------------------------------

#     kmeans = KMeans(

#         n_clusters=4,

#         random_state=42,

#         n_init=10

#     )

#     feature_df["Cluster"] = kmeans.fit_predict(

#         X_scaled

#     )

#     # ---------------------------------------------
#     # Cluster Labels
#     # ---------------------------------------------

#     cluster_names = {

#         0: "High Volume",

#         1: "Growing Demand",

#         2: "Stable Demand",

#         3: "Low Volume"

#     }

#     feature_df["Demand Segment"] = (

#         feature_df["Cluster"]

#         .map(cluster_names)

#     )

#     # ---------------------------------------------
#     # PCA Visualization
#     # ---------------------------------------------

#     pca = PCA(n_components=2)

#     components = pca.fit_transform(

#         X_scaled

#     )

#     feature_df["PC1"] = components[:, 0]

#     feature_df["PC2"] = components[:, 1]

#     fig = px.scatter(

#         feature_df,

#         x="PC1",

#         y="PC2",

#         color="Demand Segment",

#         hover_name="Sub-Category",

#         title="Demand Segmentation using K-Means + PCA"

#     )

#     st.plotly_chart(

#         fig,

#         width="stretch"

#     )

#     st.subheader("Cluster Membership")

#     st.dataframe(

#         feature_df[

#             [

#                 "Sub-Category",

#                 "Demand Segment"

#             ]

#         ]

#     )

#     st.subheader("Recommended Stocking Strategy")

#     strategy = pd.DataFrame({

#         "Demand Segment": [

#             "High Volume",

#             "Growing Demand",

#             "Stable Demand",

#             "Low Volume"

#         ],

#         "Recommended Strategy": [

#             "Maintain high inventory with frequent replenishment.",

#             "Increase stock gradually to meet rising demand.",

#             "Keep consistent inventory and monitor trends.",

#             "Reduce inventory and avoid overstocking."

#         ]

#     })

#     st.table(strategy)

#     st.success(
#     "Forecasts are generated using the forecasting model developed in Task 4. "
#     "The dashboard visualizes future demand and reports the model's evaluation metrics."
# )

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import xgboost as xgb
from sklearn.model_selection import train_test_split

from prophet import Prophet

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error
)

from sklearn.ensemble import IsolationForest
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Intelligent Sales Forecasting Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Intelligent Sales Forecasting & Demand Intelligence System")
st.caption("Developed by Roshna Geekuri")

# ---------------------------------------------------
# CACHE DATA
# ---------------------------------------------------

@st.cache_data
def load_data():

    df = pd.read_csv("train.csv")

    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        errors="coerce",
        dayfirst=True,
        format="mixed"
    )

    df["Ship Date"] = pd.to_datetime(
        df["Ship Date"],
        errors="coerce",
        dayfirst=True,
        format="mixed"
    )

    df = df.dropna(subset=["Order Date"])

    df["Year"] = df["Order Date"].dt.year

    df["Month"] = (
        df["Order Date"]
        .dt.to_period("M")
        .astype(str)
    )

    df["Quarter"] = df["Order Date"].dt.quarter

    df["Week"] = df["Order Date"].dt.isocalendar().week

    df["Day"] = df["Order Date"].dt.day_name()

    return df


# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

try:
    df = load_data()

except Exception as e:

    st.error("Unable to load train.csv")

    st.exception(e)

    st.stop()

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.image(
    "https://img.icons8.com/color/96/combo-chart--v1.png",
    width=80
)

st.sidebar.title("Navigation")

page = st.sidebar.radio(

    "Select Dashboard",

    [

        "Sales Overview",

        "Forecast Explorer",

        "Anomaly Report",

        "Demand Segments"

    ]

)

# ===========================================================
# PAGE 1
# ===========================================================

if page == "Sales Overview":

    st.header("📈 Sales Overview Dashboard")

    region = st.sidebar.selectbox(

        "Region",

        ["All"] + sorted(df["Region"].unique())

    )

    category = st.sidebar.selectbox(

        "Category",

        ["All"] + sorted(df["Category"].unique())

    )

    filtered = df.copy()

    if region != "All":

        filtered = filtered[
            filtered["Region"] == region
        ]

    if category != "All":

        filtered = filtered[
            filtered["Category"] == category
        ]

    # ------------------------------------------------
    # KPI CARDS
    # ------------------------------------------------

    total_sales = filtered["Sales"].sum()

    total_orders = filtered["Order ID"].nunique()

    avg_order = filtered["Sales"].mean()

    avg_ship = (
        filtered["Ship Date"] -
        filtered["Order Date"]
    ).dt.days.mean()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Sales",
        f"${total_sales:,.0f}"
    )

    c2.metric(
        "Orders",
        total_orders
    )

    c3.metric(
        "Average Order Value",
        f"${avg_order:,.2f}"
    )

    c4.metric(
        "Avg Shipping Days",
        f"{avg_ship:.1f}"
    )

    st.divider()

    # ------------------------------------------------
    # YEARLY SALES
    # ------------------------------------------------

    yearly = (

        filtered

        .groupby("Year")["Sales"]

        .sum()

        .reset_index()

    )

    fig = px.bar(

        yearly,

        x="Year",

        y="Sales",

        text_auto=".2s",

        color="Sales",

        title="Total Sales by Year"

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ------------------------------------------------
    # MONTHLY TREND
    # ------------------------------------------------

    monthly = (

        filtered

        .groupby("Month")["Sales"]

        .sum()

        .reset_index()

    )

    monthly["Month"] = pd.to_datetime(
        monthly["Month"]
    )

    fig = px.line(

        monthly,

        x="Month",

        y="Sales",

        markers=True,

        title="Monthly Sales Trend"

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ------------------------------------------------
    # REGION SALES
    # ------------------------------------------------

    left, right = st.columns(2)

    region_sales = (

        filtered

        .groupby("Region")["Sales"]

        .sum()

        .reset_index()

    )

    fig = px.pie(

        region_sales,

        names="Region",

        values="Sales",

        hole=0.45,

        title="Sales by Region"

    )

    left.plotly_chart(
        fig,
        use_container_width=True
    )

    category_sales = (

        filtered

        .groupby("Category")["Sales"]

        .sum()

        .reset_index()

    )

    fig = px.bar(

        category_sales,

        x="Category",

        y="Sales",

        color="Category",

        title="Sales by Category"

    )

    right.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("Filtered Dataset")

    st.dataframe(
        filtered,
        use_container_width=True
    )
    # ==========================================================
# PAGE 2 : FORECAST EXPLORER
# ==========================================================

elif page == "Forecast Explorer":

    st.header("📈 Sales Forecast Explorer")

    forecast_type = st.selectbox(
        "Forecast Based On",
        ["Category", "Region"]
    )

    if forecast_type == "Category":

        selected = st.selectbox(
            "Select Category",
            sorted(df["Category"].unique())
        )

        temp = df[df["Category"] == selected]

    else:

        selected = st.selectbox(
            "Select Region",
            sorted(df["Region"].unique())
        )

        temp = df[df["Region"] == selected]

    forecast_months = st.slider(
        "Forecast Horizon",
        1,
        3,
        3
    )

    # ----------------------------
    # Monthly Aggregation
    # ----------------------------

    prophet_df = (

        temp

        .groupby("Month")["Sales"]

        .sum()

        .reset_index()

    )

    prophet_df["Month"] = pd.to_datetime(prophet_df["Month"])

    prophet_df = prophet_df.rename(
        columns={
            "Month": "ds",
            "Sales": "y"
        }
    )

    if len(prophet_df) < 12:

        st.warning(
            "Not enough historical data for forecasting."
        )

    else:

        # ----------------------------
        # Train Test Split
        # ----------------------------

        train = prophet_df.iloc[:-3]

        test = prophet_df.iloc[-3:]

        model = Prophet(

            yearly_seasonality=True,

            weekly_seasonality=False,

            daily_seasonality=False

        )

        model.fit(train)

        future = model.make_future_dataframe(

            periods=3,

            freq="MS"

        )

        forecast = model.predict(future)

        pred = forecast.tail(3)["yhat"].values

        actual = test["y"].values

        mae = mean_absolute_error(

            actual,

            pred

        )

        rmse = np.sqrt(

            mean_squared_error(

                actual,

                pred

            )

        )

        # ----------------------------
        # Retrain on Full Dataset
        # ----------------------------

        final_model = Prophet(

            yearly_seasonality=True,

            weekly_seasonality=False,

            daily_seasonality=False

        )

        final_model.fit(prophet_df)

        future2 = final_model.make_future_dataframe(

            periods=forecast_months,

            freq="MS"

        )

        forecast2 = final_model.predict(future2)

        future_forecast = forecast2.tail(

            forecast_months

        )[

            [

                "ds",

                "yhat",

                "yhat_lower",

                "yhat_upper"

            ]

        ]

        # ----------------------------
        # Historical + Forecast Plot
        # ----------------------------

        import plotly.graph_objects as go

        fig = go.Figure()

        fig.add_trace(

            go.Scatter(

                x=prophet_df["ds"],

                y=prophet_df["y"],

                mode="lines+markers",

                name="Historical Sales"

            )

        )

        fig.add_trace(

            go.Scatter(

                x=future_forecast["ds"],

                y=future_forecast["yhat"],

                mode="lines+markers",

                name="Forecast"

            )

        )

        fig.add_trace(

            go.Scatter(

                x=future_forecast["ds"],

                y=future_forecast["yhat_upper"],

                line=dict(width=0),

                showlegend=False

            )

        )

        fig.add_trace(

            go.Scatter(

                x=future_forecast["ds"],

                y=future_forecast["yhat_lower"],

                fill='tonexty',

                line=dict(width=0),

                name="Confidence Interval"

            )

        )

        fig.update_layout(

            title="",

            xaxis_title="Month",

            yaxis_title="Sales"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

        # ----------------------------
        # Forecast Table
        # ----------------------------

        st.subheader("Forecast Values")

        display = future_forecast.copy()

        display.columns = [

            "Forecast Month",

            "Predicted Sales",

            "Lower Bound",

            "Upper Bound"

        ]

        st.dataframe(

            display,

            use_container_width=True

        )

        # ----------------------------
        # Metrics
        # ----------------------------

        st.subheader("Model Performance")

        c1, c2 = st.columns(2)

        c1.metric(

            "MAE",

            f"{mae:,.2f}"

        )

        c2.metric(

            "RMSE",

            f"{rmse:,.2f}"

        )

        st.success(
            "Forecast generated using Facebook Prophet with automatic trend and seasonality modeling."
        )

        # ----------------------------
        # Trend & Seasonality
        # ----------------------------

        st.subheader("Trend and Seasonality")

        fig2 = final_model.plot_components(

            forecast2

        )

        st.pyplot(fig2)
        # ==========================================================
# PAGE 3 : ANOMALY REPORT
# ==========================================================

elif page == "Anomaly Report":

    st.header("🚨 Sales Anomaly Detection Report")

    # -----------------------------------------
    # Weekly Sales Aggregation
    # -----------------------------------------

    weekly_sales = (
        df.set_index("Order Date")
        .resample("W")["Sales"]
        .sum()
        .reset_index()
    )

    # -----------------------------------------
    # Isolation Forest
    # -----------------------------------------

    iso = IsolationForest(
        contamination=0.05,
        random_state=42
    )

    weekly_sales["Isolation"] = iso.fit_predict(
        weekly_sales[["Sales"]]
    )

    weekly_sales["Isolation"] = weekly_sales["Isolation"].map(
        {
            1: "Normal",
            -1: "Anomaly"
        }
    )

    # -----------------------------------------
    # Rolling Mean + Z Score
    # -----------------------------------------

    weekly_sales["Rolling Mean"] = (
        weekly_sales["Sales"]
        .rolling(4)
        .mean()
    )

    weekly_sales["Rolling Std"] = (
        weekly_sales["Sales"]
        .rolling(4)
        .std()
    )

    weekly_sales["ZScore"] = (

        weekly_sales["Sales"]

        -

        weekly_sales["Rolling Mean"]

    ) / weekly_sales["Rolling Std"]

    weekly_sales["Z Anomaly"] = (
        abs(weekly_sales["ZScore"]) > 2
    )

    # -----------------------------------------
    # KPI Cards
    # -----------------------------------------

    total = len(weekly_sales)

    iso_count = (
        weekly_sales["Isolation"] == "Anomaly"
    ).sum()

    z_count = weekly_sales["Z Anomaly"].sum()

    both = weekly_sales[
        (weekly_sales["Isolation"] == "Anomaly")
        &
        (weekly_sales["Z Anomaly"])
    ].shape[0]

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Weeks", total)

    c2.metric("Isolation Forest", iso_count)

    c3.metric("Z-Score", z_count)

    c4.metric("Common", both)

    st.divider()

    # -----------------------------------------
    # Plot
    # -----------------------------------------

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            x=weekly_sales["Order Date"],

            y=weekly_sales["Sales"],

            mode="lines",

            name="Weekly Sales"

        )

    )

    anomaly = weekly_sales[
        weekly_sales["Isolation"] == "Anomaly"
    ]

    fig.add_trace(

        go.Scatter(

            x=anomaly["Order Date"],

            y=anomaly["Sales"],

            mode="markers",

            marker=dict(
                color="red",
                size=10
            ),

            name="Isolation Forest"

        )

    )

    fig.update_layout(

        title="Weekly Sales with Detected Anomalies",

        xaxis_title="Date",

        yaxis_title="Sales"

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # -----------------------------------------
    # Isolation Forest Table
    # -----------------------------------------

    st.subheader("Isolation Forest Results")

    st.dataframe(

        anomaly[
            [
                "Order Date",
                "Sales"
            ]
        ],

        use_container_width=True

    )

    # -----------------------------------------
    # Z Score Table
    # -----------------------------------------

    st.subheader("Z-Score Results")

    ztable = weekly_sales[
        weekly_sales["Z Anomaly"]
    ][
        [
            "Order Date",
            "Sales",
            "ZScore"
        ]
    ]

    st.dataframe(
        ztable,
        use_container_width=True
    )

    # -----------------------------------------
    # Comparison
    # -----------------------------------------

    st.subheader("Method Comparison")

    compare = pd.DataFrame({

        "Method": [

            "Isolation Forest",

            "Z Score"

        ],

        "Detected": [

            iso_count,

            z_count

        ]

    })

    st.table(compare)

    # -----------------------------------------
    # Business Insights
    # -----------------------------------------

    st.subheader("Business Interpretation")

    st.info("""

• Sudden sales spikes generally indicate festive sales,
discount campaigns or product launches.

• Sudden drops may indicate inventory shortages,
logistics issues or seasonal decline.

• Isolation Forest identifies unusual patterns using
machine learning.

• Z-Score statistically detects weeks far away from
normal sales behaviour.

• If both methods flag the same week,
confidence in the anomaly is much higher.

""")

    # -----------------------------------------
    # Download CSV
    # -----------------------------------------

    csv = anomaly.to_csv(index=False)

    st.download_button(

        "📥 Download Anomaly Report",

        csv,

        "anomaly_report.csv",

        "text/csv"

    )
    # ==========================================================
# PAGE 4 : DEMAND SEGMENTS
# ==========================================================

elif page == "Demand Segments":

    st.header("📦 Product Demand Segmentation")

    monthly = df.copy()

    monthly["YearMonth"] = (
        monthly["Order Date"]
        .dt.to_period("M")
        .astype(str)
    )

    monthly_sales = (
        monthly
        .groupby(["Sub-Category", "YearMonth"])["Sales"]
        .sum()
        .reset_index()
    )

    # ---------------------------------------
    # Feature Engineering
    # ---------------------------------------

    feature_df = (
        monthly_sales
        .groupby("Sub-Category")
        .agg(
            Total_Sales=("Sales", "sum"),
            Avg_Monthly_Sales=("Sales", "mean"),
            Sales_Volatility=("Sales", "std")
        )
        .fillna(0)
        .reset_index()
    )

    avg_order = (
        df.groupby("Sub-Category")["Sales"]
        .mean()
        .reset_index(name="Average_Order_Value")
    )

    feature_df = feature_df.merge(
        avg_order,
        on="Sub-Category"
    )

    growth = (
        monthly_sales
        .groupby("Sub-Category")
        .apply(
            lambda x: (
                (x["Sales"].iloc[-1] - x["Sales"].iloc[0]) /
                max(x["Sales"].iloc[0], 1)
            )
        )
        .reset_index(name="Growth_Rate")
    )

    feature_df = feature_df.merge(
        growth,
        on="Sub-Category"
    )

    X = feature_df.drop(columns=["Sub-Category"])

    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X)

    # ---------------------------------------
    # Elbow Method
    # ---------------------------------------

    inertia = []

    for k in range(2, 8):

        km = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=10
        )

        km.fit(X_scaled)

        inertia.append(km.inertia_)

    elbow = px.line(

        x=list(range(2, 8)),
        y=inertia,
        markers=True,
        labels={
            "x": "Clusters",
            "y": "Inertia"
        },
        title="Elbow Method"
    )

    st.plotly_chart(
        elbow,
        use_container_width=True
    )

    # ---------------------------------------
    # Final Model
    # ---------------------------------------

    kmeans = KMeans(
        n_clusters=4,
        random_state=42,
        n_init=10
    )

    feature_df["Cluster"] = kmeans.fit_predict(
        X_scaled
    )

    labels = {
        0: "High Volume",
        1: "Growing Demand",
        2: "Stable Demand",
        3: "Low Volume"
    }

    feature_df["Demand Segment"] = (
        feature_df["Cluster"].map(labels)
    )

    # ---------------------------------------
    # PCA
    # ---------------------------------------

    pca = PCA(n_components=2)

    comp = pca.fit_transform(X_scaled)

    feature_df["PC1"] = comp[:, 0]
    feature_df["PC2"] = comp[:, 1]

    fig = px.scatter(

        feature_df,

        x="PC1",

        y="PC2",

        color="Demand Segment",

        hover_name="Sub-Category",

        size="Total_Sales",

        title="Demand Clusters (PCA)"

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ---------------------------------------
    # Cluster Counts
    # ---------------------------------------

    st.subheader("Cluster Summary")

    cluster_summary = (
        feature_df["Demand Segment"]
        .value_counts()
        .reset_index()
    )

    cluster_summary.columns = [
        "Demand Segment",
        "Products"
    ]

    st.dataframe(
        cluster_summary,
        use_container_width=True
    )

    # ---------------------------------------
    # Product Table
    # ---------------------------------------

    st.subheader("Sub Category Mapping")

    st.dataframe(

        feature_df[

            [
                "Sub-Category",
                "Demand Segment",
                "Total_Sales",
                "Growth_Rate"
            ]

        ],

        use_container_width=True

    )

    # ---------------------------------------
    # Strategy
    # ---------------------------------------

    st.subheader("Recommended Stocking Strategy")

    strategy = pd.DataFrame({

        "Demand Segment":[

            "High Volume",

            "Growing Demand",

            "Stable Demand",

            "Low Volume"

        ],

        "Business Recommendation":[

            "Maintain high inventory and replenish frequently.",

            "Increase inventory gradually to capture demand.",

            "Maintain normal inventory with periodic review.",

            "Reduce inventory and avoid overstock."

        ]

    })

    st.table(strategy)

    # ---------------------------------------
    # Download Report
    # ---------------------------------------

    csv = feature_df.to_csv(index=False)

    st.download_button(

        "📥 Download Cluster Report",

        csv,

        "product_clusters.csv",

        "text/csv"

    )

    st.success(
        "Products have been segmented using K-Means clustering. "
        "The Elbow Method was used to determine a suitable number of clusters, "
        "and PCA was applied for visualization."
    )