import { request, requestForm } from "./httpClient";

export function loginApi(username, password) {
  return requestForm("/token", {
    formData: {
      username,
      password,
    },
  });
}

export function registerApi(payload) {
  return request("/users/", {
    method: "POST",
    body: payload,
  });
}

export function meApi(token) {
  return request("/users/me", { token });
}
