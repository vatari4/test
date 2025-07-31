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
    
@app.route('/reviews', methods=['POST'])
def create_review():
    data = request.get_json()
    text = data.get('text', '').strip()

    if not text:
        return jsonify({'error': 'Поле "text" обязательно'}), 400

    sentiment = analyze_sentiment(text)
    created_at = datetime.utcnow().isoformat()

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO reviews (text, sentiment, created_at)
            VALUES (?, ?, ?)
        ''', (text, sentiment, created_at))
        conn.commit()
        review_id = cursor.lastrowid
        conn.close()
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({
        'id': review_id,
        'text': text,
        'sentiment': sentiment,
        'created_at': created_at
    }), 201

@app.route('/reviews', methods=['GET'])
def get_reviews():
    sentiment_filter = request.args.get('sentiment')

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        if sentiment_filter:
            cursor.execute('''
                SELECT id, text, sentiment, created_at
                FROM reviews
                WHERE sentiment = ?
                ORDER BY created_at DESC
            ''', (sentiment_filter,))
        else:
            cursor.execute('''
                SELECT id, text, sentiment, created_at
                FROM reviews
                ORDER BY created_at DESC
            ''')

        rows = cursor.fetchall()
        conn.close()
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

    reviews = [
        {'id': r[0], 'text': r[1], 'sentiment': r[2], 'created_at': r[3]}
        for r in rows
    ]

    return jsonify(reviews)
    
if __name__ == '__main__':
    app.run(debug=True)