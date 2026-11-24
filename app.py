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











# @app.route("/posts", methods=["GET"])
# def get_all_posts():
#     return jsonify(posts), 200
#
# @app.route("/posts/<int:post_id>", methods=["GET"])
# def get_post_by_id(post_id):
#     post = next((i for i in posts if i["id"] == post_id), None)
#     if post is not None:
#         return jsonify(post), 200
#     else:
#         return jsonify({"error": "Post not found"}), 404
#
#

#
#
# @app.route("/posts/<int:post_id>", methods=["DELETE"])
# def delete_post(post_id):
#     post = next((i for i in posts if i["id"] == post_id), None)
#
#     if post:
#         posts.remove(post)
#         return jsonify({"success": True}), 200
#     else:
#         return jsonify({"error": "post not found"}), 404
#
#
# @app.route("/posts/<int:post_id>", methods=["PUT"])
# def recreate_post(post_id):
#     if request.is_json:
#         post = next((i for i in posts if i["id"] == post_id), None)
#         if post is None:
#             return jsonify({"error": "Post not found"}), 404
#         else:
#             data = request.get_json(silent=True)
#
#             if not data or "text" not in data or "author" not in data:
#                 return jsonify({"error 1": "Unsupported Jason Type: 'text' and 'author' in Jason is required!"}), 415
#             else:
#                 data["id"] = post_id
#                 posts.remove(post)
#                 posts.append(data)
#                 return jsonify({f'Post {post_id} is overritten': post}, {f'with this Post {post_id}': data}), 201
#     else:
#         return jsonify({"error 2": "Unsupported Media Type: That's is no Jason format"}), 415
#
#
# @app.route("/posts/<int:post_id>", methods=["PATCH"])
# def fix_post(post_id):
#     if request.is_json:
#         post = next((i for i in posts if i["id"] == post_id), None)
#         if post is None:
#             return jsonify({"error": "Post not found"}), 404
#         else:
#             new_post = post.copy()
#             data = request.get_json(silent=True)
#
#             if not data:  # or "text" not in data or "author" not in data:
#                 return jsonify({"error 1": "Unsupported Jason Type: 'text' and 'author' in Jason is required!"}), 415
#             else:
#                 if "text" in data:
#                     new_post["text"] = data["text"]
#                     print("text updated")
#
#                 if "author" in data:
#                     new_post["author"] = data["author"]
#
#                 posts.remove(post)
#                 posts.append(new_post)
#                 return jsonify({f'Post {post_id} is Updated': post}, {f'with this Post {post_id}': new_post}), 201
#     else:
#         return jsonify({"error 2": "Unsupported Media Type: That's is no Jason format"}), 415







if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
