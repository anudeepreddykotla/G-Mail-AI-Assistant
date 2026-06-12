"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

import {
  Menu,
  Inbox,
  FileText,
  Send,
  Star,
  Trash2,
  Pencil,
} from "lucide-react";

import { useUIStore } from "@/store/uiStore";

interface SidebarProps {
  onCompose: () => void;
}

const menuItems = [
  {
    label: "Inbox",
    href: "/inbox",
    icon: Inbox,
  },
  {
    label: "Drafts",
    href: "/drafts",
    icon: FileText,
  },
  {
    label: "Sent",
    href: "/sent",
    icon: Send,
  },
  {
    label: "Starred",
    href: "/starred",
    icon: Star,
  },
  {
    label: "Trash",
    href: "/trash",
    icon: Trash2,
  },
];

export default function Sidebar({
  onCompose,
}: SidebarProps) {
  const pathname = usePathname();

  const sidebarCollapsed =
    useUIStore(
      (state) => state.sidebarCollapsed
    );

  const toggleSidebar =
    useUIStore(
      (state) => state.toggleSidebar
    );

  return (
    <aside
      className={`
        flex flex-col
        border-r border-zinc-800
        bg-black
        transition-all duration-300
        ${
          sidebarCollapsed
            ? "w-20"
            : "w-64"
        }
      `}
    >
      <div className="flex items-center justify-between p-4">
        <button
          onClick={toggleSidebar}
          className="
            rounded-lg
            p-2
            text-zinc-400
            hover:bg-zinc-900
            hover:text-white
          "
        >
          <Menu size={20} />
        </button>
      </div>

      <div className="px-3 pb-4">
        <button
          onClick={onCompose}
          className={`
            flex items-center gap-3
            rounded-xl
            bg-blue-600
            px-4 py-3
            text-white
            transition
            hover:bg-blue-700
            ${
              sidebarCollapsed
                ? "justify-center"
                : ""
            }
          `}
        >
          <Pencil size={18} />

          {!sidebarCollapsed && (
            <span>Compose</span>
          )}
        </button>
      </div>

      <nav className="flex flex-col gap-1 px-3">
        {menuItems.map((item) => {
          const active =
            pathname === item.href;

          const Icon =
            item.icon;

          return (
            <Link
              key={item.href}
              href={item.href}
              className={`
                flex items-center gap-3
                rounded-lg
                px-4 py-3
                transition
                ${
                  active
                    ? "bg-blue-600 text-white"
                    : "text-zinc-400 hover:bg-zinc-900 hover:text-white"
                }
                ${
                  sidebarCollapsed
                    ? "justify-center"
                    : ""
                }
              `}
            >
              <Icon size={18} />

              {!sidebarCollapsed && (
                <span>
                  {item.label}
                </span>
              )}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}