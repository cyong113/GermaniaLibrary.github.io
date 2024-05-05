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
    word = ""  # Initialize the word variable
    if request.method == 'POST':
        word = request.form.get('word', '')  # Default to empty string if no word is given
        if text and word:  # Ensure both text is loaded and word is not empty
            sentences = find_sentences_containing_word(text, word)
            return render_template_string(home_template(), sentences=sentences, word=word)
    # Always pass the word, even if it's empty, to avoid "undefined" errors in the template
    return render_template_string(home_template(), sentences=[], word=word)


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
      <title>Search Tacitus Germania</title>
      <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&display=swap" rel="stylesheet">
      <style>
        html {
            overflow-y: scroll; /* Always shows vertical scrollbar */
        }
        body { font-family: 'Fira Code', monospace; margin: 0; background-color: #222; color: #fff; overflow-x: hidden; }
        .top-nav { background-color: #333; padding: 10px; text-align: center; }
        .top-nav a { color: #ccc; font-size: 15px; padding: 24px; text-decoration: none; }
        .header { background-color: #333; padding: 60px; text-align: center; }
        .header h1 { color: #ddd; font-size: 30px; }
        .content { padding: 20px; }
        .content ul li { 
            padding: 5px 10px; 
            display: inline-block;
            margin-right: 10px; 
            margin-bottom: 15px;
            background: #333; 
            border-radius: 6px;
        }
        input[type="text"], button {
            padding: 10px;
            margin: 5px 0;
            border-radius: 5px;
            border: 1px solid #ccc;
            font-size: 16px;
            width: auto;
        }
        input[type="text"] {
            flex-grow: 1;
            margin-right: 10px;
        }
        button {
            cursor: pointer;
            background-color: #444;
            color: white;
            border: none;
        }
        button:hover, button:focus {
            background-color: #555;
        }
        input[type="text"]:focus {
            border-color: #666;
            outline: none;
        }
      </style>
    </head>
    <body>
      <div class="top-nav">
        <a href="/">Search</a> | <a href="/tribes">Tribes in Germania</a>
      </div>
      <div class="header">
        <h1>Search Tacitus Germania</h1>
        <form method="post">
          <input type="text" name="word" placeholder="Enter a word" required>
          <button type="submit">Search</button>
        </form>
      </div>
      <div class="content">
        {% if sentences %}
          <h2>Sentences containing "{{ word }}":</h2>
          <ul>
          {% for sentence in sentences %}
            <li>{{ sentence }}</li>
          {% endfor %}
          </ul>
        {% elif word %}
          <p>No sentences found containing the word "{{ word }}".</p>
        {% else %}
          <p> </p>
        {% endif %}
      </div>
    </body>
    </html>
    '''



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
      <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&display=swap" rel="stylesheet">
      <style>
        body { font-family: 'Fira Code', monospace; margin: 0; background-color: #222; color: #fff; }
        .top-nav { background-color: #333; padding: 10px; text-align: center; }
        .top-nav a { color: #ccc; font-size: 15px; padding: 24px; text-decoration: none; }
        .header { background-color: #333; padding: 60px; text-align: center; }
        .header h2 { color: #ddd; font-size: 30px; }
        iframe { width: 100%; height: 90vh; border: none; }
      </style>
    </head>
    <body>
      <div class="top-nav">
        <a href="/">Search</a> | <a href="/tribes">Tribes in Germania</a>
      </div>
      <div class="header">
        <h2>Tribes Mentioned By Tacitus</h2>
        <iframe src="https://www.figma.com/embed?embed_host=share&url=https%3A%2F%2Fwww.figma.com%2Fproto%2F48FybQ1oHF89y0faSZGo7h%2FUntitled%3Ftype%3Ddesign%26node-id%3D9-8903%26t%3DGibRPHPgGAeLZFVf-1%26scaling%3Dmin-zoom%26page-id%3D0%253A1%26mode%3Ddesign" allowfullscreen></iframe>
      </div>
    </body>
    </html>
    '''





if __name__ == "__main__":
    app.run(debug=True)  # Turn off debug mode when deploying to production.
