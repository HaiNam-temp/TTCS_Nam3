// Default to backend on the deployment server at port 8010 when not overridden
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://54.206.52.145:8010";
const DEFAULT_TIMEOUT_MS = parseInt(import.meta.env.VITE_API_TIMEOUT_MS || "15000", 10); // 15s
const DEFAULT_RETRIES = parseInt(import.meta.env.VITE_API_RETRIES || "3", 10);
import loadingState from "./loadingState";

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

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function fetchWithTimeout(url, options = {}, timeout = DEFAULT_TIMEOUT_MS) {
  const controller = new AbortController();
  const id = setTimeout(() => controller.abort(), timeout);
  try {
    const resp = await fetch(url, { ...options, signal: controller.signal });
    clearTimeout(id);
    return resp;
  } catch (err) {
    clearTimeout(id);
    throw err;
  }
}

async function fetchWithRetry(url, options = {}, { retries = DEFAULT_RETRIES, timeout = DEFAULT_TIMEOUT_MS } = {}) {
  // increment global in-flight counter once per logical request
  loadingState.increment();
  try {
    let attempt = 0;
    let lastErr;
    while (attempt < retries) {
      try {
        const res = await fetchWithTimeout(url, options, timeout);
        return res;
      } catch (err) {
        lastErr = err;
        // For abort vs network errors, retry; for HTTP errors we'll handle after response
        const backoff = Math.min(1000 * 2 ** attempt, 8000) + Math.floor(Math.random() * 200);
        await sleep(backoff);
        attempt += 1;
      }
    }
    // final attempt
    return fetchWithTimeout(url, options, timeout).catch((err) => { throw lastErr || err; });
  } finally {
    loadingState.decrement();
  }
}

export async function request(path, { method = "GET", body, token, contentType = "application/json" } = {}) {
  const apiPath = ensureApiPath(path);
  // If token not provided, try to read from localStorage (auth token key used by AuthContext)
  if (!token) {
    try {
      token = localStorage.getItem("pricecomp_token");
    } catch (e) {
      // ignore
    }
  }
  const response = await fetchWithRetry(`${API_BASE_URL}${apiPath}`, {
    method,
    headers: buildHeaders(token, contentType),
    body: body ? JSON.stringify(body) : undefined,
  }, { timeout: DEFAULT_TIMEOUT_MS, retries: DEFAULT_RETRIES });

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
  if (!token) {
    try {
      token = localStorage.getItem("pricecomp_token");
    } catch (e) {}
  }
  const response = await fetchWithRetry(`${API_BASE_URL}${apiPath}`, {
    method: "POST",
    headers: buildHeaders(token, "application/x-www-form-urlencoded"),
    body: new URLSearchParams(formData),
  }, { timeout: DEFAULT_TIMEOUT_MS, retries: DEFAULT_RETRIES });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `Request failed with status ${response.status}`);
  }

  return response.json();
}
