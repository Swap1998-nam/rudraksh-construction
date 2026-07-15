from flask import Blueprint, render_template, abort
from app.models import BlogPost

blog_bp = Blueprint('blog', __name__)

@blog_bp.route('/')
def list():
    posts = BlogPost.query.filter_by(published=True).order_by(BlogPost.created_at.desc()).all()
    return render_template('blog/list.html', posts=posts)

@blog_bp.route('/<slug>')
def post(slug):
    post = BlogPost.query.filter_by(slug=slug, published=True).first_or_404()
    return render_template('blog/post.html', post=post)
