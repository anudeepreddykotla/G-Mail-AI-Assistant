"use client";

import { useEffect } from "react";
import { useRouter, useSearchParams } from "next/navigation";

import { getCurrentUser } from "@/services/auth";
import { useAuthStore } from "@/store/authStore";

export default function AuthCallbackPage() {
  const router = useRouter();

  const searchParams = useSearchParams();

  const setToken = useAuthStore(
    (state) => state.setToken
  );

  const setUser = useAuthStore(
    (state) => state.setUser
  );

  useEffect(() => {
    const handleLogin = async () => {
      try {
        const token =
          searchParams.get("token");

        if (!token) {
          router.replace("/");
          return;
        }

        setToken(token);

        const user =
          await getCurrentUser();

        setUser(user);

        router.replace("/inbox");
      } catch (error) {
        console.error(error);

        router.replace("/");
      }
    };

    handleLogin();
  }, [
    router,
    searchParams,
    setToken,
    setUser,
  ]);

  return (
    <div className="flex h-screen items-center justify-center">
      <p>Signing you in...</p>
    </div>
  );
}