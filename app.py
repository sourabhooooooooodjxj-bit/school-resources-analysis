from flask import Flask, render_template, request, redirect
 
import sqlite3
from database import create_database
app = Flask(__name__)
create_database()

app = Flask(__name__,static_folder="static")
school_data =[]


@app.route("/")
def home():
    con = sqlite3.connect("school.db")
    cursor = con.cursor()

    cursor.execute("SELECT COUNT(*) FROM schools")
    total_schools = cursor.fetchone()[0]

    cursor.execute("SELECT COALESCE(SUM(students), 0) FROM schools")
    total_students = cursor.fetchone()[0]

    cursor.execute("SELECT COALESCE(SUM(teachers), 0) FROM schools")
    total_teachers = cursor.fetchone()[0]

    cursor.execute("SELECT COALESCE(SUM(classrooms), 0) FROM schools")
    total_classrooms = cursor.fetchone()[0]

    cursor.execute("SELECT COALESCE(SUM(laboratories), 0) FROM schools")
    total_laboratories = cursor.fetchone()[0]

    cursor.execute("SELECT COALESCE(SUM(computers), 0) FROM schools")
    total_computers = cursor.fetchone()[0]

    cursor.execute("SELECT COALESCE(SUM(toilets), 0) FROM schools")
    total_toilets = cursor.fetchone()[0]

    cursor.execute("SELECT * FROM schools")
    schools = cursor.fetchall()
    school_names = [school[1] for school in schools]
    student_counts = [school[3] for school in schools]
    teacher_counts = [school[4] for school in schools]

    con.close()

    return render_template(
        "index.html",
        total_schools=total_schools,
        total_students=total_students,
        total_teachers=total_teachers,
        total_classrooms=total_classrooms,
        total_laboratories=total_laboratories,
        total_computers=total_computers,
        total_toilets=total_toilets,
        schools=schools,
        school_names=school_names,
        student_counts=student_counts,
        teacher_counts=teacher_counts
    )
@app.route("/report")
def report():
    con = sqlite3.connect("school.db")
    cursor = con.cursor()

    cursor.execute("SELECT COUNT(*) FROM schools")
    total_schools = cursor.fetchone()[0]

    cursor.execute("SELECT COALESCE(SUM(students), 0) FROM schools")
    total_students = cursor.fetchone()[0]

    cursor.execute("SELECT COALESCE(SUM(teachers), 0) FROM schools")
    total_teachers = cursor.fetchone()[0]

    cursor.execute("SELECT COALESCE(SUM(classrooms), 0) FROM schools")
    total_classrooms = cursor.fetchone()[0]

    cursor.execute("SELECT COALESCE(SUM(laboratories), 0) FROM schools")
    total_laboratories = cursor.fetchone()[0]

    cursor.execute("SELECT COALESCE(SUM(toilets), 0) FROM schools")
    total_toilets = cursor.fetchone()[0]

    cursor.execute("SELECT COALESCE(SUM(computers), 0) FROM schools")
    total_computers = cursor.fetchone()[0]

    cursor.execute("SELECT * FROM schools")
    schools = cursor.fetchall()

    school_names = [school[1] for school in schools]
    student_counts = [school[3] for school in schools]
    teacher_counts = [school[4] for school in schools]
    con.close()

    return render_template(
        "report.html",
        total_schools=total_schools,
        total_students=total_students,
        total_teachers=total_teachers,
        total_classrooms=total_classrooms,
        total_laboratories=total_laboratories,
        total_toilets=total_toilets,
        total_computers=total_computers,
        schools=schools,
        school_names=school_names,
        student_counts=student_counts,
        teacher_counts=teacher_counts
    )
@app.route("/recommendations")
def recommendation():
    con = sqlite3.connect("school.db")
    cursor = con.cursor()

    cursor.execute("SELECT * FROM schools")
    schools = cursor.fetchall()

    con.close()

    return render_template(
        "recommendation.html",
        schools=schools
    )
@app.route("/school")
def school():
    return render_template("school.html")


@app.route("/submit", methods=["POST"])
def submit():

    school_name = request.form["school_name"]
    location = request.form["location"]
    students = request.form["students"]
    teachers = request.form["teachers"]
    classrooms = request.form["classrooms"]
    laboratories = request.form["laboratories"]
    toilets = request.form["toilets"]
    computers = request.form["computers"]
    conn = sqlite3.connect("school.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO schools (school_name, location, students, teachers, classrooms, laboratories, toilets, computers)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (school_name, location, students, teachers, classrooms, laboratories, toilets, computers))

    conn.commit()
    conn.close()

    return "School data saved successfully!"
@app.route("/data")
def data():

    search = request.args.get("search", "")

    conn = sqlite3.connect("school.db")
    cursor = conn.cursor()

    if search:
        cursor.execute(
            "SELECT * FROM schools WHERE school_name LIKE ?",
            ("%" + search + "%",)
        )
    else:
        cursor.execute("SELECT * FROM schools")

    schools = cursor.fetchall()
    school_names = [school[1] for school in schools] 
    student_counts =[school[3] for school in schools]

    cursor.execute("SELECT COUNT(*) FROM schools")
    total_schools = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(students) FROM schools")
    total_students = cursor.fetchone()[0] or 0
    

    cursor.execute("SELECT SUM(teachers) FROM schools")
    total_teachers = cursor.fetchone()[0] or 0

   

    conn.close()

    return render_template(
        "data.html",
        schools=schools,
        school_names=school_names,
        student_counts=student_counts,
        total_schools=total_schools,
        total_students=total_students,
        total_teachers=total_teachers
    )

@app.route("/delete/<int:school_id>")
def delete_school(school_id):

    conn = sqlite3.connect("school.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM schools WHERE id = ?",
        (school_id,)
    )

    conn.commit()
    conn.close()

    return redirect ("/data")
@app.route("/edit/<int:school_id>", methods=["GET", "POST"])
def edit_school(school_id):

    conn = sqlite3.connect("school.db")
    cursor = conn.cursor()

    if request.method == "POST":

        school_name = request.form["school_name"]
        location = request.form["location"]
        students = request.form["students"]
        teachers = request.form["teachers"]
        

        cursor.execute("""
            UPDATE schools
            SET school_name = ?, location = ?, students = ?, teachers = ?
            WHERE id = ?
        """, (school_name, location, students, teachers, school_id))

        conn.commit()
        conn.close()

        return redirect("/data")

    cursor.execute(
        "SELECT * FROM schools WHERE id = ?",
        (school_id,)
    )

    school = cursor.fetchone()

    conn.close()

    return render_template("edit.html", school=school)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=50000,debug=True)