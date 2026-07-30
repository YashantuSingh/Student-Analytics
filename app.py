import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Student Analytics Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    /* Main App */
    .main {
        background-color: #f5f7fb;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #111827;
    }

    section[data-testid="stSidebar"] * {
        color: white;
    }

    /* Main Header */
    .main-header {
        font-size: 36px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .sub-header {
        font-size: 16px;
        color: #6b7280;
        margin-bottom: 25px;
    }

    /* KPI Cards */
    .kpi-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        border-left: 5px solid #2563eb;
    }

    .kpi-title {
        font-size: 14px;
        color: #6b7280;
    }

    .kpi-value {
        font-size: 30px;
        font-weight: 700;
        color: #111827;
    }

    /* Section */
    .section-title {
        font-size: 22px;
        font-weight: 600;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #6b7280;
        padding: 30px;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# DATA LOADING
# ============================================================

@st.cache_data
def load_data():

    file_path = Path("master_dataset.xlsx")

    if not file_path.exists():
        return None

    try:
        return pd.read_excel(file_path)
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return None


df = load_data()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-header">🎓 Student Analytics Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-header">Interactive student performance, attendance, fee and risk analytics</div>',
    unsafe_allow_html=True
)


# ============================================================
# DATA CHECK
# ============================================================

if df is None:

    st.error(
        "❌ master_dataset.xlsx was not found. "
        "Please make sure it is in the same folder as app.py."
    )

    st.stop()


if df.empty:

    st.warning("The dataset is empty.")

    st.stop()


# ============================================================
# COLUMN DETECTION
# ============================================================

def find_column(possible_names):

    for col in df.columns:

        clean_col = str(col).lower().replace("_", " ").strip()

        for name in possible_names:

            if name.lower() in clean_col:
                return col

    return None


student_col = find_column([
    "student id",
    "student name",
    "enrollment no",
    "enrollment number",
    "student"
])

course_col = find_column([
    "course",
    "program",
    "department"
])

mentor_col = find_column([
    "mentor",
    "teacher",
    "faculty"
])

attendance_col = find_column([
    "attendance"
])

marks_col = find_column([
    "total marks",
    "marks",
    "score",
    "percentage"
])

fee_col = find_column([
    "fee",
    "fees",
    "fee collection"
])

risk_col = find_column([
    "risk",
    "at risk"
])


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🎓 Student Analytics")

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "👨‍🎓 Student Analysis",
        "📚 Academic Performance",
        "📅 Attendance Analysis",
        "💰 Fee Collection",
        "⚠️ Risk Analysis",
        "👨‍🏫 Mentor Analysis",
        "🤖 ML Prediction"
    ]
)

st.sidebar.markdown("---")

st.sidebar.subheader("🔍 Filters")


# ============================================================
# FILTERS
# ============================================================

filtered_df = df.copy()


if course_col:

    courses = ["All"] + sorted(
        df[course_col].dropna().astype(str).unique().tolist()
    )

    selected_course = st.sidebar.selectbox(
        "Course",
        courses
    )

    if selected_course != "All":

        filtered_df = filtered_df[
            filtered_df[course_col].astype(str) == selected_course
        ]


if mentor_col:

    mentors = ["All"] + sorted(
        df[mentor_col].dropna().astype(str).unique().tolist()
    )

    selected_mentor = st.sidebar.selectbox(
        "Mentor",
        mentors
    )

    if selected_mentor != "All":

        filtered_df = filtered_df[
            filtered_df[mentor_col].astype(str) == selected_mentor
        ]


if risk_col:

    risks = ["All"] + sorted(
        df[risk_col].dropna().astype(str).unique().tolist()
    )

    selected_risk = st.sidebar.selectbox(
        "Risk Level",
        risks
    )

    if selected_risk != "All":

        filtered_df = filtered_df[
            filtered_df[risk_col].astype(str) == selected_risk
        ]


st.sidebar.markdown("---")

st.sidebar.info(
    f"Showing {len(filtered_df):,} of {len(df):,} students"
)


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_students = len(filtered_df)


if attendance_col:

    avg_attendance = pd.to_numeric(
        filtered_df[attendance_col],
        errors="coerce"
    ).mean()

else:

    avg_attendance = 0


if marks_col:

    avg_marks = pd.to_numeric(
        filtered_df[marks_col],
        errors="coerce"
    ).mean()

else:

    avg_marks = 0


if risk_col:

    risk_count = filtered_df[risk_col].astype(str).str.lower().isin(
        ["1", "yes", "high", "at risk", "risk"]
    ).sum()

else:

    risk_count = 0


# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    st.markdown(
        '<div class="section-title">📊 Key Performance Indicators</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "👨‍🎓 Total Students",
            f"{total_students:,}"
        )

    with col2:

        st.metric(
            "📅 Avg Attendance",
            f"{avg_attendance:.1f}%"
        )

    with col3:

        st.metric(
            "📚 Avg Marks",
            f"{avg_marks:.1f}"
        )

    with col4:

        st.metric(
            "⚠️ At-Risk Students",
            f"{risk_count:,}"
        )


    st.markdown(
        '<div class="section-title">📈 Analytics Overview</div>',
        unsafe_allow_html=True
    )


    col1, col2 = st.columns(2)


    # Course Chart

    with col1:

        if course_col:

            course_data = (
                filtered_df[course_col]
                .astype(str)
                .value_counts()
                .reset_index()
            )

            course_data.columns = [
                "Course",
                "Students"
            ]

            fig = px.bar(
                course_data,
                x="Course",
                y="Students",
                title="👨‍🎓 Students by Course"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


    # Attendance Chart

    with col2:

        if attendance_col:

            attendance_data = pd.to_numeric(
                filtered_df[attendance_col],
                errors="coerce"
            ).dropna()

            fig = px.histogram(
                attendance_data,
                x=attendance_data,
                nbins=10,
                title="📅 Attendance Distribution"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


    col1, col2 = st.columns(2)


    # Marks Chart

    with col1:

        if marks_col:

            marks_data = pd.to_numeric(
                filtered_df[marks_col],
                errors="coerce"
            ).dropna()

            fig = px.histogram(
                marks_data,
                x=marks_data,
                nbins=10,
                title="📚 Marks Distribution"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


    # Risk Chart

    with col2:

        if risk_col:

            risk_data = (
                filtered_df[risk_col]
                .astype(str)
                .value_counts()
                .reset_index()
            )

            risk_data.columns = [
                "Risk",
                "Students"
            ]

            fig = px.pie(
                risk_data,
                names="Risk",
                values="Students",
                title="⚠️ Student Risk Distribution"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


# ============================================================
# STUDENT ANALYSIS
# ============================================================

elif page == "👨‍🎓 Student Analysis":

    st.title("👨‍🎓 Student Analysis")

    st.write(
        "Explore detailed information about individual students."
    )

    search = st.text_input(
        "🔍 Search Student"
    )

    display_df = filtered_df.copy()

    if search:

        display_df = display_df[
            display_df.astype(str)
            .apply(
                lambda row: row.str.contains(
                    search,
                    case=False,
                    na=False
                ).any(),
                axis=1
            )
        ]

    st.dataframe(
        display_df,
        use_container_width=True,
        height=500
    )


    st.download_button(
        "📥 Download Filtered Data",
        display_df.to_csv(index=False),
        "student_analysis.csv",
        "text/csv"
    )


# ============================================================
# ACADEMIC PERFORMANCE
# ============================================================

elif page == "📚 Academic Performance":

    st.title("📚 Academic Performance")

    if marks_col:

        if course_col:

            performance = (
                filtered_df
                .groupby(course_col)[marks_col]
                .mean()
                .reset_index()
            )

            performance.columns = [
                "Course",
                "Average Marks"
            ]

            fig = px.bar(
                performance,
                x="Course",
                y="Average Marks",
                title="Average Marks by Course"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


        st.subheader("📊 Marks Statistics")

        st.dataframe(
            filtered_df[marks_col]
            .describe()
            .to_frame(),
            use_container_width=True
        )

    else:

        st.warning(
            "Marks column was not detected."
        )


# ============================================================
# ATTENDANCE
# ============================================================

elif page == "📅 Attendance Analysis":

    st.title("📅 Attendance Analysis")

    if attendance_col:

        attendance_data = pd.to_numeric(
            filtered_df[attendance_col],
            errors="coerce"
        ).dropna()


        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "Average Attendance",
                f"{attendance_data.mean():.1f}%"
            )


        with col2:

            st.metric(
                "Highest Attendance",
                f"{attendance_data.max():.1f}%"
            )


        with col3:

            st.metric(
                "Lowest Attendance",
                f"{attendance_data.min():.1f}%"
            )


        fig = px.histogram(
            attendance_data,
            x=attendance_data,
            nbins=20,
            title="Attendance Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


        low_attendance = filtered_df[
            pd.to_numeric(
                filtered_df[attendance_col],
                errors="coerce"
            ) < 75
        ]

        st.subheader("⚠️ Students Below 75% Attendance")

        st.dataframe(
            low_attendance,
            use_container_width=True
        )

    else:

        st.warning(
            "Attendance column was not detected."
        )


# ============================================================
# FEE COLLECTION
# ============================================================

elif page == "💰 Fee Collection":

    st.title("💰 Fee Collection Analysis")

    if fee_col:

        fee_data = filtered_df[fee_col].astype(str)

        fee_summary = (
            fee_data
            .value_counts()
            .reset_index()
        )

        fee_summary.columns = [
            "Fee Status",
            "Students"
        ]


        fig = px.pie(
            fee_summary,
            names="Fee Status",
            values="Students",
            title="Fee Collection Status"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


        st.dataframe(
            fee_summary,
            use_container_width=True
        )

    else:

        st.warning(
            "Fee column was not detected."
        )


# ============================================================
# RISK ANALYSIS
# ============================================================

elif page == "⚠️ Risk Analysis":

    st.title("⚠️ Student Risk Analysis")

    if risk_col:

        risk_summary = (
            filtered_df[risk_col]
            .astype(str)
            .value_counts()
            .reset_index()
        )

        risk_summary.columns = [
            "Risk Level",
            "Students"
        ]


        fig = px.bar(
            risk_summary,
            x="Risk Level",
            y="Students",
            title="Students by Risk Level"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


        st.subheader("🚨 At-Risk Students")


        at_risk = filtered_df[
            filtered_df[risk_col]
            .astype(str)
            .str.lower()
            .isin(
                [
                    "1",
                    "yes",
                    "high",
                    "at risk",
                    "risk"
                ]
            )
        ]


        st.dataframe(
            at_risk,
            use_container_width=True
        )

    else:

        st.warning(
            "Risk column was not detected."
        )


# ============================================================
# MENTOR ANALYSIS
# ============================================================

elif page == "👨‍🏫 Mentor Analysis":

    st.title("👨‍🏫 Mentor Performance Analysis")

    if mentor_col:

        mentor_count = (
            filtered_df[mentor_col]
            .astype(str)
            .value_counts()
            .reset_index()
        )

        mentor_count.columns = [
            "Mentor",
            "Students"
        ]


        fig = px.bar(
            mentor_count,
            x="Mentor",
            y="Students",
            title="Students by Mentor"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


        st.dataframe(
            mentor_count,
            use_container_width=True
        )

    else:

        st.warning(
            "Mentor column was not detected."
        )


# ============================================================
# MACHINE LEARNING
# ============================================================

elif page == "🤖 ML Prediction":

    st.title("🤖 Machine Learning Prediction")

    st.info(
        "This section is prepared for integration with your "
        "3-model machine learning pipeline."
    )


    st.subheader("🧠 Available Models")


    col1, col2, col3 = st.columns(3)


    with col1:

        st.markdown(
            "### Logistic Regression"
        )

        st.write(
            "Classification model for predicting student risk."
        )


    with col2:

        st.markdown(
            "### Random Forest"
        )

        st.write(
            "Ensemble model for robust student classification."
        )


    with col3:

        st.markdown(
            "### Gradient Boosting"
        )

        st.write(
            "Boosting-based classification model."
        )


    st.markdown("---")


    st.subheader(
        "🎯 Student Risk Prediction"
    )


    col1, col2 = st.columns(2)


    with col1:

        attendance_input = st.number_input(
            "Attendance (%)",
            min_value=0.0,
            max_value=100.0,
            value=75.0
        )


        marks_input = st.number_input(
            "Marks",
            min_value=0.0,
            max_value=100.0,
            value=50.0
        )


    with col2:

        fee_status = st.selectbox(
            "Fee Status",
            [
                "Paid",
                "Pending"
            ]
        )


        model_choice = st.selectbox(
            "Select Model",
            [
                "Logistic Regression",
                "Random Forest",
                "Gradient Boosting"
            ]
        )


    if st.button(
        "🔮 Predict Student Risk",
        use_container_width=True
    ):

        if attendance_input < 60 or marks_input < 40:

            prediction = "🔴 High Risk"

        elif attendance_input < 75 or marks_input < 60:

            prediction = "🟡 Medium Risk"

        else:

            prediction = "🟢 Low Risk"


        st.success(
            f"Prediction using {model_choice}: {prediction}"
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    '<div class="footer">'
    '🎓 Student Analytics Dashboard | '
    'Built with Streamlit, Python & Machine Learning'
    '</div>',
    unsafe_allow_html=True
)