from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, timedelta
import json
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    resumes = db.relationship('Resume', backref='user', lazy=True, cascade='all, delete-orphan')
    plans = db.relationship('Plan', backref='user', lazy=True, cascade='all, delete-orphan')
    progress = db.relationship('Progress', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password against hash"""
        return check_password_hash(self.password_hash, password)


class Resume(db.Model):
    __tablename__ = 'resumes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    
    # Extracted resume data
    skills = db.Column(db.JSON, default=list)  # ['Python', 'SQL', 'JavaScript']
    experience_level = db.Column(db.String(50), default='beginner')  # beginner, intermediate, advanced
    years_of_experience = db.Column(db.Float, default=0)
    current_role = db.Column(db.String(255))
    education = db.Column(db.String(255))
    
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Plan(db.Model):
    __tablename__ = 'plans'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'), nullable=False)
    
    # Plan details
    goal = db.Column(db.String(255), nullable=False)  # "Become Software Engineer"
    duration_months = db.Column(db.Integer, nullable=False)  # 6
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=False)
    
    # Plan content
    daily_tasks = db.Column(db.JSON, default=list)  # [{day: 1, task: "", duration_hours: 2}, ...]
    milestones = db.Column(db.JSON, default=list)  # [{week: 2, milestone: "Complete Python basics"}, ...]
    technologies = db.Column(db.JSON, default=list)  # Technologies to learn
    
    status = db.Column(db.String(50), default='active')  # active, completed, paused, updated
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    version = db.Column(db.Integer, default=1)  # Track plan versions for updates
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    daily_progress = db.relationship('DailyProgress', backref='plan', lazy=True, cascade='all, delete-orphan')


class Progress(db.Model):
    __tablename__ = 'progress'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    total_days_planned = db.Column(db.Integer, default=0)
    total_days_completed = db.Column(db.Integer, default=0)
    completion_percentage = db.Column(db.Float, default=0.0)
    
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class DailyProgress(db.Model):
    __tablename__ = 'daily_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.id'), nullable=False)
    
    day_number = db.Column(db.Integer, nullable=False)
    task = db.Column(db.Text, nullable=False)
    planned_date = db.Column(db.DateTime, nullable=False)
    
    is_completed = db.Column(db.Boolean, default=False)
    completed_date = db.Column(db.DateTime)
    hours_spent = db.Column(db.Float, default=0)
    notes = db.Column(db.Text)  # User notes on task completion
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TechTrend(db.Model):
    __tablename__ = 'tech_trends'
    
    id = db.Column(db.Integer, primary_key=True)
    technology_name = db.Column(db.String(255), unique=True, nullable=False)
    category = db.Column(db.String(100))  # 'llm', 'framework', 'tool', etc.
    relevance_score = db.Column(db.Float, default=0.0)  # 0-100
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    description = db.Column(db.Text)
    learn_resources = db.Column(db.JSON, default=list)  # Links to learning resources
