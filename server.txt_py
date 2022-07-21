from flask import Flask, request, render_template
import SpotifyFunctions
app = Flask(__name__)

@app.route('/')
def default():
    return render_template('index.html')

@app.route('/spotify')
def my_form():
    return render_template('form.html')

@app.route('/spotify', methods=['POST'])
def my_form_post():
    text = request.form['song']
    SpotifyFunctions.search_analyze(text)
    return render_template('image.html')


app.run(host='localhost', port=5000)