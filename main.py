import streamlit as st
import streamlit.components.v1 as components
import time

# Page Configuration
st.set_page_config(
    page_title="CGPA Calculator for KARE Students",
    page_icon="👑",
    layout="centered",
    initial_sidebar_state="auto",
)

# Session State Initialization
if "ad_verified" not in st.session_state:
    st.session_state.ad_verified = False
if "button_clicked_time" not in st.session_state:
    st.session_state.button_clicked_time = None

# Show Ad Prompt
if not st.session_state.ad_verified:
    st.title("👑 CGPA Calculator for KARE Students")
    st.markdown("Please click the ad below and wait **3 seconds** to access the calculator.")

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
        st.session_state.button_clicked_time = time.time()

    # Check if 3 seconds have passed
    if st.session_state.button_clicked_time:
        elapsed = time.time() - st.session_state.button_clicked_time
        if elapsed >= 3:
            st.session_state.ad_verified = True
        else:
            with st.spinner(f"Verifying... Please wait {int(3 - elapsed)} more second(s)"):
                time.sleep(3 - elapsed)
            st.session_state.ad_verified = True

# If ad is verified, show calculator
if st.session_state.ad_verified:

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
        total_grade = sum(
            grade_point * credit for grade_point, credit in zip(grade_points, credits)
        ) + (previous_cgpa * previous_credit)
        return total_grade / total_credit

    st.title("🎓 CGPA Calculator for KARE Students")
    st.markdown("This calculator helps you compute your semester and cumulative CGPA.")
    st.latex(r"CGPA = \frac{\sum_{i=1}^{n} (grade_i * credit_i)}{\sum_{i=1}^{n} credit_i}")

    cols = st.columns(2)
    previous_cgpa = cols[0].number_input(
        "Previous CGPA",
        help="Enter your cumulative CGPA up to the previous semester",
        min_value=0.00,
        value=0.00,
        step=0.01,
    )
    previous_credit = cols[1].number_input(
        "Previous Credits",
        help="Enter total credits completed until the previous semester",
        min_value=0.0,
        value=0.0,
        step=0.5,
    ).__int__()

    number_of_subjects = st.number_input(
        "Number of Subjects this Semester",
        min_value=1,
        max_value=10,
        value=5,
        step=1,
    ).__int__()

    grade = [grades[0]] * number_of_subjects
    credit = [0.0] * number_of_subjects

    for i in range(number_of_subjects):
        st.subheader(f"Subject {i+1}")
        cols = st.columns(2)
        grade[i] = cols[0].selectbox(
            f"Grade for Subject {i+1}",
            options=grades,
            index=0,
            key=f"grade_{i}",
        )
        credit[i] = cols[1].number_input(
            f"Credit for Subject {i+1}",
            min_value=1.0,
            max_value=10.0,
            value=4.0,
            step=0.5,
            key=f"credit_{i}",
        )

    if st.button("Calculate"):
        grade_points = [grade_to_point[x] for x in grade]
        sem_gpa = calculate_cgpa(grade_points, credit)
        final_cgpa = calculate_cgpa(grade_points, credit, previous_cgpa, previous_credit)
        st.info(f"📊 Semester GPA: **{sem_gpa:.2f}**")
        st.success(f"🎯 Cumulative GPA: **{final_cgpa:.2f}**")

    st.markdown("Made with ❤️ by [RDMCODER](https://github.com/rdmcoder123) — ONLY FOR KARE Students")
