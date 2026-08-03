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
