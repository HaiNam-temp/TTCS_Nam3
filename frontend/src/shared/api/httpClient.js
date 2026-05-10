const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://price-comp-alb-2137356393.ap-southeast-2.elb.amazonaws.com";

function ensureApiPath(path) {
  if (!path) return "/api";
  if (path.startsWith("/api")) return path;
  if (path.startsWith("/")) return "/api" + path;
  return "/api/" + path;
}

function buildHeaders(token, contentType = "application/json") {
  const headers = {};
  if (contentType) {
    headers["Content-Type"] = contentType;
  }
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }
  return headers;
}

export async function request(path, { method = "GET", body, token, contentType = "application/json" } = {}) {
  const apiPath = ensureApiPath(path);
  const response = await fetch(`${API_BASE_URL}${apiPath}`, {
    method,
    headers: buildHeaders(token, contentType),
    body: body ? JSON.stringify(body) : undefined,
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `Request failed with status ${response.status}`);
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}

export async function requestForm(path, { formData, token } = {}) {
  const apiPath = ensureApiPath(path);
  const response = await fetch(`${API_BASE_URL}${apiPath}`, {
    method: "POST",
    headers: buildHeaders(token, "application/x-www-form-urlencoded"),
    body: new URLSearchParams(formData),
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `Request failed with status ${response.status}`);
  }

  return response.json();
}
