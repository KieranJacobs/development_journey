# app.py / version-6.1 /
import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, Response, flash, send_file, jsonify
from flask_cors import CORS
from backend import data_manager
from backend import project_ops
import csv
import io

app = Flask(__name__,
            template_folder='frontend/templates',
            static_folder='frontend/static')
CORS(app)
app.secret_key = 'super_secret_key_6.1'

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET'])
def home():
    app_title = "Project Manager 6.1 Core Web Interface"
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
    title = request.form.get('task_title')
    priority = request.form.get('task_priority', 'Low')
    due_date = request.form.get('task_due_date', '')

    if title:
        result = project_ops.add_task_web(project_id, title, priority, due_date)

        if isinstance(result, int):
            return jsonify({
                "status": "success",
                "task_id": result,
                "title": title,
                "priority": priority,
                "due_date": due_date
            })
        else:
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
    app.run(debug=True)