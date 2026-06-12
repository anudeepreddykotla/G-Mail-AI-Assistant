"use client";

import { login } from "@/services/auth";

export default function HomePage() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-gray-100">
      <div className="w-full max-w-md rounded-lg bg-white p-8 shadow-md">
        <h1 className="mb-2 text-3xl font-bold">
          Gmail AI Assistant
        </h1>

        <p className="mb-8 text-gray-600">
          Connect your Gmail account and manage emails with AI assistance.
        </p>

        <button
          onClick={login}
          className="w-full rounded-md bg-blue-600 px-4 py-3 text-white transition hover:bg-blue-700"
        >
          Sign in with Google
        </button>
      </div>
    </main>
  );
}