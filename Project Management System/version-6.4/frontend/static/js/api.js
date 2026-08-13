// api.js/version-6.3
class APIClient {
  static BASE_URL = "";

  static async requestJson(url, options = {}) {
    const response = await fetch(url, options);

    let payload = null;
    try {
      payload = await response.json();
    } catch (_error) {
      payload = null;
    }

    if (!response.ok || (payload && payload.status === "error")) {
      const message =
        payload && payload.message
          ? payload.message
          : `Request failed with status ${response.status}`;
      throw new Error(message);
    }

    return payload || { status: "success" };
  }

  static async getProjects() {
    return await this.requestJson(`${this.BASE_URL}/api/projects`);
  }

  static async getTasks(projectId) {
    return await this.requestJson(`${this.BASE_URL}/api/tasks/${projectId}`);
  }

  static async getStats() {
    return await this.requestJson(`${this.BASE_URL}/api/stats`);
  }

  static async addTask(url, formData) {
    return await this.requestJson(`${this.BASE_URL}${url}`, {
      method: "POST",
      body: formData,
    });
  }

  static async toggleTask(url) {
    return await this.requestJson(`${this.BASE_URL}${url}`, { method: "POST" });
  }

  static async deleteTask(url) {
    return await this.requestJson(`${this.BASE_URL}${url}`, { method: "POST" });
  }

  static async getAttachments(projectId) {
    return await this.requestJson(
      `${this.BASE_URL}/api/attachments/${projectId}`,
    );
  }

  static async uploadAttachment(projectId, formData) {
    return await this.requestJson(
      `${this.BASE_URL}/api/attachments/upload/${projectId}`,
      {
        method: "POST",
        body: formData,
      },
    );
  }

  static async downloadAttachment(attachmentId) {
    const response = await fetch(
      `${this.BASE_URL}/api/attachments/download/${attachmentId}`,
    );
    if (!response.ok) {
      let message = "Failed to download file.";
      try {
        const payload = await response.json();
        if (payload && payload.message) {
          message = payload.message;
        }
      } catch (_error) {
        // ignore non-JSON error payloads
      }
      throw new Error(message);
    }
    return await response.blob();
  }

  static async updateDescription(projectId, description) {
    return await this.requestJson(
      `${this.BASE_URL}/api/projects/${projectId}/description`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ description }),
      },
    );
  }
}
