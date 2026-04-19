import { request } from "./httpClient";

export function getStatsApi(token) {
  return request("/admin/stats", { token });
}

export function getUsersApi(token) {
  return request("/admin/users/", { token });
}

export function deleteUserApi(token, userId) {
  return request(`/admin/users/${userId}`, {
    method: "DELETE",
    token,
  });
}

export function crawlProductsApi(token, query, limit = 20) {
  return request("/admin/batch/crawl-products", {
    method: "POST",
    token,
    body: { query, limit },
  });
}
