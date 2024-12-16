from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import random

app = Flask(__name__)
def init_db():
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS questions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        question TEXT NOT NULL,
                        option1 TEXT NOT NULL,
                        option2 TEXT NOT NULL,
                        option3 TEXT NOT NULL,
                        option4 TEXT NOT NULL,
                        correct_option INTEGER NOT NULL)''')
    conn.commit()
    cursor.execute("SELECT COUNT(*) FROM questions")
    if cursor.fetchone()[0] == 0:
        sample_questions = [
            ("What is the capital of France?", "Paris", "London", "Berlin", "Madrid", 1),
            ("What is 2 + 2?", "3", "4", "5", "6", 2),
            ("Which programming language is known as the language of AI?", "Python", "Java", "C++", "Ruby", 1),
            ("Who wrote 'Hamlet'?", "Charles Dickens", "Mark Twain", "William Shakespeare", "J.K. Rowling", 3),
            ("What is the boiling point of water?", "90°C", "100°C", "120°C", "150°C", 2)
            ("where is the university SPSU located?","Udaipur","Hyderabad","Mumbai","Banglore",1)
            ("what is the first element in periodic table?","Hydrogen","helium","Carbon","Boron",1)
        ]
        cursor.executemany("INSERT INTO questions (question, option1, option2, option3, option4, correct_option) VALUES (?, ?, ?, ?, ?, ?)", sample_questions)
        conn.commit()

    conn.close()

@app.route('/')
def home():
    return redirect(url_for('quiz'))

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        question_id = int(request.form['question_id'])
        selected_option = int(request.form['option'])
        conn = sqlite3.connect('quiz.db')
        cursor = conn.cursor()
        cursor.execute("SELECT correct_option FROM questions WHERE id = ?", (question_id,))
        correct_option = cursor.fetchone()[0]
        conn.close()

        if selected_option == correct_option:
            return render_template('result.html', message="Hurray! You got it right!", correct=True)
        else:
            return render_template('result.html', message="Oops! Try again!", correct=False)

    else:
        conn = sqlite3.connect('quiz.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM questions")
        questions = cursor.fetchall()
        conn.close()

        question = random.choice(questions)
        return render_template('quiz.html', question=question)

@app.route('/next')
def next_question():
    return redirect(url_for('quiz'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
