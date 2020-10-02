from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)


@app.route("/show_student_information")
def show():
    # read file
    data = []
    with open("./data/student_information.txt",encoding='utf-8') as fin:
        is_first_line = True
        for line in fin:
            if is_first_line:
                is_first_line = False
                continue
            line = line[:-1]  # \n
            student_number, name, height = line.split("\t")
            data.append((student_number, name, height))
    return render_template("student_information.html", data=data)


if __name__ == '__main__':
    app.run(debug=True)
