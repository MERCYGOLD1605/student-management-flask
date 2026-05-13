from flask import Flask, render_template, request, redirect

app = Flask(__name__)


# 📋 Home page
@app.route('/')
def index():
    students = []

    try:
        with open("students.txt", "r") as file:
            for line in file.readlines():
                name, age, course = line.strip().split(",")

                students.append({
                    "name": name,
                    "age": age,
                    "course": course
                })

    except:
        pass

    return render_template(
        "index.html",
        students=students,
        total_students=len(students)
    )


# 🔍 Search student
@app.route('/search', methods=['POST'])
def search_student():
    query = request.form['query'].lower()

    filtered_students = []

    try:
        with open("students.txt", "r") as file:
            for line in file.readlines():
                name, age, course = line.strip().split(",")

                student = {
                    "name": name,
                    "age": age,
                    "course": course
                }

                # 🔥 Partial match
                if query in name.lower():
                    filtered_students.append(student)

    except:
        pass

    return render_template(
        "index.html",
        students=filtered_students,
        total_students=len(filtered_students)
    )


# ➕ Add student
@app.route('/add', methods=['POST'])
def add_student():
    name = request.form['name']
    age = request.form['age']
    course = request.form['course']

    with open("students.txt", "a") as file:
        file.write(f"{name},{age},{course}\n")

    return redirect('/')


# ❌ Delete student
@app.route('/delete/<int:index>')
def delete_student(index):

    with open("students.txt", "r") as file:
        students = file.readlines()

    students.pop(index)

    with open("students.txt", "w") as file:
        file.writelines(students)

    return redirect('/')


# ✏️ Update student
@app.route('/update/<int:index>', methods=['GET', 'POST'])
def update_student(index):

    with open("students.txt", "r") as file:
        students = file.readlines()

    if request.method == 'POST':

        name = request.form['name']
        age = request.form['age']
        course = request.form['course']

        students[index] = f"{name},{age},{course}\n"

        with open("students.txt", "w") as file:
            file.writelines(students)

        return redirect('/')

    # Existing student data
    name, age, course = students[index].strip().split(",")

    student = {
        "name": name,
        "age": age,
        "course": course
    }

    return render_template(
        "update.html",
        student=student,
        index=index
    )


if __name__ == "__main__":
    app.run(debug=True)