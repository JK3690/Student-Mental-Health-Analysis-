from database import run_query
def risk_classification():
    query_total = "SELECT COUNT(*) FROM student_mental_health WHERE Depression='Yes' OR Anxiety='Yes' OR Panic_attack='Yes';"
    total = run_query(query_total, fetch=True)[0][0]

    query_help = "SELECT COUNT(*) FROM student_mental_health WHERE (Depression='Yes' OR Anxiety='Yes' OR Panic_attack='Yes') AND Specialist_seeked='Yes';"
    helped = run_query(query_help, fetch=True)[0][0]

    if total == 0:
        print("No at-risk students found")
    else:
        percent = (helped / total) * 100
    return total, helped, percent

total, helped, percent = risk_classification()
print(total, helped, percent)
import streamlit as st
import matplotlib.pyplot as plt

st.title("Student Mental Health Insights Dashboard")

st.subheader("Overview")
st.write(f"Total students with mental health issues: {total}")
st.write(f"Students who sought help: {helped}")
st.write(f"Help-seeking rate: {percent:.2f}%")

option = st.selectbox("Select Mental Health Indicator", ["Depression", "Anxiety", "Panic_attack"])
query = f"SELECT {option}, COUNT(*) FROM table GROUP BY {option};"
result = run_query(query, fetch=True)[0][0]
st.write(f"{result} students reported {option}")

fig, ax = plt.subplots()
ax.bar(["Yes"], [result])
ax.set_title(f"{option} Prevalence Among Students")

st.pyplot(fig)

field = st.selectbox("Compare by", ["Gender", "Course", "Year"])
query = f"""SELECT {field}, COUNT(*) FROM student_mental_health WHERE {option}='Yes' GROUP BY {field};"""
result = run_query(query, fetch=True)

labels = [row[0] for row in result]
counts = [row[1] for row in result]

fig, ax = plt.subplots()
ax.bar(labels, counts)
ax.set_title(f"{option} by {field}")

st.pyplot(fig)

st.subheader("Key Insight")
st.write(f"Only {percent:.2f}% of students with mental health issues seek professional help")

col1, col2 = st.columns(2)
with col1:
    st.write(f"Total: {total}")
with col2:
    st.write(f"Helped: {helped}")