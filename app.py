from flask import Flask, render_template, jsonify, request, redirect, url_for
import json

app = Flask(__name__)


@app.route('/')
def index():
    with open('posts.json', 'r', encoding='utf-8') as datei:
        blog_posts = json.load(datei)
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':

        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        if  author and  title and  content: # or not isinstance(author,str)
            with open('posts.json', 'r', encoding='utf-8') as datei:
                blog_posts = json.load(datei)
            new_id = max(p["id"] for p in blog_posts) + 1 if blog_posts else 1

            new_posts = {
                "id": new_id,
                "author": author,
                "title": title,
                "content": content
            }
            blog_posts.append(new_posts)

            with open('posts.json', 'w', encoding='utf-8') as datei:
                json.dump(blog_posts, datei, indent=4, ensure_ascii=False)
            return redirect(url_for('index'))
        else:
            errors = []
            if not author:
                errors.append(f'Author: "{author}" denied')
            if not title:
                errors.append(f'Title: "{title}" denied')
            if not content:
                errors.append(f'Text: "{content}" denied')
            return render_template('add.html', errors=errors)

    return render_template('add.html')



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)