# app.py / version-6.4 /
import os
from collections import defaultdict
from time import monotonic
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, Response, flash, send_file, jsonify
from flask_cors import CORS
from backend import data_manager
from backend import project_ops
import csv
import io

RATE_LIMIT_WINDOW_SECONDS = int(os.getenv('RATE_LIMIT_WINDOW_SECONDS', '60'))
RATE_LIMIT_MAX_REQUESTS = int(os.getenv('RATE_LIMIT_MAX_REQUESTS', '60'))
REQUEST_LOG = defaultdict(list)

# Use absolute paths for template and static folders to avoid ambiguity when importing the app
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_FOLDER = os.path.join(BASE_DIR, 'frontend', 'templates')
STATIC_FOLDER = os.path.join(BASE_DIR, 'frontend', 'static')
app = Flask(__name__, template_folder=TEMPLATE_FOLDER, static_folder=STATIC_FOLDER)
# Configure CORS with an environment-driven whitelist (default: local dev frontend)
ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', 'http://localhost:8443')
# Support comma-separated list
origins = [o.strip() for o in ALLOWED_ORIGINS.split(',') if o.strip()]
# Apply CORS only to API routes for least privilege
CORS(app, resources={r"/api/*": {"origins": origins}}, supports_credentials=True)
# Load SECRET_KEY from environment to avoid hardcoded secrets
ENVIRONMENT = os.getenv('FLASK_ENV', 'development')
SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    if ENVIRONMENT != 'development':
        raise RuntimeError('SECRET_KEY must be set in environment for non-development environments')
    # Development fallback (do NOT use in production)
    SECRET_KEY = 'dev-secret-key-6.4'
    print('WARNING: Using development SECRET_KEY fallback. Set SECRET_KEY in the environment for production.')
app.secret_key = SECRET_KEY

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RATE_LIMIT_WINDOW_SECONDS'] = RATE_LIMIT_WINDOW_SECONDS
app.config['RATE_LIMIT_MAX_REQUESTS'] = RATE_LIMIT_MAX_REQUESTS
# File upload hardening
# Default max content length: 16 MB (can be reduced in production)
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', str(16 * 1024 * 1024)))
# Allowed extensions (comma-separated environment override)
ALLOWED_EXTENSIONS = set([e.strip().lower() for e in os.getenv('ALLOWED_EXTENSIONS', 'png,jpg,jpeg,gif,pdf,txt,md').split(',') if e.strip()])

def allowed_file(filename):
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in ALLOWED_EXTENSIONS

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def get_client_identifier():
    forwarded_for = request.headers.get('X-Forwarded-For')
    if forwarded_for:
        return forwarded_for.split(',')[0].strip()
    return request.remote_addr or 'unknown'


@app.after_request
def set_security_headers(response):
    # Basic security headers — adjust CSP as needed for app assets
    response.headers.setdefault('X-Content-Type-Options', 'nosniff')
    response.headers.setdefault('X-Frame-Options', 'DENY')
    response.headers.setdefault('Referrer-Policy', 'same-origin')
    # Minimal CSP: allow same-origin for scripts/styles; block inline by default
    csp = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:;"
    response.headers.setdefault('Content-Security-Policy', csp)
    return response


@app.before_request
def enforce_rate_limit():
    if not request.path.startswith('/api'):
        return None

    if request.method == 'OPTIONS':
        return None

    client_id = get_client_identifier()
    now = monotonic()
    timestamps = REQUEST_LOG[client_id]
    timestamps[:] = [stamp for stamp in timestamps if now - stamp < RATE_LIMIT_WINDOW_SECONDS]

    if len(timestamps) >= RATE_LIMIT_MAX_REQUESTS:
        return jsonify({
            'status': 'error',
            'message': 'Rate limit exceeded. Please wait a moment before trying again.'
        }), 429

    timestamps.append(now)
    return None

@app.route('/', methods=['GET'])
def home():
    app_title = "Project Management system"
    return render_template('index.html', dynamic_title=app_title)

@app.route('/api/attachments/upload/<int:project_id>', methods=['POST'])
def api_upload_attachment(project_id):
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No file provided"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"status": "error", "message": "No file provided"}), 400
    if file:
        filename = secure_filename(file.filename)
        if not allowed_file(filename):
            return jsonify({"status": "error", "message": "File type not allowed"}), 400
        # Additional server-side size check (Flask will already enforce MAX_CONTENT_LENGTH)
        file.seek(0, os.SEEK_END)
        file_length = file.tell()
        file.seek(0)
        if file_length > app.config['MAX_CONTENT_LENGTH']:
            return jsonify({"status": "error", "message": "File too large"}), 413
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        data_manager.add_attachment_record(project_id, filename, file_path)
        return jsonify({"status": "success", "message": "File uploaded successfully", "file_name": filename})

@app.route('/api/attachments/download/<int:attachment_id>', methods=['GET'])
def api_download_attachment(attachment_id):
    attachment = data_manager.get_attachment_by_id(attachment_id)

    if not attachment:
        return jsonify({"status": "error", "message": "File not found"}), 404

    file_path = attachment['file_path']
    file_name = attachment['file_name']

    return send_file(file_path, as_attachment=True, download_name=file_name)

@app.route('/project/<int:project_id>', methods=['GET'])
def view_project(project_id):
    project = data_manager.get_project_by_id(project_id)
    if not project:
        return redirect(url_for('home'))

    return render_template('project_details.html', project=project)

@app.route('/delete_project/<int:project_id>', methods=['POST'])
def delete_project(project_id):
    project_ops.delete_project_web(project_id)
    return redirect(url_for('home'))

@app.route('/update_project_status/<int:project_id>', methods=['POST'])
def update_project_status(project_id):
    data = request.get_json()
    new_status = data.get('status')
    if new_status:
        data_manager.update_project_status(project_id, new_status)
        return jsonify({"status": "success", "new_status": new_status})
    return jsonify({"status": "error", "message": "No status provided"}), 400

@app.route('/toggle_task/<int:task_id>/<int:project_id>', methods=['POST'])
def toggle_task(task_id, project_id):
    project_ops.toggle_task_web(task_id)
    return jsonify({"status": "success"})

@app.route('/delete_task/<int:task_id>/<int:project_id>', methods=['POST'])
def delete_task(task_id, project_id):
    project_ops.delete_task_web(task_id)
    return jsonify({"status": "success"})

@app.route('/export_csv')
def export_csv():
    rows = project_ops.get_export_data_web()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Project Title', 'Task Title', 'Status'])
    for row in rows:
        title, desc, completed = row[0], row[1], row[2]

        if completed is None:
            status = 'No Tasks'
            desc = 'N/A'
        else:
            status = 'Completed' if completed == 1 else 'Pending'

        writer.writerow([title, desc, status])
    output.seek(0)

    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=projects_export.csv'}
    )

@app.route('/upload_file/<int:project_id>', methods=['POST'])
def upload_file(project_id):
    if 'file' not in request.files:
        flash("No File part")
        return redirect(url_for('view_project', project_id=project_id))
    file = request.files['file']

    if file.filename == '':
        flash("No Selected File")
        return redirect(url_for('view_project', project_id=project_id))

    if file:
        filename = secure_filename(file.filename)
        if not allowed_file(filename):
            flash("File type not allowed")
            return redirect(url_for('view_project', project_id=project_id))
        # server-side size check
        file.seek(0, os.SEEK_END)
        file_length = file.tell()
        file.seek(0)
        if file_length > app.config['MAX_CONTENT_LENGTH']:
            flash("File too large")
            return redirect(url_for('view_project', project_id=project_id))
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        data_manager.add_attachment_record(project_id, filename, file_path)
        flash("File successfully uploaded!")
    return redirect(url_for('view_project', project_id=project_id))

@app.route('/download_file/<int:attachment_id>')
def download_file(attachment_id):
    attachment = data_manager.get_attachment_by_id(attachment_id)
    if attachment:
        return send_file(attachment['file_path'], as_attachment=True)

    flash("File not found.")
    return redirect(url_for('home'))

@app.route('/add_task/<int:project_id>', methods=['POST'])
def add_task(project_id):
    if request.is_json:
        data = request.get_json()
        title = data.get('title')
        description = data.get('description', '')
        assignee_id = data.get('assigneeId', 'm1')
        priority = data.get('priority', 'low')
        status = data.get('status', 'backlog')
        due_date = data.get('dueDate', '')
    else:
        title = request.form.get('task_title')
        description = request.form.get('task_description', '')
        assignee_id = request.form.get('assignee_id', 'm1')
        priority = request.form.get('task_priority', 'low')
        status = request.form.get('status', 'backlog')
        due_date = request.form.get('task_due_date', '')

    if title:
        result = project_ops.add_task_full(project_id, title, description, assignee_id, priority, status, due_date)
        if isinstance(result, int):
            return jsonify({
                "status": "success",
                "task_id": result,
                "title": title,
                "priority": priority,
                "status": status,
                "due_date": due_date
            })
        return jsonify({"status": "error", "message": result}), 400
    return jsonify({"status": "error", "message": "Missing title"}), 400

@app.route('/api/tasks/<int:project_id>', methods=['GET'])
def api_get_tasks(project_id):
    sort_by = request.args.get('sort')
    tasks = data_manager.get_tasks_for_project(project_id, sort_by)
    tasks_data = [dict(task) for task in tasks]
    return jsonify({"status": "success", "tasks": tasks_data})

@app.route('/api/projects', methods=['GET', 'POST'])
def api_get_projects():
    if request.method == 'POST':
        data = request.get_json()
        new_title = data.get('title')
        new_status = data.get('status')

        result = project_ops.create_project_web(new_title, new_status)

        if result != "SUCCESS":
            return jsonify({"status": "error", "message": result}), 400

        return jsonify({"status": "success", "message": "Project created successfully"})

    projects = data_manager.get_all_projects()
    projects_data = [dict(project) for project in projects]
    return jsonify({"status": "success", "projects": projects_data})

@app.route('/api/attachments/<int:project_id>', methods=['GET'])
def api_get_attachments(project_id):
    attachments = data_manager.get_attachments_for_project(project_id)
    attachments_data = [dict(file) for file in attachments]
    return jsonify({"status": "success", "attachments": attachments_data})

@app.route('/api/stats', methods=['GET'])
def api_get_stats():
    stats = project_ops.get_statistics_web()
    return jsonify({"status": "success", "stats": stats})

@app.route('/api/projects/<int:project_id>/description', methods=['POST'])
def api_update_description(project_id):
    data = request.get_json()
    description = data.get('description', '')
    project_ops.update_project_description_web(project_id, description)
    return jsonify({"status": "success", "message": "Description updated"})

if __name__ == '__main__':
    # Control debug mode via environment variable; prevent debug in non-development environments
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() in ('1', 'true', 'yes')
    if DEBUG and ENVIRONMENT != 'development':
        raise RuntimeError('Refusing to start with debug enabled in non-development environment')
    app.run(debug=DEBUG)