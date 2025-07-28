# wcp_tracker/data/seed_data.py
# This file now only contains the logic, not the execution context.
from models import db, Department, APPIndicator

def seed():
    # The app context is provided by the Flask CLI command that calls this function.
    print("Clearing old data...")
    db.drop_all()
    db.create_all()

    print("Seeding new data...")

    # Create Departments
    d1 = Department(name="Department of Health", email="health@wcp.gov", head_name="Dr. Wellness")
    d2 = Department(name="Department of Education", email="edu@wcp.gov", head_name="Prof. Knowledge")
    d3 = Department(name="Department of Transport", email="transport@w.gov", head_name="Mr. Wheeler")

    db.session.add_all([d1, d2, d3])
    db.session.commit()

    # Create Indicators
    i1 = APPIndicator(department_id=d1.id, indicator_name="Hospital bed occupancy rate",
                      description="Percentage of available beds that are occupied.", target_value=85.0,
                      unit="Percentage")
    i2 = APPIndicator(department_id=d1.id, indicator_name="Number of new nurses hired",
                      description="Total new nurses appointed in the quarter.", target_value=50, unit="Number")
    i3 = APPIndicator(department_id=d2.id, indicator_name="Learner-to-educator ratio",
                      description="Average ratio of learners to educators in public schools.", target_value=35.0,
                      unit="Ratio")
    i4 = APPIndicator(department_id=d3.id, indicator_name="On-time performance of public buses",
                      description="Percentage of buses arriving within 5 minutes of schedule.", target_value=90.0,
                      unit="Percentage")

    db.session.add_all([i1, i2, i3, i4])
    db.session.commit()

    print("Database has been seeded successfully!")

# The if __name__ == '__main__': block has been removed.