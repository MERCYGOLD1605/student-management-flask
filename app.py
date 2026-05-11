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

    return render_template("index.html", students=students)


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


if __name__ == "__main__":
    app.run(debug=True)