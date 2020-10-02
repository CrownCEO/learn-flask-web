from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello 大家好，很开心在编程工作坊和大家一起学习FlaskWeb"


if __name__ == '__main__':
    app.run(debug=True)
