# sportsbooking-app/app/admin.py
from flask import Blueprint, render_template, request, redirect, current_app
from flask_login import login_required, current_user
from .models import db, Booking, Availability, Image
import os, uuid, datetime as dt

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


# Helper
def _upload_dir() -> str:
    """Return the absolute path to the local uploads directory."""
    path = os.path.join(current_app.root_path, "static", "uploads")
    os.makedirs(path, exist_ok=True)
    return path


# Dashboard
@admin_bp.route("/", methods=["GET"])
@login_required
def dashboard():
    if current_user.role != "admin":
        return redirect("/member")

    bookings = Booking.query.all()
    avail = Availability.query.all()
    images = Image.query.order_by(Image.uploaded.desc()).all()

    return render_template(
        "admin.html",
        bookings=bookings,
        avail=avail,
        images=images,
    )


# Booking 
@admin_bp.post("/api/bookings/delete")
@login_required
def delete_booking():
    if current_user.role != "admin":
        return ("", 403)

    db.session.delete(Booking.query.get(request.form["booking_id"]))
    db.session.commit()
    return redirect("/admin")


# Availability 
@admin_bp.post("/api/avail/delete")
@login_required
def delete_avail():
    if current_user.role != "admin":
        return ("", 403)

    db.session.delete(Availability.query.get(request.form["avail_id"]))
    db.session.commit()
    return redirect("/admin")


@admin_bp.post("/api/avail/add")
@login_required
def add_avail():
    if current_user.role != "admin":
        return ("", 403)

    start = dt.datetime.fromisoformat(request.form["start"])
    end = dt.datetime.fromisoformat(request.form["end"])
    db.session.add(Availability(start_time=start, end_time=end))
    db.session.commit()
    return redirect("/admin")


# Image management (local disk)
@admin_bp.post("/api/images/upload")
@login_required
def upload_image():
    if current_user.role != "admin":
        return ("", 403)

    fileobj = request.files["file"]
    filename = f"{uuid.uuid4().hex}_{fileobj.filename}"
    file_path = os.path.join(_upload_dir(), filename)
    fileobj.save(file_path)

    db.session.add(Image(s3_key=f"uploads/{filename}"))
    db.session.commit()
    return redirect("/admin")


@admin_bp.post("/api/images/delete")
@login_required
def delete_image():
    if current_user.role != "admin":
        return ("", 403)

    img = Image.query.get(request.form["img_id"])
    try:
        os.remove(os.path.join(current_app.root_path, "static", img.s3_key))
    except FileNotFoundError:
        pass

    db.session.delete(img)
    db.session.commit()
    return redirect("/admin")
