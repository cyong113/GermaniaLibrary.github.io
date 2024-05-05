from flask import Flask, request, render_template_string

import nltk
from nltk.tokenize import sent_tokenize

# Download the NLTK data only once; it's not needed every time in the actual application.
nltk.download('punkt')

app = Flask(__name__)

# Function to load text from a file, handling errors if the file is not found.
def load_text(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return None

# Load the text once when the server starts.
text = load_text('Germania.txt')

# Function to find sentences that contain a specified word.
def find_sentences_containing_word(text, word):
    sentences = sent_tokenize(text, language='german')
    return [sentence for sentence in sentences if word.lower() in sentence.lower()]

# Define the route and the request handling for the home page.
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        word = request.form.get('word')
        if text and word:
            sentences = find_sentences_containing_word(text, word)
            return render_template_string(home_template(), sentences=sentences, word=word)
        else:
            return render_template_string(home_template(), sentences=[], word=word)
    return render_template_string(home_template())

# Route for the Figma embed page.
@app.route('/tribes')
def tribes():
    return render_template_string(tribes_template())

# Function that returns the HTML template for the home page.
def home_template():
    return '''
    <!doctype html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport"
            content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
      <meta http-equiv="X-UA-Compatible" content="ie=edge">
      <title>Search in Germania</title>
      <style>
        body { font-family: Arial, sans-serif; }
        nav { background-color: #f2f2f2; padding: 10px; text-align: center; text-align: left;}
        nav a { margin: 0 10px; text-decoration: none; color: black; font-size: 18px; }
      </style>
    </head>
    <body>
      <nav>
        <a href="/">Search</a>
        <a href="/tribes">Tribes mentioned</a>
      </nav>
      <h1>Search for Sentences in Germania</h1>
      <form method="post">
        <input type="text" name="word" placeholder="Enter a word" required>
        <button type="submit">Search</button>
      </form>
      {% if sentences %}
        <h2>Sentences containing "{{ word }}":</h2>
        <ul>
        {% for sentence in sentences %}
          <li>{{ sentence }}</li>
        {% endfor %}
        </ul>
      {% else %}
        <p>No sentences found containing the word "{{ word }}".</p>
      {% endif %}
    </body>
    </html>
    '''

# Function that returns the HTML template for the Tribes page.
def tribes_template():
    return '''
    <!doctype html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport"
            content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
      <meta http-equiv="X-UA-Compatible" content="ie=edge">
      <title>Tribes in Germania</title>
      <style>
        body { font-family: Arial, sans-serif; }
        iframe { width: 100%; height: 90vh; border: none; }
        nav { background-color: #f2f2f2; padding: 10px; text-align: center; text-align: left;}
        nav a { margin: 0 10px; text-decoration: none; color: black; font-size: 18px; }
      </style>
    </head>
    <body>
      <nav>
        <a href="/">Search</a>
        <a href="/tribes">Tribes mentioned</a>
      </nav>
      <iframe src="https://www.figma.com/embed?embed_host=share&url=https%3A%2F%2Fwww.figma.com%2Fproto%2F48FybQ1oHF89y0faSZGo7h%2FUntitled%3Ftype%3Ddesign%26node-id%3D9-8903%26t%3DGibRPHPgGAeLZFVf-1%26scaling%3Dmin-zoom%26page-id%3D0%253A1%26mode%3Ddesign" allowfullscreen></iframe>
    </body>
    </html>
    '''

if __name__ == "__main__":
    app.run(debug=True)  # Turn off debug mode when deploying to production.
