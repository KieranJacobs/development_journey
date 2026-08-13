// script.js/version-6.3
function showApiFeedback(message, type = "error") {
  let banner = document.getElementById("api-feedback-banner");
  if (!banner) {
    banner = document.createElement("div");
    banner.id = "api-feedback-banner";
    banner.style.position = "fixed";
    banner.style.top = "16px";
    banner.style.right = "16px";
    banner.style.maxWidth = "320px";
    banner.style.padding = "10px 14px";
    banner.style.borderRadius = "8px";
    banner.style.zIndex = "9999";
    banner.style.fontSize = "0.9rem";
    banner.style.fontWeight = "600";
    banner.style.boxShadow = "0 12px 30px rgba(0, 0, 0, 0.18)";
    banner.style.color = "#f5f7fa";
    banner.style.display = "none";
    document.body.appendChild(banner);
  }

  const isError = type === "error";
  banner.style.backgroundColor = isError ? "#e74c3c" : "#2ecc71";
  banner.textContent = message;
  banner.style.display = "block";

  clearTimeout(banner.hideTimer);
  banner.hideTimer = setTimeout(() => {
    banner.style.display = "none";
  }, 4000);
}

function showApiError(message) {
  showApiFeedback(message, "error");
}

function showApiSuccess(message) {
  showApiFeedback(message, "success");
}

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
      showApiError(error.message || "Unable to delete task.");
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
      showApiError(error.message || "Unable to update task status.");
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
        const payload = await response.json().catch(() => ({ message: "Failed to update project status." }));
        showApiError(payload.message || "Failed to update project status.");
        location.reload();
      }
    } catch (error) {
      console.error("Error updating status:", error);
      showApiError(error.message || "Failed to update project status.");
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
        showApiSuccess("Task added successfully.");
      } else {
        showApiError(data.message || "Failed to add task.");
      }
    } catch (error) {
      console.error("Error adding task:", error);
      showApiError(error.message || "Unable to create task.");
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
        showApiSuccess("File uploaded successfully.");
      } else {
        showApiError(data.message || "Failed to upload file.");
      }
    } catch (error) {
      console.error("Error uploading file:", error);
      showApiError(error.message || "Unable to upload file.");
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
      showApiSuccess("File downloaded successfully.");
    } catch (error) {
      console.error("Error downloading file:", error);
      showApiError(error.message || "Failed to download file.");
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
      showApiError(error.message || "Unable to load projects.");
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
      showApiError(error.message || "Unable to load tasks.");
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
      showApiError(error.message || "Unable to load attachments.");
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
      showApiError(error.message || "Unable to load dashboard statistics.");
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
          showApiSuccess("Project description saved.");

          setTimeout(() => {
            saveDescBtn.innerText = originalText;
            saveDescBtn.style.backgroundColor = "";
            saveDescBtn.style.opacity = "1";
          }, 2000);
        }
      } catch (error) {
        console.error("Error saving description:", error);
        saveDescBtn.innerText = "Error";
        showApiError(error.message || "Unable to save description.");
      }
    });
  }
});
