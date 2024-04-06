from flask import Flask, render_template, request
from text_summary import summarizer

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/analyze', methods = ['GET', 'POST'])
def analyze():
    # it is good that i should initialize the text here else it will crash if no value is passed 
    summary = "Enter Correct value to be initialised"
    org_txt = "Enter Valid length of text"
    line_of_summary = 0

    if request.method == 'POST':
        rawtext = request.form['rawtext']
        summary, org_txt, line_of_summary = summarizer(rawtext)

    return render_template('summary.html',  summary = summary, original_txt = org_txt, total_line_in_summary = line_of_summary)



    return render_template()




if __name__ == '__main__':
    app.run()

