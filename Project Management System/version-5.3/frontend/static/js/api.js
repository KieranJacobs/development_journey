class APIClient {
  static BASE_URL = "";

  static async getTasks(projectId) {
    const response = await fetch(`${this.BASE_URL}/api/tasks/${projectId}`);
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
}
