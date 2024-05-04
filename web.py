from flask import Flask, request, render_template_string
import nltk
from nltk.tokenize import sent_tokenize

nltk.download('punkt')

app = Flask(__name__)

def load_text(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return None

text = load_text('Germania.txt')

def find_sentences_containing_word(text, word):
    sentences = sent_tokenize(text, language='german')
    return [sentence for sentence in sentences if word.lower() in sentence.lower()]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        word = request.form.get('word')
        if text and word:
            sentences = find_sentences_containing_word(text, word)
            return render_template_string(HTML_TEMPLATE, sentences=sentences, word=word)
        else:
            return render_template_string(HTML_TEMPLATE, sentences=[], word=word)
    return render_template_string(HTML_TEMPLATE)

HTML_TEMPLATE = '''
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport"
        content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="ie=edge">
  <title>Search in Germania</title>
</head>
<body>
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
    {% if word %}
      <p>No sentences found containing the word "{{ word }}".</p>
    {% endif %}
  {% endif %}
</body>
</html>
'''

if __name__ == "__main__":
    app.run(debug=True)
