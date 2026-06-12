import api from "./api";

export const login = () => {
  window.location.href = `${process.env.NEXT_PUBLIC_API_URL}/auth/login`;
};

export const getCurrentUser = async () => {
  const response = await api.get("/auth/me");
  return response.data;
};

export const logout = async () => {
  const response = await api.post("/auth/logout");
  return response.data;
};