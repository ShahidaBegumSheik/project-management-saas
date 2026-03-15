import axios from "axios";


const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000/api/v1";


const api = axios.create({
  baseURL: API_BASE,
  headers: {
    "Content-Type": "application/json"
  }
});


export function getToken() {
  return localStorage.getItem("token");
}


export function getStoredUser() {
  const raw = localStorage.getItem("user");
  return raw ? JSON.parse(raw) : null;
}


export function setAuthSession(token, user = null) {
  if (token) {
    localStorage.setItem("token", token);
    api.defaults.headers.common.Authorization = `Bearer ${token}`;
  }


  if (user) {
    localStorage.setItem("user", JSON.stringify(user));
  }
}


export function clearAuthSession() {
  localStorage.removeItem("token");
  localStorage.removeItem("user");
  delete api.defaults.headers.common.Authorization;
}


const token = getToken();
if (token) {
  api.defaults.headers.common.Authorization = `Bearer ${token}`;
}


export default api;
