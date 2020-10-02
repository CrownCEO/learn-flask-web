from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

# 代码示例，仅仅是为了测试request的属性值
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == request.form['password']:
            return 'TRUE'
        else:
            # 当form中的两个字段内容不一致时，返回我们所需要的测试信息
            return str(request.headers)  # 需要替换的部分
    else:
        return "METHODS ERROR "


@app.route('/hello_code/chinese?name=<name>&age=<age>')
def hello(name, age):
    return 'Hello 大家好，我是' + name + ',我今年' + age + '岁了' + "很开心在编程工作坊和大家一起学习FlaskWeb"


@app.route("/index")
def index():
    data = {
        "a_str": "this is a str",
        "b_int": 1002,
        "list": [1, 2, 3, 4, 5],
        "dict": {
            "x": 44,
            "y": 55
        }
    }
    name = "44"
    return render_template("index.html", name=name, **data)


@app.template_filter("ls_filter")  # 自定义过滤器
def step2(a):
    return a[::2]


if __name__ == '__main__':
    app.run(debug=True)
