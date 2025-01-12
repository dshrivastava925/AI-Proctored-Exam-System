from flask import Blueprint, render_template
from app.models import Exam, Course  # Updated import
from datetime import datetime

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    # Get upcoming exams
    upcoming_exams = Exam.query.filter(
        Exam.date > datetime.now()
    ).order_by(Exam.date.asc()).limit(5).all()
    
    # Get all courses
    courses = Course.query.all()
    
    return render_template('index.html', 
                         upcoming_exams=upcoming_exams,
                         courses=courses)