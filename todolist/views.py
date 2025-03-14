from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, send_from_directory
from flask_login import login_required, current_user
from .models import Note, User  # Thêm User để cập nhật avatar
from . import db
import os
from werkzeug.utils import secure_filename
from PIL import Image
from flask import request, jsonify
from datetime import datetime

views = Blueprint("views", __name__)

# Thư mục lưu ảnh
UPLOAD_FOLDER = "static/uploads"
AVATAR_FOLDER = "static/avatars"

# Tạo thư mục nếu chưa có
for folder in [UPLOAD_FOLDER, AVATAR_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Định dạng ảnh cho phép
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Route hiển thị ảnh ghi chú
@views.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(os.path.abspath(UPLOAD_FOLDER), filename)

# Route hiển thị avatar
@views.route("/avatars/<filename>")
def uploaded_avatar(filename):
    return send_from_directory(os.path.abspath(AVATAR_FOLDER), filename)

# Kích thước tối đa của ảnh
MAX_WIDTH = 450  
MAX_HEIGHT = 250
AVATAR_SIZE = (150, 150)

@views.route("/home", methods=["GET", "POST"])
@views.route("/", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        note_text = request.form.get("note")
        due_date = request.form.get("due_date")  # Lấy hạn chót từ form
        image = request.files.get("image")

        image_filename = None
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            
            img = Image.open(image)
            img.thumbnail((MAX_WIDTH, MAX_HEIGHT))
            img.save(image_path)

            image_filename = filename

        if not note_text and not image_filename:
            flash("Ghi chú không được để trống!", category="error")
        else:
            new_note = Note(
                data=note_text.strip() if note_text else "",
                image=image_filename,
                user_id=current_user.id,
                due_date=datetime.strptime(due_date, "%Y-%m-%d") if due_date else None
            )
            db.session.add(new_note)
            db.session.commit()
            flash("Thêm ghi chú thành công!", category="success")

        return redirect(url_for("views.home"))

    # Lấy danh sách ghi chú của user
    notes = Note.query.filter_by(user_id=current_user.id).all()

    # Kiểm tra số lượng ghi chú bị trễ hạn
    overdue_notes = Note.query.filter(
        Note.user_id == current_user.id,
        Note.is_finished == False,
        Note.due_date < datetime.utcnow()
    ).count()

    return render_template("index.html", user=current_user, notes=notes, overdue_notes=overdue_notes)


@views.route("/delete-note", methods=["POST"])
@login_required
def delete_note():
    data = request.get_json()
    note_ids = data.get("note_ids", [])

    if not note_ids:
        return jsonify({"success": False, "message": "Chưa chọn ghi chú nào để xóa"}), 400

    notes = Note.query.filter(Note.id.in_(note_ids), Note.user_id == current_user.id).all()
    if not notes:
        return jsonify({"success": False, "message": "Không tìm thấy ghi chú nào hợp lệ"}), 404

    deleted_count = len(notes)
    for note in notes:
        # Xóa ảnh nếu có
        if note.image:
            image_path = os.path.join(UPLOAD_FOLDER, note.image)
            if os.path.exists(image_path):
                os.remove(image_path)
        db.session.delete(note)
    db.session.commit()

    flash(f"Đã xóa {deleted_count} ghi chú!", category="success")
    return jsonify({"success": True, "code": 200, "message": f"Đã xóa {deleted_count} ghi chú"})

@views.route("/update-note", methods=["POST"])
@login_required
def update_note():
    note_id = request.form.get("note_id")
    new_text = request.form.get("note")
    new_image = request.files.get("image")

    note = Note.query.get(note_id)

    if not note or note.user_id != current_user.id:
        return jsonify({"success": False, "message": "Không tìm thấy ghi chú hợp lệ"}), 404

    # Nếu có ảnh mới, xóa ảnh cũ trước khi cập nhật
    if new_image and allowed_file(new_image.filename):
        if note.image:
            old_image_path = os.path.join(UPLOAD_FOLDER, note.image)
            if os.path.exists(old_image_path):
                os.remove(old_image_path)

        filename = secure_filename(new_image.filename)
        new_image_path = os.path.join(UPLOAD_FOLDER, filename)

        img = Image.open(new_image)
        img.thumbnail((MAX_WIDTH, MAX_HEIGHT))
        img.save(new_image_path)

        note.image = filename  # Cập nhật ảnh mới

    # Cập nhật nội dung ghi chú
    note.data = new_text.strip() if new_text else note.data
    db.session.commit()

    flash("Ghi chú đã được cập nhật!", category="success")
    return redirect(url_for("views.home"))

# 🔹 **Upload Avatar**
@views.route("/upload-avatar", methods=["POST"])
@login_required
def upload_avatar():
    if "avatar" not in request.files:
        flash("Không có tệp nào được chọn!", category="error")
        return redirect(url_for("views.home"))

    avatar = request.files["avatar"]

    if avatar and allowed_file(avatar.filename):
        filename = secure_filename(avatar.filename)
        avatar_path = os.path.join(AVATAR_FOLDER, filename)

        img = Image.open(avatar)
        img.thumbnail(AVATAR_SIZE)
        img.save(avatar_path)

        # Cập nhật avatar trong database
        current_user.avatar = filename
        db.session.commit()

        flash("Cập nhật avatar thành công!", category="success")
    else:
        flash("Định dạng file không hợp lệ!", category="error")

    return redirect(url_for("views.home"))

@views.route("/finish_note/<int:note_id>", methods=["POST"])
@login_required
def finish_note(note_id):
    note = Note.query.get(note_id)
    if note and note.user_id == current_user.id:
        note.is_finished = True
        note.finished = datetime.now()
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"success": False})