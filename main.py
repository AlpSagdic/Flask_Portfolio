from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'YOU_CHOSE_A_SECRET_KEY'


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
