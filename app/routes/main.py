from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Project, Service, TeamMember, BlogPost, SiteSetting, ContactMessage
from app.forms import ContactForm
from app import db
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    services = Service.query.filter_by(active=True).order_by(Service.order).all()
    projects = Project.query.order_by(Project.order, Project.created_at.desc()).all()
    team_members = TeamMember.query.order_by(TeamMember.order).all()
    blog_posts = BlogPost.query.filter_by(published=True).order_by(BlogPost.created_at.desc()).limit(3).all()

    settings = {}
    for key in ['site_name', 'site_email', 'site_phone', 'site_address', 'site_hours']:
        settings[key] = SiteSetting.get(key)

    project_count = Project.query.count()
    team_count = TeamMember.query.count()
    years_active = datetime.utcnow().year - 2016

    return render_template('index.html',
                         services=services,
                         projects=projects,
                         team_members=team_members,
                         blog_posts=blog_posts,
                         settings=settings,
                         project_count=project_count,
                         team_count=team_count,
                         years_active=years_active)

@main_bp.route('/contact', methods=['POST'])
def contact_submit():
    form = ContactForm()
    if form.validate_on_submit():
        message = ContactMessage(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data or '',
            project_type=form.project_type.data,
            details=form.details.data or ''
        )
        db.session.add(message)
        db.session.commit()
        flash('Thank you! Your inquiry has been received. We will get back to you shortly.', 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field}: {error}', 'error')
    return redirect(url_for('main.index') + '#contact')
