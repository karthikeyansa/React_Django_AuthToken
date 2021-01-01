export class API {
  static Login(body) {
    return fetch("http://127.0.0.1:8000/auth/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    }).then((resp) => resp.json());
  }
  static Register(body) {
    return fetch("http://127.0.0.1:8000/api/users/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    }).then((resp) => resp.json());
  }
  static GetTasks(token) {
    return fetch("http://127.0.0.1:8000/api/todos/", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Token ${token}`,
      },
    }).then((resp) => resp.json());
  }
  static TaskAdd(body, token) {
    return fetch(`http://127.0.0.1:8000/api/todos/`, {
      method: "POST",
      headers: {
        "content-Type": "application/json",
        Authorization: `Token ${token}`,
      },
      body: JSON.stringify(body),
    }).then((resp) => resp.json());
  }
  static TaskEdit(task, body, token) {
    console.log(task, body);
    return fetch(`http://127.0.0.1:8000/api/todos/${task.id}/`, {
      method: "PUT",
      headers: {
        "content-Type": "application/json",
        Authorization: `Token ${token}`,
      },
      body: JSON.stringify(body),
    }).then((resp) => resp.json());
  }
  static TaskComplete(task, token) {
    return fetch(`http://127.0.0.1:8000/api/todos/${task.id}/`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Token ${token}`,
      },
    }).then((resp) => resp.json());
  }
  static TaskDelete(task, token) {
    return fetch(`http://127.0.0.1:8000/api/todos/${task.id}/`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Token ${token}`,
      },
    }).then((resp) => resp.json());
  }
}
