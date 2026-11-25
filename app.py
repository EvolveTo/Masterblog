from flask import Flask, render_template, jsonify, request, redirect, url_for
import json

app = Flask(__name__)


def read_posts(posts_file='posts.json'):
    with open(posts_file, 'r', encoding='utf-8') as datei:
        blog_posts = json.load(datei)
    return blog_posts


def write_posts(blog_posts, posts_file='posts.json'):
    with open(posts_file, 'w', encoding='utf-8') as datei:
        json.dump(blog_posts, datei, indent=4, ensure_ascii=False)


def fetch_post_by_id(post_id):
    post = next((i for i in read_posts() if i["id"] == post_id), None)
    return post


def request_post(post_id=""):
    author = request.form.get('author')
    title = request.form.get('title')
    content = request.form.get('content')

    if not author or not title or not content:
        errors = []
        if not author:
            errors.append(f'Author: "{author}" denied')
        if not title:
            errors.append(f'Title: "{title}" denied')
        if not content:
            errors.append(f'Text: "{content}" denied')
        return errors

    if not post_id:
        blog_posts = read_posts()
        post_id = max(p["id"] for p in blog_posts) + 1 if blog_posts else 1

    post = {
        "id": post_id,
        "author": author,
        "title": title,
        "content": content}
    return post


@app.route('/')
def index():
    return render_template('index.html', posts=read_posts())


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        new_post = request_post()
        if isinstance(new_post, list):
            return render_template('add.html', errors=new_post)

        blog_posts = read_posts()
        blog_posts.append(new_post)
        write_posts(blog_posts)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route("/delete/<int:post_id>", methods=["POST"])
def delete_post(post_id):
    post = fetch_post_by_id(post_id)
    if post:
        blog_posts = read_posts()
        blog_posts.remove(post)
        write_posts(blog_posts)
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    post = fetch_post_by_id(post_id)
    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        post = fetch_post_by_id(post_id)
        blog_posts = read_posts()
        blog_posts.remove(post)
        new_post = request_post(post_id)
        if isinstance(new_post, list):
            return render_template('update.html', errors=new_post)

        blog_posts.append(new_post)
        write_posts(blog_posts)
        return redirect(url_for('index'))

    return render_template('update.html', post=post)







if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)