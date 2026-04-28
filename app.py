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

#--IMPORT--
import streamlit as st
import plotly.express as px

#--PAGE SETUP--
st.set_page_config(page_title="Student Mental Health Dashboard", layout="wide")
st.title("Student Mental Health Insights Dashboard")
st.caption("Analyze patterns in student mental health and help-seeking behavior")
st.info("Interactive dashboard to analyze student mental health trends and support gaps")

st.markdown("<br>", unsafe_allow_html=True)
st.sidebar.header("Filters") #moves controls to left panel
st.sidebar.divider()
option = st.sidebar.selectbox("Select Mental Health Indicator", ["Depression", "Anxiety", "Panic_attack"])
field = st.sidebar.selectbox("Compare by", ["Gender", "Course", "Year"])
tab1, tab2 = st.tabs(["Overview", "Detailed Analysis"])

with tab1:
    #--KPI ROW--
    st.subheader("Help-Seeking Behavior") #section titles
    col1, col2, col3 = st.columns(3) #vertically split screen layout
    with col1:
        st.metric("Total At Risk", total)
    with col2:
        st.metric("Sought Help", helped)
    with col3:
        st.metric("Help Rate (%)", f"{percent:.2f}")
        if percent < 30:
            insight = "A significant gap exists between students experiencing issues and those seeking help."
        else:
            insight = "A relatively higher proportion of students are seeking help."   
    st.info(insight)
    st.divider()
    st.subheader("Top Affected Group")
    query = f"SELECT {field}, COUNT(*) FROM student_mental_health WHERE {option}='Yes' GROUP BY {field} ORDER BY COUNT(*) DESC LIMIT 1;"
    result = run_query(query, fetch=True)
    if field == 'Year':
        st.write(f"Year {result} students have the highest {option} cases.")
    else:
        st.write(f"{result} students have the highest {option} cases.")
    
with tab2:
    col1, col2 = st.columns(2)
    with col1:
        #pie chart
        st.subheader(f"{option} Distribution")
        query = f"SELECT {option}, COUNT(*) FROM student_mental_health GROUP BY {option};"
        result = run_query(query, params=(), fetch=True)
        labels = [value[0] for value in result]
        counts = [value[1] for value in result]
        fig_pie= px.pie(names=labels, values=counts, title=f"{option} Distribution", 
        color_discrete_sequence=["#111d4a", "#476a6f"])
        fig_pie.update_layout(title=f"{option} Distribution", title_x=0.2, uniformtext_minsize=8, uniformtext_mode='hide')
        st.plotly_chart(fig_pie, width='stretch')
        
    with col2: 
    #bar chart
        query = f"SELECT {field}, COUNT(*) FROM student_mental_health WHERE {option}='Yes' GROUP BY {field} ORDER BY COUNT(*) DESC;"
        result = run_query(query, fetch=True)
        
        labels = [row[0] for row in result]
        labels = [str(l).strip() for l in labels]
        counts = [row[1] for row in result]
        fig_bar = px.bar(x=counts, y=labels, orientation='h', title=f"{option} by {field}", color_discrete_sequence=["#7e849b"])
        fig_bar.update_layout(title=f"{option} Distribution by {field}",title_x=0.2,  xaxis_title="Number of Students", showlegend=False, yaxis_title=f"{field}", uniformtext_minsize=8, uniformtext_mode='hide')
        fig_bar.update_traces(texttemplate='%{x}', textposition='outside', hovertemplate="Count: %{y}<extra></extra>")
        st.plotly_chart(fig_bar, width='stretch')
#streamlit run app.py
