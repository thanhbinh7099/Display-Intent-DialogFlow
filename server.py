from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/a",methods=['GET', 'POST'])
def a():
    token = request.form['inputToken']

    print(request.form.getlist('display-options'))

    return '/static/structs_revisited.gv.pdf'



if __name__ == "__main__":
    app.run()