// event delegation for task list logic
const taskList = document.getElementById("task-list");

if (taskList) {
  taskList.addEventListener("submit", async (e) => {
    // If delete form?
    if (e.target.classList.contains("delete-task-form")) {
      e.preventDefault();
      const form = e.target;
      const url = form.action;

      try {
        const response = await fetch(url, { method: "POST" });
        const data = await response.json();

        if (response.ok && data.status === "success") {
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
      const url = form.action;

      try {
        const response = await fetch(url, { method: "POST" });
        const data = await response.json();

        if (response.ok && data.status === "success") {
          const button = form.querySelector("button");

          if (button.innerText === "Complete") {
            button.innerText = "Undo";
          } else {
            button.innerText = "Complete";
          }
        }
      } catch (error) {
        console.error("Error toggling task:", error);
      }
    }
  });
}

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
      const response = await fetch(url, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (response.ok && data.status === "success") {
        const newLi = document.createElement("li");

        let pColor = "#2ed573";
        if (data.priority === "High") {
          pColor = "#ff4757";
        } else if (data.priority === "Moderate") {
          pColor = "#ffa502";
        }

        newLi.innerHTML = `
            <strong>${data.title}</strong>
            (Priority: <span style="color: ${pColor}; font-weight: bold;">${data.priority}</span> | Due: ${data.due_date})
            
            <form action="/toggle_task/${data.task_id}/${projectId}" method="POST" class="toggle-task-form" style="display:inline;">
                <button type="submit" class="toggle-btn">Complete</button>
            </form>
            <form action="/delete_task/${data.task_id}/${projectId}" method="POST" class="delete-task-form" style="display:inline; margin-left: 5px;">
                <button type="submit">Delete</button>
            </form>
        `;

        taskList.appendChild(newLi);

        const emptyMsg = document.getElementById("empty-task-msg");
        if (emptyMsg) emptyMsg.remove();

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
