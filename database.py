import csv
import mysql.connector as m
filename = "Student Mental health.csv"
config = {'user': 'root', 'password': 'yourpassword', 'host': 'localhost','database': 'project'}
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
        
def avg_w_mhi():
    mhi = clean_input("Enter mental health issue: ")
    result = run_query(f"SELECT AVG(Age) FROM student_mental_health WHERE {mhi}='Yes';",
        fetch=True)
   if result:
        print(f"Average age with {mhi}: {result[0]}")
    else:
        print("No data found")
    
def count_w_mhi():
  mhi = clean_input("Enter mental health issue: ")
  result = run_query(f"select count(*) from student_mental_health where {mhi} = 'Yes';", (), True)
  print(f"Number of students with {mhi}: {result[0]}")
  return result
