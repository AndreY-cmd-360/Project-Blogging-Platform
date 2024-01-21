from flask import Flask, render_template, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///andi_social.db'
db = SQLAlchemy(app)
swagger = Swagger(app, template={
    "swagger": "2.0",
    "info": {
        "title": "Social Media kind of platform",
        "description": "This is a start to a social media platform",
        "version": "0.1",
    },
    "basePath": "http://localhost:5000/"
})

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     username = db.Column(db.String(255), unique=True, nullable=False)
#     password = db.Column(db.String(255), nullable=False)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time_posted = db.Column(db.DateTime, nullable=False, default=db.func.now())
    account_name = db.Column(db.String(255), nullable=True)
    content = db.Column(db.Text, nullable=False)


@app.route('/', methods=['GET'])
def index():
    """
        Home endpoint.

        ---
        tags:
          - name: Andi Media

        responses:
          200:
            description: Display the posts
    """
    posts = Post.query.order_by(Post.time_posted.desc()).all()
    return render_template('index.html', posts=posts)


@app.route('/create_post', methods=['POST'])
def create_post():
    """
        Create a new post.

        ---
        tags:
          - name: Andi Media

        parameters:
          - name: post_content
            in: formData
            type: string
            required: true
            description: The content of the post.

        responses:
          302:
            description: Redirect to the home page after creating the post
    """
    if request.method == 'POST':
        post_content = request.form['post_content']
        if post_content:
            new_post = Post(content=post_content, account_name='Anonymous')
            db.session.add(new_post)
            db.session.commit()
            return redirect('/')
        else:
            return jsonify({'success': False, 'error': 'Invalid data'})
    else:
        return jsonify({'success': False, 'error': 'Invalid method'})


@app.route('/delete_post/<int:id>')
def delete_post(id):
    """
        Delete a post.

        ---
        tags:
          - name: Andi Media

        parameters:
          - name: id
            in: path
            type: integer
            required: true
            description: The id of the post to delete.

        responses:
          302:
            description: Redirect to the home page after deleting the post
    """
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    # Run the Flask app
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
