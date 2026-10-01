const API_BASE_URL = 'http://localhost:8000';

class TodoApiError extends Error {
  constructor(message, status) {
    super(message);
    this.name = 'TodoApiError';
    this.status = status;
  }
}

async function parseError(response) {
  try {
    const body = await response.json();
    return body.error || `Request failed with status ${response.status}`;
  } catch (error) {
    return `Request failed with status ${response.status}`;
  }
}

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    throw new TodoApiError(await parseError(response), response.status);
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}

export async function fetchTodos() {
  return request('/todos/');
}

export async function createTodo(description) {
  return request('/todos/', {
    method: 'POST',
    body: JSON.stringify({ description }),
  });
}

export { TodoApiError };
