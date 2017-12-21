from flask import Flask, render_template, request
from services.draw_intents import display_intent

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/a",methods=['GET', 'POST'])
def a():
    token = request.form['inputToken']
    display_options = request.form.getlist('display-options')
    if len(display_options) == 2:
        link = display_intent(token,"all")
    elif len(display_options) == 1:
        link = display_intent(token,display_options[0])
    else:
        link = ''
    return link



if __name__ == "__main__":
    app.run(debug=True, port=8000)