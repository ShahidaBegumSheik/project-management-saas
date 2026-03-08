import axios from "axios";

export const API_BASE =
  import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000/api/v1";

export const api = axios.create({
  baseURL: API_BASE,
});

export function getToken() {
  return localStorage.getItem("token");
}

export function getRole() {
  return localStorage.getItem("role");
}

function decodeJwt(token) {
  try {
    const payload = token.split(".")[1];
    return JSON.parse(atob(payload));
  } catch {
    return null;
  }
}

export function setToken(token) {
  localStorage.setItem("token", token);
  const payload = decodeJwt(token);
  if (payload?.role) {
    localStorage.setItem("role", payload.role);
  }
}

export function clearAuth() {
  localStorage.removeItem("token");
  localStorage.removeItem("role");
}

api.interceptors.request.use((config) => {
  const token = getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
