from flask import Flask, render_template

app = Flask(__name__)

pulter = [
    {
        'id': 1,
        'title': "Alex sin"

    },
    {
        'id': 2,
        'title': "Rolf sin"
    }

]


@app.route("/")
def hello_world():
    return render_template('home.html', plasser=pulter)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
