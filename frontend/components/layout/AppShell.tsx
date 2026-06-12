"use client";

import { ReactNode, useState } from "react";

import ProtectedRoute from "@/components/common/ProtectedRoute";
import Sidebar from "@/components/layout/Sidebar";
import Header from "@/components/layout/Header";

import ComposeModal from "@/components/email/ComposeModal";

interface AppShellProps {
  children: ReactNode;
}

export default function AppShell({
  children,
}: AppShellProps) {
  const [composeOpen, setComposeOpen] =
    useState(false);

  return (
    <ProtectedRoute>
      <div className="flex h-screen overflow-hidden">
        <Sidebar
          onCompose={() =>
            setComposeOpen(true)
          }
        />

        <div className="flex flex-1 flex-col overflow-hidden">
          <Header />

          <main className="flex-1 overflow-hidden">
            {children}
          </main>
        </div>

        <ComposeModal
          open={composeOpen}
          onClose={() =>
            setComposeOpen(false)
          }
        />
      </div>
    </ProtectedRoute>
  );
}