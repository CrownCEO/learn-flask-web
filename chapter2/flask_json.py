from flask import Flask, Response, jsonify, render_template
import json

app = Flask(__name__)


@app.route('/')
def root():
    t = {
        'a': 1,
        'b': 2,
        'c': [3, 4, 5]
    }
    # return t
    # return json.dumps(t)
    # return Response(json.dumps(t), mimetype='application/json')
    return jsonify(t)


@app.route("/show_student_information")
def show():
    # read file
    data = []
    with open("./data/student_information.json", encoding='utf-8') as fin:
        data = json.loads(fin.read())['data']

    return render_template("student_information_json.html", data=data)


if __name__ == '__main__':
    app.debug = True
    app.run()
