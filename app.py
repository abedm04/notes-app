from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)


def now():
    return datetime.now(timezone.utc)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_updated = db.Column(db.DateTime, default=now, onupdate=now)

    def __repr__(self):
        return f'<Note {self.id}>'


@app.route('/')
def index():
    notes = Note.query.order_by(Note.date_updated.desc()).all()
    return render_template('index.html', notes=notes)


@app.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        note_title = request.form.get('title')
        note_content = request.form['content']
        note = Note(title=note_title, content=note_content)

        try:
            db.session.add(note)
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return 'There was an issue adding your note'
    else:
        return render_template('create.html')


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    note = Note.query.get_or_404(id)

    if request.method == 'POST':
        note.title = request.form.get('title')
        note.content = request.form['content']

        try:
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return 'There was an issue updating your note'
    else:
        return render_template('update.html', note=note)


@app.route('/delete/<int:id>')
def delete(id):
    note = Note.query.get_or_404(id)

    try:
        db.session.delete(note)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return 'There was an issue deleting your note'


if __name__ == '__main__':
    app.run(debug=True)
