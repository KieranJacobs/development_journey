// delete task logic
document.addEventListener("DOMContentLoaded", () => {
  const deleteForms = document.querySelectorAll(".delete-task-form");

  deleteForms.forEach((form) => {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();

      if (!confirm("Are you sure you want to delete this task?")) return;

      const url = form.action;

      try {
        const response = await fetch(url, {
          method: "POST",
        });

        if (response.ok) {
          form.closest("li").remove();
        } else {
          alert("Something went wrong deleting the task.");
        }
      } catch (error) {
        console.error("Error deleting task:", error);
      }
    });
  });
});

// toggle task logic
const toggleForms = document.querySelectorAll(".toggle-task-form");

toggleForms.forEach((form) => {
  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const url = form.action;
    const button = form.querySelector(".toggle-btn");

    try {
      const response = await fetch(url, {
        method: "POST",
      });

      if (response.ok) {
        const currentText = button.innerText.trim();
        if (currentText === "Complete") {
          button.innerText = "Undo";

          form.closest("li").style.textDecoration = "line-through";
        } else {
          button.innerText = "Complete";
          form.closest("li").style.textDecoration = "none";
        }
      } else {
        alert("Something went wrong updating the task.");
      }
    } catch (error) {
      console.error("Error toggling task:", error);
    }
  });
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
const taskList = document.getElementById("task-list");

if (addTaskForm) {
  addTaskForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const url = addTaskForm.action;
    const projectId = addTaskForm.getAttribute("data-project-id");

    const formData = new FormData(addTaskForm);

    try {
      const response = await fetch(url, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (response.ok && data.status === "success") {
        const newLi = document.createElement("li");

        newLi.innerHTML = `
            ${data.title} - Priority: ${data.priority} - Due: ${data.due_date} - Pending
            <form action="/toggle_task/${data.task_id}/${projectId}" method="POST" class="toggle-task-form" style="display:inline;">
                <button type="submit" class="toggle-btn">Complete</button>
            </form>
            <form action="/delete_task/${data.task_id}/${projectId}" method="POST" class="delete-task-form" style="display:inline; margin-left: 5px;">
                <button type="submit">Delete</button>
            </form>
        `;

        taskList.appendChild(newLi);

        addTaskForm.reset();
      } else {
        alert("Failed to add task: " + (data.message || "Unknown error"));
      }
    } catch (error) {
      console.error("Error adding task:", error);
    }
  });
}
