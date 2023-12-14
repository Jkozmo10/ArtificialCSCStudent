import subprocess

import jinja2
from flask import Flask, render_template, request

app = Flask(__name__)

templateEnv = jinja2.Environment(
    comment_start_string='{=',
    comment_end_string='=}',
)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', defaults={'year': None}, methods=['GET', 'POST'])
@app.route('/generate/<year>', methods=['GET', 'POST'])
def my_link(year=None):
    print(year)
    if year:
        year = int(year)
    if year and year > 0 and year < 6:
        subprocess.run(['python3', 'driver.py', str(year)], check=True)
    else:
        subprocess.run(['python3', 'driver.py'], check=True)
    subprocess.run(['pdflatex', 'resume.tex'], check=True)
    subprocess.run(['mv', 'resume.pdf', './static/resume.pdf'], check=True)
    return {'year': year}


if __name__ == '__main__':
    app.run(debug=True, port=8000)
