import { request } from "./httpClient";

export function searchProductsApi(query) {
  const q = encodeURIComponent(query || "");
  return request(`/search?q=${q}&limit=50&offset=0`);
}

export function listNewestProductsApi(limit = 12) {
  return request(`/search?limit=${limit}&offset=0`);
}
