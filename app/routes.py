# app/routes.py
from app.modules.auth.routes import auth_bp
from app.modules.employees.routes import employee_bp
from app.modules.attendance.routes import attendance_bp
from app.modules.reports.routes import report_bp


def register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(employee_bp, url_prefix="/api/employees")
    app.register_blueprint(attendance_bp, url_prefix="/api/attendance")
    app.register_blueprint(report_bp, url_prefix="/api/reports")
