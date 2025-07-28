# wcp_tracker/app.py
import os
import pandas as pd
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from models import db, Department, APPIndicator, QuarterlySubmission, ComplianceFlag
from forms import DepartmentForm, IndicatorForm, SubmissionForm

# --- App Configuration ---
app = Flask(__name__)
# IMPORTANT: For production, use environment variables for the secret key
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a-very-secret-key-that-is-not-secure')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wcp_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


# --- Helper Functions ---
def check_and_create_flags(submission):
    """Business logic to generate compliance flags."""
    indicator = submission.indicator
    if submission.actual_value < indicator.target_value:
        flag = ComplianceFlag(
            submission_id=submission.id,
            flag_type="Underperformance",
            description=f"Actual value ({submission.actual_value}) is below target ({indicator.target_value})."
        )
        db.session.add(flag)

    quarter_end_month = submission.quarter * 3
    if quarter_end_month == 12:
        deadline_date = datetime(submission.year + 1, 1, 30)  # Approx. Jan 30th
    else:
        # A simple way to get end of month, then add 30 days
        deadline_date = datetime(submission.year, quarter_end_month + 1, 1) + timedelta(days=29)

    if submission.submitted_at.date() > deadline_date.date():
        flag = ComplianceFlag(
            submission_id=submission.id,
            flag_type="Late Submission",
            description=f"Submitted on {submission.submitted_at.strftime('%Y-%m-%d')}, after deadline of {deadline_date.strftime('%Y-%m-%d')}."
        )
        db.session.add(flag)

    db.session.commit()


# --- Routes ---
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/admin')
def admin_dashboard():
    departments = Department.query.order_by(Department.name).all()
    indicators = APPIndicator.query.join(Department).order_by(Department.name, APPIndicator.indicator_name).all()
    return render_template('admin_dashboard.html', departments=departments, indicators=indicators)


@app.route('/admin/department/add', methods=['GET', 'POST'])
def add_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        new_dept = Department(name=form.name.data, email=form.email.data, head_name=form.head_name.data)
        db.session.add(new_dept)
        db.session.commit()
        flash('Department added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('department_form.html', form=form, title="Add Department")


@app.route('/admin/indicator/add', methods=['GET', 'POST'])
def add_indicator():
    form = IndicatorForm()
    if form.validate_on_submit():
        new_indicator = APPIndicator(
            department_id=form.department.data.id,
            indicator_name=form.indicator_name.data,
            description=form.description.data,
            target_value=form.target_value.data,
            unit=form.unit.data
        )
        db.session.add(new_indicator)
        db.session.commit()
        flash('Indicator added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('indicator_form.html', form=form, title="Add Indicator")


@app.route('/submit/<int:indicator_id>', methods=['GET', 'POST'])
def submit_performance(indicator_id):
    indicator = APPIndicator.query.get_or_404(indicator_id)
    form = SubmissionForm()
    if form.validate_on_submit():
        submission = QuarterlySubmission(
            indicator_id=indicator.id,
            quarter=form.quarter.data,
            year=form.year.data,
            actual_value=form.actual_value.data,
            submitted_by=form.submitted_by.data
        )
        db.session.add(submission)
        db.session.commit()
        check_and_create_flags(submission)
        flash(f'Submission for "{indicator.indicator_name}" received!', 'success')
        return redirect(url_for('submissions_list'))
    return render_template('submission_form.html', form=form, indicator=indicator, title="Submit Performance")


@app.route('/submissions')
def submissions_list():
    submissions = db.session.query(QuarterlySubmission).join(APPIndicator).join(Department).order_by(
        QuarterlySubmission.submitted_at.desc()).all()
    return render_template('submissions_list.html', submissions=submissions)


@app.route('/export/csv')
def export_csv():
    query = db.session.query(
        QuarterlySubmission.id.label('submission_id'), QuarterlySubmission.year, QuarterlySubmission.quarter,
        Department.name.label('department_name'), APPIndicator.indicator_name,
        APPIndicator.target_value.label('quarterly_target'), QuarterlySubmission.actual_value,
        QuarterlySubmission.submitted_by, QuarterlySubmission.submitted_at,
        ComplianceFlag.flag_type, ComplianceFlag.description.label('flag_description')
    ).join(APPIndicator, QuarterlySubmission.indicator_id == APPIndicator.id) \
        .join(Department, APPIndicator.department_id == Department.id) \
        .outerjoin(ComplianceFlag, QuarterlySubmission.id == ComplianceFlag.submission_id).statement

    df = pd.read_sql_query(query, db.engine)
    export_dir = 'exports'
    os.makedirs(export_dir, exist_ok=True)
    filepath = os.path.join(export_dir, f"submissions_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
    df.to_csv(filepath, index=False)
    flash(f'Successfully created export file. Ready for download.', 'info')
    return send_file(filepath, as_attachment=True, download_name='wcp_submissions_export.csv')


# +++ NEW SECTION FOR THE CLI COMMAND +++
@app.cli.command("seed-db")
def seed_database():
    """Clears existing data and seeds the database with test data."""
    # We import the seed function here to avoid circular import issues.
    from data.seed_data import seed
    seed()


# +++ END OF NEW SECTION +++


if __name__ == '__main__':
    # This block is useful for running with a debugger
    # For production, use a proper WSGI server like Gunicorn or Waitress
    with app.app_context():
        db.create_all()
    app.run(debug=True)