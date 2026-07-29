from flask import Flask, render_template, request, redirect, url_for
from backend import data_manager
from backend import project_ops

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
    return render_template('index.html', dynamic_title=app_title, projects=live_projects)

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

if __name__ == '__main__':
    app.run(debug=True)