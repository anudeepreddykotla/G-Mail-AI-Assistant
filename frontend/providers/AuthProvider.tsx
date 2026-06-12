"use client";

import { useEffect, ReactNode } from "react";

import { getCurrentUser } from "@/services/auth";
import { useAuthStore } from "@/store/authStore";

interface AuthProviderProps {
  children: ReactNode;
}

export default function AuthProvider({
  children,
}: AuthProviderProps) {
  const setUser = useAuthStore(
    (state) => state.setUser
  );

  const setToken = useAuthStore(
    (state) => state.setToken
  );

  const clearAuth = useAuthStore(
    (state) => state.clearAuth
  );

  useEffect(() => {
    const initializeAuth = async () => {
      try {
        const token =
          localStorage.getItem("token");

        if (!token) {
          return;
        }

        setToken(token);

        const user =
          await getCurrentUser();

        setUser(user);
      } catch (error) {
        console.error(
          "Failed to restore session",
          error
        );

        clearAuth();
      }
    };

    initializeAuth();
  }, [setUser, setToken, clearAuth]);

  return <>{children}</>;
}