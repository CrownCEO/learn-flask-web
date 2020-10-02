from flask import Flask, send_from_directory

app = Flask(__name__)


@app.route("/download/<filepath>")
def index(filepath):
    return send_from_directory("./download_path", filename=filepath, as_attachment=True)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)
