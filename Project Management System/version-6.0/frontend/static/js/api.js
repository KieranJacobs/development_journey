// api.js/version-6.0
class APIClient {
  static BASE_URL = "";

  static async getProjects() {
    const response = await fetch(`${this.BASE_URL}/api/projects`);
    return await response.json();
  }

  static async getTasks(projectId) {
    const response = await fetch(`${this.BASE_URL}/api/tasks/${projectId}`);
    return await response.json();
  }

  static async getStats() {
    const response = await fetch(`${this.BASE_URL}/api/stats`);
    return await response.json();
  }

  static async addTask(url, formData) {
    const response = await fetch(`${this.BASE_URL}${url}`, {
      method: "POST",
      body: formData,
    });
    return await response.json();
  }

  static async toggleTask(url) {
    const response = await fetch(`${this.BASE_URL}${url}`, { method: "POST" });
    return await response.json();
  }

  static async deleteTask(url) {
    const response = await fetch(`${this.BASE_URL}${url}`, { method: "POST" });
    return await response.json();
  }

  static async getAttachments(projectId) {
    const response = await fetch(
      `${this.BASE_URL}/api/attachments/${projectId}`,
    );
    return await response.json();
  }

  static async uploadAttachment(projectId, formData) {
    const response = await fetch(
      `${this.BASE_URL}/api/attachments/upload/${projectId}`,
      {
        method: "POST",
        body: formData,
      },
    );
    return await response.json();
  }

  static async downloadAttachment(attachmentId) {
    const response = await fetch(
      `${this.BASE_URL}/api/attachments/download/${attachmentId}`,
    );
    if (!response.ok) {
      throw new Error("Failed to fetch file");
    }
    return await response.blob();
  }

  static async updateDescription(projectId, description) {
    const response = await fetch(
      `${this.BASE_URL}/api/projects/${projectId}/description`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ description }),
      },
    );
    return await response.json();
  }
}
