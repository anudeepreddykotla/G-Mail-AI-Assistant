"use client";

import { ReactNode, useEffect } from "react";
import { useRouter } from "next/navigation";

import { useAuthStore } from "@/store/authStore";

interface ProtectedRouteProps {
  children: ReactNode;
}

export default function ProtectedRoute({
  children,
}: ProtectedRouteProps) {
  const router = useRouter();

  const token = useAuthStore(
    (state) => state.token
  );

  useEffect(() => {
    const storedToken =
      localStorage.getItem("token");

    if (!token && !storedToken) {
      router.replace("/");
    }
  }, [token, router]);

  if (!token && typeof window !== "undefined") {
    const storedToken =
      localStorage.getItem("token");

    if (!storedToken) {
      return null;
    }
  }

  return <>{children}</>;
}