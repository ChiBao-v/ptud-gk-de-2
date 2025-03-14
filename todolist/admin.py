from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, db
import random
import string

admin_bp = Blueprint('admin', __name__)  # Đổi tên biến


@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password) and user.is_admin:
            login_user(user)
            flash('Đăng nhập admin thành công!', 'success')
            return redirect(url_for('admin.admin_users'))
        flash('Email, mật khẩu không đúng hoặc bạn không phải admin!', 'error')
    return render_template('admin_login.html', user=current_user)

@admin_bp.route('/users', methods=['GET'])
@login_required
def admin_users():
    if not current_user.is_admin:
        flash('Bạn không có quyền truy cập!', 'error')
        return redirect(url_for('views.home'))
    users = User.query.all()
    return render_template('admin_users.html', users=users)

@admin_bp.route('/block_user/<int:user_id>', methods=['POST'])
@login_required
def block_user(user_id):
    if not current_user.is_admin:
        flash('Bạn không có quyền truy cập!', 'error')
        return redirect(url_for('views.home'))
    user = User.query.get_or_404(user_id)
    user.is_blocked = not user.is_blocked
    db.session.commit()
    flash(f'Đã {"khóa" if user.is_blocked else "mở khóa"} tài khoản {user.user_name}!', 'success')
    return redirect(url_for('admin.admin_users'))

@admin_bp.route('/reset_password/<int:user_id>', methods=['POST'])
@login_required
def reset_password(user_id):
    if not current_user.is_admin:
        flash('Bạn không có quyền truy cập!', 'error')
        return redirect(url_for('views.home'))
    user = User.query.get_or_404(user_id)
    new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    user.password = generate_password_hash(new_password)
    db.session.commit()
    flash(f'Mật khẩu mới cho {user.user_name}: {new_password}', 'success')
    return redirect(url_for('admin.admin_users'))