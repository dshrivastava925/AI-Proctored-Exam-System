from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from datetime import datetime, timedelta


# Initialize SQLAlchemy
db = SQLAlchemy()
login_Manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize Flask extensions
    db.init_app(app)
    login_Manager.init_app(app)
    login_Manager.login_view = 'auth.login'
    
    # Register blueprints
    from app.routes.main import bp as main_bp
    from app.routes.auth import bp as auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    
    # Create database tables
    with app.app_context():
        # Import models here to avoid circular imports
        from app.models.user import User
        from app.models.course import Course
        from app.models.exam import Exam
        
        db.create_all()
        
        # Add sample data if database is empty
        if not User.query.first():
            create_sample_data(User, Course, Exam)
    
    return app

@login_Manager.user_loader
def load_user(id):
    from app.models.user import User
    return User.query.get(int(id))

def create_sample_data(User, Course, Exam):
    try:
        # Create sample admin
        admin = User(username='admin', email='admin@example.com', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Create sample student
        student = User(username='student', email='student@example.com', role='student')
        student.set_password('student123')
        db.session.add(student)
        
        # Create sample courses
        courses = [
            Course(code='MATH101', name='Mathematics', description='Basic Mathematics Course'),
            Course(code='PHY101', name='Physics', description='Introduction to Physics'),
            Course(code='CS101', name='Computer Science', description='Programming Fundamentals')
        ]
        for course in courses:
            db.session.add(course)
        
        db.session.commit()
        
        # Create sample exams
        exams = [
            Exam(
                title='Mathematics Mid-term',
                description='Mid-term examination for Mathematics',
                date=datetime.now() + timedelta(days=7),
                duration=120,
                course_id=1
            ),
            Exam(
                title='Physics Quiz',
                description='First quiz for Physics',
                date=datetime.now() + timedelta(days=5),
                duration=60,
                course_id=2
            )
        ]
        for exam in exams:
            db.session.add(exam)
        
        db.session.commit()
        print("Sample data created successfully!")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.session.rollback()