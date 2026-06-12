import { create } from "zustand";

import { User } from "@/types/auth";

interface AuthState {
  token: string | null;
  user: User | null;

  setToken: (token: string) => void;
  setUser: (user: User) => void;

  clearAuth: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  token: null,

  user: null,

  setToken: (token) => {
    localStorage.setItem("token", token);

    set({
      token,
    });
  },

  setUser: (user) => {
    set({
      user,
    });
  },

  clearAuth: () => {
    localStorage.removeItem("token");

    set({
      token: null,
      user: null,
    });
  },
}));