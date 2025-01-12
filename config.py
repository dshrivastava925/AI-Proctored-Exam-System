class Config:
    SECRET_KEY = 'dev'  # Change this to a secure key in production
    SQLALCHEMY_DATABASE_URI = 'sqlite:///student_dashboard.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False