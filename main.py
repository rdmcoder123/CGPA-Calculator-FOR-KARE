import streamlit as st
import streamlit.components.v1 as components
import time

# Page configuration
st.set_page_config(
    page_title="CGPA Calculator for KARE Students",
    page_icon="👑",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items={
        "Get Help": "https://github.com/rdmcoder123",
        "Report a bug": "https://github.com/rdmcoder123",
        "About": None,
    },
)

# Simulated Ad Click Gate
if "ad_verified" not in st.session_state:
    st.session_state.ad_verified = False

if not st.session_state.ad_verified:
    st.title("👑 CGPA Calculator for KARE Students")
    st.markdown("Click the ad below and wait **3 seconds** to continue...")

    components.html(
        """
        <div style="text-align:center;">
            <script type="text/javascript">
                atOptions = {
                    'key': 'c7f8b088d3044e1b7bc0577d4e950f21',
                    'format': 'iframe',
                    'height': 250,
                    'width': 300,
                    'params': {}
                };
            </script>
            <script type="text/javascript" src="//www.highperformanceformat.com/c7f8b088d3044e1b7bc0577d4e950f21/invoke.js"></script>
        </div>
        """,
        height=300,
    )

    if st.button("✅ I Clicked the Ad"):
        st.session_state.show_spinner = True
        st.rerun()

# After clicking the ad and rerun
if st.session_state.get("show_spinner", False):
    with st.spinner("Verifying your click... Please wait 3 seconds"):
        time.sleep(3)
    st.session_state.ad_verified = True
    st.session_state.show_spinner = False
    st.rerun()

# ---- CGPA Calculator Section ----
grade_to_point = {
    "S": 10,
    "A": 9,
    "B": 8,
    "C": 7,
    "D": 6,
    "E": 5,
}
grades = list(grade_to_point.keys())

def calculate_cgpa(
    grade_points: list[int],
    credits: list[float],
    previous_cgpa: float = 0,
    previous_credit: float = 0,
):
    total_credit = sum(credits) + previous_credit
    total_grade = sum(grade_point * credit for grade_point, credit in zip(grade_points, credits)) + (previous_cgpa * previous_credit)
    return total_grade / total_credit

st.title("🎓 CGPA Calculator for KARE Students")

st.markdown(
    "This is a simple CGPA calculator that calculates your CGPA based on your grades and credits"
)
st.latex(r"CGPA = \frac{\sum_{i=1}^{n} (grade_i * credit_i)}{\sum_{i=1}^{n} credit_i}")

cols = st.columns(2)
previous_cgpa = cols[0].number_input(
    label="Previous CGPA",
    help="Enter Your CGPA up to previous semester",
    min_value=0.00,
    value=0.00,
    step=0.01,
)
previous_credit = cols[1].number_input(
    label="Previous Credit",
    help="Enter the total number of credits you have taken up to previous semester",
    min_value=0.0,
    value=0.0,
    step=0.5,
).__int__()

number_of_subjects = st.number_input(
    label="Number of Subjects",
    help="Enter the number of subjects you are taking this semester",
    min_value=1,
    max_value=10,
    value=5,
).__int__()

grade = [grades[0]] * number_of_subjects
credit = [0.0] * number_of_subjects

for i in range(number_of_subjects):
    st.subheader(f"Subject → {i+1}")
    cols = st.columns(2)
    grade[i] = cols[0].selectbox(
        label=f"Grade",
        options=grades,
        key=f"grade_{i}",
        index=0,
    ).__str__()

    credit[i] = cols[1].number_input(
        label=f"Credit",
        min_value=1.0,
        max_value=10.0,
        value=4.0,
        step=0.5,
        key=f"credit_{i}",
    )

if st.button("Calculate"):
    grade_points = [grade_to_point[x] for x in grade]
    st.info(f"📊 Your Semester GPA is **{calculate_cgpa(grade_points, credit):.2f}**")
    st.success(
        f"🎯 Your Cumulative GPA is **{calculate_cgpa(grade_points, credit, previous_cgpa, previous_credit):.2f}**"
    )

st.markdown("Made with ❤️ by [RDMCODER](https://github.com/rdmcoder123) — ONLY FOR KARE Students")
