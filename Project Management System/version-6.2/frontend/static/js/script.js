// script.js/version-6.2
// event delegation for task list logic
const taskList = document.getElementById("task-list");

document.addEventListener("submit", async (e) => {
  // If delete form?
  if (e.target.classList.contains("delete-task-form")) {
    e.preventDefault();
    const form = e.target;

    const url = form.getAttribute("action");

    try {
      const data = await APIClient.deleteTask(url);

      if (data.status === "success") {
        form.closest("li").remove();
      }
    } catch (error) {
      console.error("Error deleting task:", error);
    }
  }

  // If toggle form?
  if (e.target.classList.contains("toggle-task-form")) {
    e.preventDefault();
    const form = e.target;
    const url = form.getAttribute("action");

    try {
      const data = await APIClient.toggleTask(url);

      if (data.status === "success") {
        const button = form.querySelector("button");
        if (button.innerText === "Complete") {
          button.innerText = "Undo";
        } else {
          button.innerText = "Complete";
        }

        location.reload();
      }
    } catch (error) {
      console.error("Error toggling task:", error);
    }
  }
});

// project status dropdown autosave
const statusDropdown = document.getElementById("project-status-dropdown");

if (statusDropdown) {
  statusDropdown.addEventListener("change", async (e) => {
    // get new value selected
    const newStatus = e.target.value;
    // get project ID from data attribute
    const projectId = statusDropdown.getAttribute("data-project-id");

    try {
      const response = await fetch(`/update_project_status/${projectId}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json", // tell flask what is being sent is JSON
        },
        // convert JS object to JSON string
        body: JSON.stringify({ status: newStatus }),
      });

      if (!response.ok) {
        alert("Failed to update project status.");
        // revert dropdown if server failed
        location.reload();
      }
    } catch (error) {
      console.error("Error updating status:", error);
    }
  });
}

// add task logic
const addTaskForm = document.getElementById("add-task-form");

if (addTaskForm) {
  addTaskForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const url = addTaskForm.action;
    const projectId = addTaskForm.getAttribute("data-project-id");
    const formData = new FormData(addTaskForm);

    const submitBtn = addTaskForm.querySelector("button[type='submit']");
    const originalText = submitBtn.innerText;
    submitBtn.innerText = "Adding...";
    submitBtn.disabled = true;
    submitBtn.style.opacity = "0.7";

    try {
      const data = await APIClient.addTask(url, formData);

      if (data.status === "success") {
        const newLi = document.createElement("li");

        let pColor = "#2ed573";
        if (data.priority === "High") {
          pColor = "#ff4757";
        } else if (data.priority === "Moderate") {
          pColor = "#ffa502";
        }

        newLi.innerHTML = `
                    <strong>${data.title}</strong>
                    <br>
                    <small>(Priority: <span style="color: ${pColor}; font-weight: bold;">${data.priority}</span> | Due: ${data.due_date})</small>
                    <br><br>
                    <form action="/toggle_task/${data.task_id}/${projectId}" method="POST" class="toggle-task-form" style="display:inline;">
                        <button type="submit" class="toggle-btn" style="padding: 5px 10px; font-size: 0.85em;">Complete</button>
                    </form>
                    <form action="/delete_task/${data.task_id}/${projectId}" method="POST" class="delete-task-form" style="display:inline; margin-left: 5px;">
                        <button type="submit" style="padding: 5px 10px; font-size: 0.85em;">Delete</button>
                    </form>
                `;

        const pendingList = document.getElementById("pending-tasks");
        if (pendingList) {
          pendingList.appendChild(newLi);
        }

        const emptyMsg = document.getElementById("empty-task-msg");
        if (emptyMsg) emptyMsg.style.display = "none";

        addTaskForm.reset();
      } else {
        alert("Failed to add task: " + (data.message || "Unknown error"));
      }
    } catch (error) {
      console.error("Error adding task:", error);
    } finally {
      submitBtn.innerText = originalText;
      submitBtn.disabled = false;
      submitBtn.style.opacity = "1";
    }
  });
}

// upload attachment logic
const uploadFileForm = document.getElementById("upload-file-form");

if (uploadFileForm) {
  uploadFileForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const projectId = uploadFileForm.getAttribute("data-project-id");

    const formData = new FormData(uploadFileForm);
    const submitBtn = uploadFileForm.querySelector("button[type='submit']");

    submitBtn.innerText = "Uploading...";
    submitBtn.disabled = true;

    try {
      const data = await APIClient.uploadAttachment(projectId, formData);

      if (data.status === "success") {
        const attachmentList = document.getElementById("attachment-list");
        const emptyMsg = document.getElementById("empty-attachment-msg");

        const newLi = document.createElement("li");

        newLi.innerHTML = `<a href="#" class="download-link" data-attachment-id="${data.id}">${data.file_name}</a>`;
        attachmentList.appendChild(newLi);

        if (emptyMsg) emptyMsg.style.display = "none";
        uploadFileForm.reset();
      } else {
        alert("Failed to upload: " + (data.message || "Unknown error"));
      }
    } catch (error) {
      console.error("Error uploading file:", error);
    } finally {
      submitBtn.innerText = "Upload File";
      submitBtn.disabled = false;
    }
  });
}

document.addEventListener("click", async (e) => {
  if (e.target.classList.contains("download-link")) {
    e.preventDefault();

    const link = e.target;
    const attachmentId = link.getAttribute("data-attachment-id");
    const fileName = link.innerText;

    const originalText = link.innerText;
    link.innerText = "Downloading...";
    link.style.pointerEvents = "none";

    try {
      const blob = await APIClient.downloadAttachment(attachmentId);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.style.display = "none";
      a.href = url;
      a.download = fileName;

      document.body.appendChild(a);
      a.click();

      window.URL.revokeObjectURL(url);
      a.remove();
    } catch (error) {
      console.error("Error downloading file:", error);
      alert("Failed to download file.");
    } finally {
      link.innerText = originalText;
      link.style.pointerEvents = "auto";
    }
  }
});

// auto-load tasks on page load
document.addEventListener("DOMContentLoaded", async () => {
  // dashboard logic { index.html }
  const projectList = document.getElementById("project-list");
  const searchInput = document.getElementById("project-search");
  if (projectList) {
    try {
      const data = await APIClient.getProjects();
      if (data.status === "success") {
        if (data.projects.length === 0) {
          projectList.innerHTML = "<p>No projects found. Create one above!</p>";
        } else {
          data.projects.forEach((project) => {
            const newLi = document.createElement("li");
            newLi.innerHTML = `
                <strong><a href="/project/${project.id}">${project.title}</a></strong>
                <p>${project.description || "No description provided."}</p>
                <form action="/delete_project/${project.id}" method="POST" style="display:inline;">
                    <button type="submit">Delete Project</button>
                </form>
            `;
            projectList.appendChild(newLi);
          });

          if (searchInput) {
            searchInput.addEventListener("input", (e) => {
              const searchTerm = e.target.value.toLowerCase();
              const listItems = projectList.querySelectorAll("li");

              listItems.forEach((item) => {
                const text = item.innerText.toLowerCase();
                if (text.includes(searchTerm)) {
                  item.style.display = "";
                } else {
                  item.style.display = "none";
                }
              });
            });
          }
        }
      }
    } catch (error) {
      console.error("Error fetching projects:", error);
    }
  }
  // project details logic
  const pendingList = document.getElementById("pending-tasks");
  const completedList = document.getElementById("completed-tasks");
  const addTaskForm = document.getElementById("add-task-form");

  if (pendingList && completedList && addTaskForm) {
    const projectId = addTaskForm.getAttribute("data-project-id");

    try {
      const data = await APIClient.getTasks(projectId);

      if (data.status === "success") {
        data.tasks.forEach((task) => {
          const newLi = document.createElement("li");

          let pColor = "#2ed573";
          if (task.priority === "High") {
            pColor = "#ff4757";
          } else if (task.priority === "Moderate") {
            pColor = "#ffa502";
          }

          const btnText = task.completed ? "Undo" : "Complete";

          newLi.innerHTML = `
                        <!-- Left Side: Task Info -->
                        <div style="flex-grow: 1; padding-right: 15px;">
                            <strong>${task.title}</strong>
                            <br>
                            <small>(Priority: <span style="color: ${pColor}; font-weight: bold;">${task.priority}</span> | Due: ${task.due_date})</small>
                        </div>
                        
                        <!-- Right Side: Buttons -->
                        <div style="white-space: nowrap;">
                            <form action="/toggle_task/${task.id}/${projectId}" method="POST" class="toggle-task-form" style="display:inline;">
                                <button type="submit" class="toggle-btn" style="padding: 5px 10px; font-size: 0.85em;">${btnText}</button>
                            </form>
                            <form action="/delete_task/${task.id}/${projectId}" method="POST" class="delete-task-form" style="display:inline; margin-left: 5px;">
                                <button type="submit" style="padding: 5px 10px; font-size: 0.85em;">Delete</button>
                            </form>
                        </div>
                    `;

          if (task.completed) {
            newLi.style.opacity = "0.6";
            completedList.appendChild(newLi);
          } else {
            pendingList.appendChild(newLi);
          }
        });
      }
    } catch (error) {
      console.error("Error fetching tasks:", error);
    }
  }

  // attachment details logic
  const attachmentList = document.getElementById("attachment-list");
  const emptyAttachmentMsg = document.getElementById("empty-attachment-msg");
  const uploadFileForm = document.getElementById("upload-file-form");

  if (attachmentList && uploadFileForm) {
    const projId = uploadFileForm.getAttribute("data-project-id");

    try {
      const data = await APIClient.getAttachments(projId);
      if (data.status === "success") {
        if (data.attachments.length === 0) {
          emptyAttachmentMsg.style.display = "block";
        } else {
          data.attachments.forEach((file) => {
            const newLi = document.createElement("li");

            newLi.innerHTML = `<a href="#" class="download-link" data-attachment-id="${file.id}">${file.file_name}</a>`;
            attachmentList.appendChild(newLi);
          });
        }
      }
    } catch (error) {
      console.error("Error fetching attachments:", error);
    }
  }

  // Fetch & display dashboard statistics
  const statTotalProjects = document.getElementById("stat-total-projects");

  if (statTotalProjects) {
    try {
      const statData = await APIClient.getStats();
      if (statData.status === "success") {
        document.getElementById("stat-total-projects").innerText =
          statData.stats.total_projects;
        document.getElementById("stat-total-tasks").innerText =
          statData.stats.total_tasks;
        document.getElementById("stat-completed-tasks").innerText =
          statData.stats.completed_tasks;
        document.getElementById("stat-pending-tasks").innerText =
          statData.stats.pending_tasks;
      }
    } catch (error) {
      console.error("Error fetching stats:", error);
      document.getElementById("stat-total-projects").innerText = "Error";
      document.getElementById("stat-total-tasks").innerText = "Error";
      document.getElementById("stat-completed-tasks").innerText = "Error";
      document.getElementById("stat-pending-tasks").innerText = "Error";
    }
  }

  // project description
  const saveDescBtn = document.getElementById("save-description-btn");
  const descTextarea = document.getElementById("project-description");

  if (saveDescBtn && descTextarea) {
    saveDescBtn.addEventListener("click", async () => {
      const projectId = descTextarea.getAttribute("data-project-id");
      const description = descTextarea.value;
      const originalText = saveDescBtn.innerText;

      saveDescBtn.innerText = "Saving...";
      saveDescBtn.style.opacity = "0.7";

      try {
        const data = await APIClient.updateDescription(projectId, description);
        if (data.status === "success") {
          saveDescBtn.innerText = "Saved!";
          saveDescBtn.style.backgroundColor = "#2ed573";

          setTimeout(() => {
            saveDescBtn.innerText = originalText;
            saveDescBtn.style.backgroundColor = "";
            saveDescBtn.style.opacity = "1";
          }, 2000);
        }
      } catch (error) {
        console.error("Error saving description:", error);
        saveDescBtn.innerText = "Error";
      }
    });
  }
});
