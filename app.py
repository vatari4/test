from flask import Flask, request, jsonify
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)
DB_PATH = 'reviews.db'  

def analyze_sentiment(text):
    text = text.lower()
    positives = ['хорош', 'люблю', 'отлично', 'супер', 'нравит', 'удобно']
    negatives = ['плохо', 'ненавиж', 'ужас', 'проблем', 'тормозит', 'неудобно']

    if any(word in text for word in positives):
        return 'positive'
    elif any(word in text for word in negatives):
        return 'negative'
    else:
        return 'neutral'
    
if __name__ == '__main__':
    app.run(debug=True)