"use client";

import {
  RefreshCw,
  Archive,
  Trash2,
  Search,
} from "lucide-react";

import {
  archiveMessage,
  trashMessage,
} from "@/services/gmail";

interface Props {
  onRefresh: () => Promise<void>;

  selectedIds: string[];

  clearSelection: () => void;

  searchQuery: string;

  onSearchChange: (
    value: string
  ) => void;
}

export default function EmailToolbar({
  onRefresh,
  selectedIds,
  clearSelection,
  searchQuery,
  onSearchChange,
}: Props) {
  const hasSelection =
    selectedIds.length > 0;

  const handleArchive =
    async () => {
      try {
        await Promise.all(
          selectedIds.map((id) =>
            archiveMessage(id)
          )
        );

        clearSelection();

        await onRefresh();
      } catch (error) {
        console.error(error);
      }
    };

  const handleTrash =
    async () => {
      try {
        await Promise.all(
          selectedIds.map((id) =>
            trashMessage(id)
          )
        );

        clearSelection();

        await onRefresh();
      } catch (error) {
        console.error(error);
      }
    };

  return (
    <div
      className="
        flex
        items-center
        gap-3
        border-b
        border-zinc-800
        px-4
        py-2
      "
    >
      <button
        onClick={onRefresh}
        className="rounded p-2 hover:bg-zinc-900"
      >
        <RefreshCw size={18} />
      </button>

      <button
        onClick={handleArchive}
        disabled={!hasSelection}
        className="
          rounded
          p-2
          hover:bg-zinc-900
          disabled:cursor-not-allowed
          disabled:opacity-40
        "
      >
        <Archive size={18} />
      </button>

      <button
        onClick={handleTrash}
        disabled={!hasSelection}
        className="
          rounded
          p-2
          hover:bg-zinc-900
          disabled:cursor-not-allowed
          disabled:opacity-40
        "
      >
        <Trash2 size={18} />
      </button>

      {hasSelection && (
        <span className="text-sm text-zinc-400">
          {selectedIds.length} selected
        </span>
      )}

      <div className="ml-auto relative w-96">
        <Search
          size={16}
          className="
            absolute
            left-3
            top-1/2
            -translate-y-1/2
            text-zinc-500
          "
        />

        <input
          type="text"
          value={searchQuery}
          onChange={(e) =>
            onSearchChange(
              e.target.value
            )
          }
          placeholder="Search emails..."
          className="
            w-full
            rounded-lg
            border
            border-zinc-700
            bg-zinc-900
            py-2
            pl-10
            pr-4
            text-sm
            outline-none
            focus:border-blue-500
          "
        />
      </div>
    </div>
  );
}