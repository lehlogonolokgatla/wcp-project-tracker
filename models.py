# wcp_tracker/models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    head_name = db.Column(db.String(150), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to indicators
    indicators = db.relationship('APPIndicator', back_populates='department', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Department {self.name}>'


class APPIndicator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    indicator_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    # NOTE: Assuming target_value is the *quarterly* target for simplicity.
    # For annual targets, logic would need to adjust (e.g., divide by 4).
    target_value = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(50), nullable=False)  # e.g., "Percentage", "Number", "Rand"

    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    department = db.relationship('Department', back_populates='indicators')

    # Relationship to submissions
    submissions = db.relationship('QuarterlySubmission', back_populates='indicator', lazy=True,
                                  cascade="all, delete-orphan")

    def __repr__(self):
        return f'<APPIndicator {self.indicator_name}>'


class QuarterlySubmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quarter = db.Column(db.Integer, nullable=False)  # 1, 2, 3, or 4
    year = db.Column(db.Integer, nullable=False)
    actual_value = db.Column(db.Float, nullable=False)
    submitted_by = db.Column(db.String(150), nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

    indicator_id = db.Column(db.Integer, db.ForeignKey('app_indicator.id'), nullable=False)
    indicator = db.relationship('APPIndicator', back_populates='submissions')

    # Relationship to flags
    flags = db.relationship('ComplianceFlag', back_populates='submission', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Submission Q{self.quarter} {self.year} for Indicator {self.indicator_id}>'


class ComplianceFlag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flag_type = db.Column(db.String(50), nullable=False)  # e.g., "Underperformance", "Late Submission"
    description = db.Column(db.Text, nullable=False)
    resolved = db.Column(db.Boolean, default=False, nullable=False)

    submission_id = db.Column(db.Integer, db.ForeignKey('quarterly_submission.id'), nullable=False)
    submission = db.relationship('QuarterlySubmission', back_populates='flags')

    def __repr__(self):
        return f'<Flag {self.flag_type} for Submission {self.submission_id}>'