import csv
import mysql.connector as m
filename = "Student Mental health.csv"
config = {'user': 'root', 'password': 'Jess@2009', 'host': 'localhost','database': 'project'}

#defining helper functions
def convert(filename, **config):
  con = m.connect(**config)
  cursor = con.cursor()
  with open(filename, 'r') as file:
    reader = csv.reader(file)
    headers = next(reader)
    headers = [h.strip() for h in headers]
    columns = []
    for header in headers:
        if header in ["Age", "Year"]:
            columns.append(f"{header} INT")
        elif header == "CGPA":
            columns.append(f"{header} FLOAT")
        else:
            columns.append(f"{header} VARCHAR(255)")
    columns = ', '.join(columns)

    create_table_query = f"CREATE TABLE IF NOT EXISTS student_mental_health ({columns});"
    cursor.execute(create_table_query)
    insert_query = f"INSERT INTO student_mental_health ({', '.join(headers)}) VALUES ({', '.join(['%s']*len(headers))});"
    for row in reader:
        cursor.execute(insert_query, row)
    con.commit()
    cursor.close()
    con.close()

def run_query(query, params=(), fetch=False):
    con = m.connect(**config)
    cur = con.cursor()
    cur.execute(query, params)
    data = cur.fetchall() if fetch else None
    con.commit()
    cur.close()
    con.close()
    return data

def clean_input(s):
    return input(s).strip().capitalize()

def cgpa_clean(cgpa):
    cgpa_val = [(0,1.99,"0-1.99"), (2,2.49,"2-2.49"), (2.5,2.99,"2.50-2.99"), (3,3.49,"3-3.49"), (3.5,4,"3.50-4")]
    for low, high, label in cgpa_val:
        if low <= cgpa <= high:
            return label

        
def insights():
    mhi = clean_input("Enter mental health issue: ")
    valid_cols = ["Depression", "Anxiety", "Panic_attack"]
    if mhi not in valid_cols:
        print("Invalid input")
        return
    query = f"SELECT AVG(Age) FROM student_mental_health WHERE {mhi} = %s"
    result = run_query(query, ("Yes",), True)
    print(f"Students with {mhi} have an average age of {result[0][0]} years")
    query = f"SELECT COUNT(*) FROM student_mental_health WHERE {mhi} = %s"
    result1 = run_query(query, ("Yes",), True)
    print(f" {result1[0][0]} students reported {mhi}")

    def risk_classification():
        query_total = """SELECT COUNT(*) FROM student_mental_health WHERE Depression='Yes' OR Anxiety='Yes' OR Panic_attack='Yes';"""
        total = run_query(query_total, fetch=True)[0][0]
        print(f"{total} students have mental health issues")
        
        def help_gap():
            # those who sought help
            query_help = """
            SELECT COUNT(*) FROM student_mental_health
            WHERE (Depression='Yes' OR Anxiety='Yes' OR Panic_attack='Yes') AND Specialist_seeked='Yes';"""
            helped = run_query(query_help, fetch=True)[0][0]

            if total == 0:
                print("No at-risk students found")
            else:
                percent = (helped / total) * 100
            print(f"Only {percent:.2f}% ({helped}) of students with mental health issues seek professional help")
            
        help_gap()
    risk_classification()
    
