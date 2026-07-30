# app.py / version-4.1 /
from flask import Flask, render_template, request, redirect, url_for, Response
from backend import data_manager
from backend import project_ops
import csv
import io

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        new_title = request.form.get('title')
        new_status = request.form.get('status')
        
        result = project_ops.create_project_web(new_title, new_status)
        
        if result != "SUCCESS":
            print(result)
        
        return redirect(url_for('home'))
    
    app_title = "Project Manager 4.0 Core Web Interface"
    live_projects = data_manager.get_all_projects()
    stats = project_ops.get_statistics_web()
    return render_template('index.html', dynamic_title=app_title, projects=live_projects, stats=stats)

@app.route('/project/<int:project_id>', methods=['GET', 'POST'])
def view_project(project_id):
    error_msg = None

    if request.method == 'POST':
        task_title = request.form.get('task_title')
        task_priority = request.form.get('task_priority')
        task_due_date = request.form.get('task_due_date')

        result = project_ops.add_task_web(project_id, task_title, task_priority, task_due_date)

        if result != "SUCCESS":
            error_msg = result
        else:
            return redirect(url_for('view_project', project_id=project_id))
    
    project = data_manager.get_project_by_id(project_id)
    if not project:
        return redirect(url_for('home'))
    tasks = data_manager.get_tasks_for_project(project_id)
    return render_template('project_details.html', project=project, tasks=tasks)

@app.route('/delete_project/<int:project_id>', methods=['POST'])
def delete_project(project_id):
    project_ops.delete_project_web(project_id)
    return redirect(url_for('home'))

@app.route('/update_project_status/<int:project_id>', methods=['POST'])
def update_project_status(project_id):
    new_status = request.form.get('project_status')
    if new_status:
        project_ops.change_project_status_web(project_id, new_status)
    return redirect(url_for('view_project', project_id=project_id))

@app.route('/toggle_task/<int:task_id>/<int:project_id>', methods=['POST'])
def toggle_task(task_id, project_id):
    project_ops.toggle_task_web(task_id)
    return redirect(url_for('view_project', project_id=project_id))

@app.route('/delete_task/<int:task_id>/<int:project_id>', methods=['POST'])
def delete_task(task_id, project_id):
    project_ops.delete_task_web(task_id)
    return redirect(url_for('view_project', project_id=project_id))

@app.route('/export_csv')
def export_csv():
    rows = project_ops.get_export_data_web()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(['Project Title', 'Task Description', 'Status'])

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

if __name__ == '__main__':
    app.run(debug=True)