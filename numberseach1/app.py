from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20), nullable=False)
    info = db.Column(db.Text, nullable=False)
    positive_votes = db.Column(db.Integer, default=0)
    negative_votes = db.Column(db.Integer, default=0)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        phone_number = request.form['phone_number']
        info = request.form['info']

        if phone_number and info:
            new_post = Post(phone_number=phone_number, info=info)
            db.session.add(new_post)
            db.session.commit()
            flash('投稿が成功しました！', 'success')
        else:
            flash('電話番号と情報を入力してください。', 'error')

    posts = Post.query.all()
    grouped_posts = {}
    for post in posts:
        if post.phone_number not in grouped_posts:
            grouped_posts[post.phone_number] = []
        grouped_posts[post.phone_number].append(post.info)

    return render_template('index.html', grouped_posts=grouped_posts)

# 以下、他のルートとテンプレートの定義


# 以下、他のルートとテンプレートの定義

@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        phone_number = request.form['phone_number']
        info = request.form['info']

        if phone_number and info:
            new_post = Post(phone_number=phone_number, info=info)
            db.session.add(new_post)
            db.session.commit()
            flash('投稿が成功しました！', 'success')
            return redirect(url_for('index'))
        else:
            flash('電話番号と情報を入力してください。', 'error')

    return render_template('create_post.html')

@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def view_post(post_id):
    post = Post.query.get_or_404(post_id)

    if request.method == 'POST':
        vote = request.form['vote']

        if vote == 'yes':
            post.positive_votes += 1
        elif vote == 'no':
            post.negative_votes += 1

        db.session.commit()

    return render_template('view_post.html', post=post)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form['search_query']
        posts = Post.query.filter(Post.phone_number.contains(search_query)).all()
        return render_template('search.html', posts=posts)

    return render_template('search.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # テーブルを作成
    app.run(debug=True)
