import os
import uuid
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.models import User, Project, Service, TeamMember, ContactMessage, BlogPost, SiteSetting
from app.forms import (LoginForm, ProjectForm, ServiceForm, TeamForm,
                       BlogForm, SiteSettingForm)

admin_bp = Blueprint('admin', __name__)

def save_upload(file):
    if file and file.filename:
        ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
        filename = f"{uuid.uuid4().hex}.{ext}"
        upload_dir = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_dir, exist_ok=True)
        filepath = os.path.join(upload_dir, filename)
        file.save(filepath)
        return filename
    return None

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Welcome back, admin!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('admin.dashboard'))
        flash('Invalid username or password', 'error')
    return render_template('admin/login.html', form=form)

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('admin.login'))

@admin_bp.route('/')
@login_required
def dashboard():
    project_count = Project.query.count()
    service_count = Service.query.count()
    team_count = TeamMember.query.count()
    message_count = ContactMessage.query.count()
    unread_messages = ContactMessage.query.filter_by(is_read=False).count()
    blog_count = BlogPost.query.count()
    recent_messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).limit(5).all()
    return render_template('admin/dashboard.html',
                         project_count=project_count,
                         service_count=service_count,
                         team_count=team_count,
                         message_count=message_count,
                         unread_messages=unread_messages,
                         blog_count=blog_count,
                         recent_messages=recent_messages)

# --- Projects ---
@admin_bp.route('/projects')
@login_required
def projects():
    all_projects = Project.query.order_by(Project.order, Project.created_at.desc()).all()
    return render_template('admin/projects.html', projects=all_projects)

@admin_bp.route('/projects/new', methods=['GET', 'POST'])
@login_required
def project_new():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(
            title=form.title.data,
            category=form.category.data,
            description=form.description.data or '',
            location=form.location.data or '',
            year=form.year.data or '',
            featured=form.featured.data,
            order=form.order.data or 0
        )
        filename = save_upload(request.files.get('image'))
        if filename:
            project.image = filename
        db.session.add(project)
        db.session.commit()
        flash('Project created successfully!', 'success')
        return redirect(url_for('admin.projects'))
    return render_template('admin/project_form.html', form=form, project=None)

@admin_bp.route('/projects/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def project_edit(id):
    project = Project.query.get_or_404(id)
    form = ProjectForm(obj=project)
    if form.validate_on_submit():
        project.title = form.title.data
        project.category = form.category.data
        project.description = form.description.data or ''
        project.location = form.location.data or ''
        project.year = form.year.data or ''
        project.featured = form.featured.data
        project.order = form.order.data or 0
        filename = save_upload(request.files.get('image'))
        if filename:
            if project.image:
                old_file = os.path.join(current_app.config['UPLOAD_FOLDER'], project.image)
                if os.path.exists(old_file):
                    os.remove(old_file)
            project.image = filename
        db.session.commit()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('admin.projects'))
    return render_template('admin/project_form.html', form=form, project=project)

@admin_bp.route('/projects/delete/<int:id>', methods=['POST'])
@login_required
def project_delete(id):
    project = Project.query.get_or_404(id)
    if project.image:
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], project.image)
        if os.path.exists(file_path):
            os.remove(file_path)
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted.', 'info')
    return redirect(url_for('admin.projects'))

# --- Services ---
@admin_bp.route('/services')
@login_required
def services():
    all_services = Service.query.order_by(Service.order).all()
    return render_template('admin/services.html', services=all_services)

@admin_bp.route('/services/new', methods=['GET', 'POST'])
@login_required
def service_new():
    form = ServiceForm()
    if form.validate_on_submit():
        service = Service(
            title=form.title.data,
            description=form.description.data,
            icon_name=form.icon_name.data,
            order=form.order.data or 0,
            active=form.active.data
        )
        db.session.add(service)
        db.session.commit()
        flash('Service created successfully!', 'success')
        return redirect(url_for('admin.services'))
    return render_template('admin/service_form.html', form=form, service=None)

@admin_bp.route('/services/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def service_edit(id):
    service = Service.query.get_or_404(id)
    form = ServiceForm(obj=service)
    if form.validate_on_submit():
        service.title = form.title.data
        service.description = form.description.data
        service.icon_name = form.icon_name.data
        service.order = form.order.data or 0
        service.active = form.active.data
        db.session.commit()
        flash('Service updated successfully!', 'success')
        return redirect(url_for('admin.services'))
    return render_template('admin/service_form.html', form=form, service=service)

@admin_bp.route('/services/delete/<int:id>', methods=['POST'])
@login_required
def service_delete(id):
    service = Service.query.get_or_404(id)
    db.session.delete(service)
    db.session.commit()
    flash('Service deleted.', 'info')
    return redirect(url_for('admin.services'))

# --- Team ---
@admin_bp.route('/team')
@login_required
def team():
    members = TeamMember.query.order_by(TeamMember.order).all()
    return render_template('admin/team.html', members=members)

@admin_bp.route('/team/new', methods=['GET', 'POST'])
@login_required
def team_new():
    form = TeamForm()
    if form.validate_on_submit():
        member = TeamMember(
            name=form.name.data,
            title=form.title.data or '',
            bio=form.bio.data or '',
            credentials=form.credentials.data or '',
            license_no=form.license_no.data or '',
            experience=form.experience.data or '',
            registered_in=form.registered_in.data or '',
            is_lead=form.is_lead.data,
            order=form.order.data or 0
        )
        filename = save_upload(request.files.get('image'))
        if filename:
            member.image = filename
        db.session.add(member)
        db.session.commit()
        flash('Team member added successfully!', 'success')
        return redirect(url_for('admin.team'))
    return render_template('admin/team_form.html', form=form, member=None)

@admin_bp.route('/team/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def team_edit(id):
    member = TeamMember.query.get_or_404(id)
    form = TeamForm(obj=member)
    if form.validate_on_submit():
        member.name = form.name.data
        member.title = form.title.data or ''
        member.bio = form.bio.data or ''
        member.credentials = form.credentials.data or ''
        member.license_no = form.license_no.data or ''
        member.experience = form.experience.data or ''
        member.registered_in = form.registered_in.data or ''
        member.is_lead = form.is_lead.data
        member.order = form.order.data or 0
        filename = save_upload(request.files.get('image'))
        if filename:
            if member.image:
                old_file = os.path.join(current_app.config['UPLOAD_FOLDER'], member.image)
                if os.path.exists(old_file):
                    os.remove(old_file)
            member.image = filename
        db.session.commit()
        flash('Team member updated successfully!', 'success')
        return redirect(url_for('admin.team'))
    return render_template('admin/team_form.html', form=form, member=member)

@admin_bp.route('/team/delete/<int:id>', methods=['POST'])
@login_required
def team_delete(id):
    member = TeamMember.query.get_or_404(id)
    if member.image:
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], member.image)
        if os.path.exists(file_path):
            os.remove(file_path)
    db.session.delete(member)
    db.session.commit()
    flash('Team member deleted.', 'info')
    return redirect(url_for('admin.team'))

# --- Messages ---
@admin_bp.route('/messages')
@login_required
def messages():
    all_messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template('admin/messages.html', messages=all_messages)

@admin_bp.route('/messages/read/<int:id>')
@login_required
def message_read(id):
    message = ContactMessage.query.get_or_404(id)
    message.is_read = True
    db.session.commit()
    return redirect(url_for('admin.messages'))

@admin_bp.route('/messages/delete/<int:id>', methods=['POST'])
@login_required
def message_delete(id):
    message = ContactMessage.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    flash('Message deleted.', 'info')
    return redirect(url_for('admin.messages'))

# --- Blog ---
@admin_bp.route('/blog')
@login_required
def blog():
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    return render_template('admin/blog.html', posts=posts)

@admin_bp.route('/blog/new', methods=['GET', 'POST'])
@login_required
def blog_new():
    form = BlogForm()
    if form.validate_on_submit():
        post = BlogPost(
            title=form.title.data,
            slug=form.slug.data,
            content=form.content.data,
            excerpt=form.excerpt.data or '',
            author=form.author.data or 'Admin',
            published=form.published.data
        )
        filename = save_upload(request.files.get('image'))
        if filename:
            post.image = filename
        db.session.add(post)
        db.session.commit()
        flash('Blog post created!', 'success')
        return redirect(url_for('admin.blog'))
    return render_template('admin/blog_form.html', form=form, post=None)

@admin_bp.route('/blog/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def blog_edit(id):
    post = BlogPost.query.get_or_404(id)
    form = BlogForm(obj=post)
    if form.validate_on_submit():
        post.title = form.title.data
        post.slug = form.slug.data
        post.content = form.content.data
        post.excerpt = form.excerpt.data or ''
        post.author = form.author.data or 'Admin'
        post.published = form.published.data
        filename = save_upload(request.files.get('image'))
        if filename:
            if post.image:
                old_file = os.path.join(current_app.config['UPLOAD_FOLDER'], post.image)
                if os.path.exists(old_file):
                    os.remove(old_file)
            post.image = filename
        db.session.commit()
        flash('Blog post updated!', 'success')
        return redirect(url_for('admin.blog'))
    return render_template('admin/blog_form.html', form=form, post=post)

@admin_bp.route('/blog/delete/<int:id>', methods=['POST'])
@login_required
def blog_delete(id):
    post = BlogPost.query.get_or_404(id)
    if post.image:
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], post.image)
        if os.path.exists(file_path):
            os.remove(file_path)
    db.session.delete(post)
    db.session.commit()
    flash('Blog post deleted.', 'info')
    return redirect(url_for('admin.blog'))

# --- Settings ---
@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = SiteSettingForm()
    if form.validate_on_submit():
        for key in ['site_name', 'site_email', 'site_phone', 'site_address', 'site_hours']:
            value = getattr(form, key).data or ''
            SiteSetting.set(key, value)
        flash('Settings updated!', 'success')
        return redirect(url_for('admin.settings'))

    form.site_name.data = SiteSetting.get('site_name')
    form.site_email.data = SiteSetting.get('site_email')
    form.site_phone.data = SiteSetting.get('site_phone')
    form.site_address.data = SiteSetting.get('site_address')
    form.site_hours.data = SiteSetting.get('site_hours')
    return render_template('admin/settings.html', form=form)
