#Importing required modules
from database import (filename, config, convert, run_query, clean_input, cgpa_clean, insights)
from visualization import *

convert(filename, **config)

    
#defining queries in menu
def disp_all(): #Display all records
    data = run_query("SELECT * FROM student_mental_health;", fetch=True)
    for row in data:
        print(row)
      
def add_rec(): #Add record
    Gender = clean_input("Enter gender: ")
    Age = input("Enter age: ")
    Course = clean_input("Enter course: ")
    Year = int(input("Enter year of study: "))
    CGPA = float(input("Enter CGPA (0.00-4.00): "))
    nCGPA = cgpa_clean(CGPA)
    Depression = clean_input("Do you have Depression? (Yes/No): ")
    Anxiety = clean_input("Do you have Anxiety? (Yes/No): ")
    Panic_attack = clean_input("Do you have Panic Attack? (Yes/No): ")
    Specialist_seeked = clean_input("Have you seeked a specialist? (Yes/No): ")
    run_query(
        "INSERT INTO student_mental_health VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);",
        (Gender, Age, Course, Year, nCGPA, Depression, Anxiety, Panic_attack, Specialist_seeked))

def modify_rec(): #Modify record
    allowed_fields = ["Gender", "Age", "Course", "Year_of_study", "Cgpa", 
                  "Depression", "Anxiety", "Panic_attack", "Specialist_seeked"]
    field = clean_input("Field to modify: ")
    if field not in allowed_fields:
        print("Invalid field ❌")
        return
    old_val = clean_input("Old value: ")
    new_val = clean_input("New value: ")
    run_query(f"UPDATE student_mental_health SET {field}=%s WHERE {field}=%s;", (new_val, old_val))

def delete_rec(): #Delete record
    field = clean_input("Field to delete: ")
    value = clean_input("Value: ")
    run_query(f"DELETE FROM student_mental_health WHERE {field}=%s;", (value,))

while True:
    print("""Student Mental Health Analysis 📈 \n
-KEY- \n Fields = Gender/Age/CGPA(o/Year of Study/Course \n MHI = Particular Mental Health Issue (Depression/Anxiety/Panic_attack) \n
~MENU~ \n 1. Display all records + Bar Chart \n 2. Add record \n 3. Modify record(s) \n 4. Delete record(s) \n
~INSIGHTS~ \n 5. Show Insights \n 6. Distribution by MHI fields \n 7. MHI by Fields \n 8. Exit""")
    try:
      choice = int(input("Enter your choice: "))
    except (ValueError, TypeError):
        print("Invalid input. ⚠️ Enter choice number: ")
        continue
    menu = {1: disp_all, 2: add_rec, 3: modify_rec, 4: delete_rec, 5: insights, 6: mhi_by_fields, 7: dist_by_fields }
    if choice == 8:
        break
    elif choice in menu:
        menu[choice]()