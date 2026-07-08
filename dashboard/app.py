import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="Employee Attrition Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Employee Attrition Analytics Dashboard")

st.markdown("""
This dashboard analyzes employee attrition using the IBM HR Analytics dataset.
Use the filters on the left to explore employee demographics, salary distribution,
department-wise attrition, and overtime patterns.
""")


@st.cache_data
def load_employee_data():
    """Load the HR employee attrition dataset."""
    return pd.read_csv("../data/WA_Fn-UseC_-HR-Employee-Attrition.csv")


df = load_employee_data()


# Sidebar filters
st.sidebar.header("Filter the Data")

selected_departments = st.sidebar.multiselect(
    "Department",
    options=sorted(df["Department"].unique()),
    default=sorted(df["Department"].unique())
)

selected_genders = st.sidebar.multiselect(
    "Gender",
    options=sorted(df["Gender"].unique()),
    default=sorted(df["Gender"].unique())
)

selected_attrition = st.sidebar.multiselect(
    "Attrition Status",
    options=sorted(df["Attrition"].unique()),
    default=sorted(df["Attrition"].unique())
)


filtered_df = df[
    (df["Department"].isin(selected_departments)) &
    (df["Gender"].isin(selected_genders)) &
    (df["Attrition"].isin(selected_attrition))
]


# KPI Cards
total_employees = len(filtered_df)

attrition_rate = (
    filtered_df["Attrition"]
    .value_counts(normalize=True)
    .get("Yes", 0) * 100
)

average_age = filtered_df["Age"].mean()
average_income = filtered_df["MonthlyIncome"].mean()

metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

metric_col1.metric("Total Employees", total_employees)
metric_col2.metric("Attrition Rate", f"{attrition_rate:.2f}%")
metric_col3.metric("Average Age", f"{average_age:.2f} Years")
metric_col4.metric("Average Monthly Income", f"${average_income:,.2f}")

st.divider()


# Age and income overview
col1, col2 = st.columns(2)

with col1:
    age_chart = px.histogram(
        filtered_df,
        x="Age",
        nbins=20,
        title="Age Distribution"
    )
    st.plotly_chart(age_chart, use_container_width=True)

with col2:
    income_chart = px.histogram(
        filtered_df,
        x="MonthlyIncome",
        nbins=25,
        title="Monthly Income Distribution"
    )
    st.plotly_chart(income_chart, use_container_width=True)


# Employee distribution
col1, col2 = st.columns(2)

with col1:
    department_summary = (
        filtered_df["Department"]
        .value_counts()
        .reset_index()
    )
    department_summary.columns = ["Department", "Employees"]

    department_chart = px.bar(
        department_summary,
        x="Department",
        y="Employees",
        color="Department",
        title="Employees by Department"
    )
    st.plotly_chart(department_chart, use_container_width=True)

with col2:
    role_summary = (
        filtered_df["JobRole"]
        .value_counts()
        .reset_index()
    )
    role_summary.columns = ["Job Role", "Employees"]

    role_chart = px.bar(
        role_summary,
        x="Employees",
        y="Job Role",
        orientation="h",
        title="Employees by Job Role"
    )
    st.plotly_chart(role_chart, use_container_width=True)


# Attrition insights
col1, col2 = st.columns(2)

with col1:
    attrition_department_chart = px.histogram(
        filtered_df,
        x="Department",
        color="Attrition",
        barmode="group",
        title="Attrition by Department"
    )
    st.plotly_chart(attrition_department_chart, use_container_width=True)

with col2:
    attrition_gender_chart = px.histogram(
        filtered_df,
        x="Gender",
        color="Attrition",
        barmode="group",
        title="Attrition by Gender"
    )
    st.plotly_chart(attrition_gender_chart, use_container_width=True)


col1, col2 = st.columns(2)

with col1:
    job_role_attrition_chart = px.histogram(
        filtered_df,
        y="JobRole",
        color="Attrition",
        barmode="group",
        title="Job Role Distribution by Attrition"
    )
    st.plotly_chart(job_role_attrition_chart, use_container_width=True)

with col2:
    overtime_chart = px.histogram(
        filtered_df,
        x="OverTime",
        color="Attrition",
        barmode="group",
        title="Overtime vs Attrition"
    )
    st.plotly_chart(overtime_chart, use_container_width=True)


# Income and age differences by attrition
col1, col2 = st.columns(2)

with col1:
    income_attrition_chart = px.box(
        filtered_df,
        x="Attrition",
        y="MonthlyIncome",
        color="Attrition",
        title="Monthly Income by Attrition Status"
    )
    st.plotly_chart(income_attrition_chart, use_container_width=True)

with col2:
    age_attrition_chart = px.box(
        filtered_df,
        x="Attrition",
        y="Age",
        color="Attrition",
        title="Age by Attrition Status"
    )
    st.plotly_chart(age_attrition_chart, use_container_width=True)


st.divider()

st.subheader("Filtered Dataset")
st.dataframe(filtered_df, use_container_width=True)

st.caption("Created by Kaustubh Valanjuwani | CodeAlpha Data Analytics Internship")