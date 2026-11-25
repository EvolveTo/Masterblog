import json
from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)


def read_posts(posts_file='posts.json'):
    with open(posts_file, 'r', encoding='utf-8') as datei:
        blog_posts = json.load(datei)
    return blog_posts


def write_posts(blog_posts, posts_file='posts.json'):
    sorted_blog_posts = sorted(blog_posts, key=lambda post: post["id"])
    with open(posts_file, 'w', encoding='utf-8') as datei:
        json.dump(sorted_blog_posts, datei, indent=4, ensure_ascii=False)


def fetch_post_by_id(post_id):
    post = next((i for i in read_posts() if i["id"] == post_id), None)
    return post


def request_post(post_id="", likes=0):
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

    post = build_post(post_id, author, title, content, likes)
    return post


def build_post(post_id, author, title, content, likes=0):
    post = {
        "id": post_id,
        "author": author,
        "title": title,
        "content": content,
        "likes": likes}
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

    if "likes" in post:
        likes = post["likes"]
    else:
        likes = 0

    if request.method == 'POST':
        blog_posts = read_posts()
        blog_posts.remove(post)
        # To keep the likes: new_post = request_post(post_id, likes)
        new_post = request_post(post_id)
        if isinstance(new_post, list):
            return render_template(
                'update.html', post_id=post_id, post=post, errors=new_post)

        blog_posts.append(new_post)
        write_posts(blog_posts)
        return redirect(url_for('index'))

    return render_template('update.html', post_id=post_id, post=post)


@app.route('/like/<int:post_id>', methods=['POST'])
def likes(post_id):
    post = fetch_post_by_id(post_id)
    if post is None:
        # Post not found
        return "Post not found", 404

    blog_posts = read_posts()
    blog_posts.remove(post)

    if "likes" in post:
        likes = post["likes"] + 1
    else:
        likes = 1

    post = build_post(
        post["id"], post["author"], post["title"], post["content"], likes)

    blog_posts.append(post)
    write_posts(blog_posts)
    return redirect(url_for('index'))







if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)