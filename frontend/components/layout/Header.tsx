"use client";

import { useAuthStore } from "@/store/authStore";

export default function Header() {
  const user = useAuthStore(
    (state) => state.user
  );

  return (
    <header className="flex h-16 items-center justify-between border-b px-6">
      <div>
        <h1 className="text-lg font-semibold">
          Gmail AI Assistant
        </h1>
      </div>

      <div className="flex-1" />

      <div className="flex items-center gap-3">
        <div
          className="
            flex
            h-10
            w-10
            items-center
            justify-center
            rounded-full
            bg-blue-600
            font-semibold
            text-white
          "
        >
          {user?.email?.[0]?.toUpperCase() ??
            "U"}
        </div>

        <div className="hidden md:block">
          <p className="text-sm font-medium">
            {user?.name}
          </p>

          <p className="text-xs text-gray-500">
            {user?.email}
          </p>
        </div>
      </div>
    </header>
  );
}