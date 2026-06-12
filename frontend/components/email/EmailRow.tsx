"use client";

import {
  memo,
  useCallback,
} from "react";

import { useRouter } from "next/navigation";

import {
  useQueryClient,
} from "@tanstack/react-query";

import {
  getMessage,
} from "@/services/gmail";

import { GmailMessage } from "@/types/gmail";

interface Props {
  message: GmailMessage;

  selected: boolean;

  onToggleSelect: (
    id: string
  ) => void;
}

function getSender(from: string) {
  const match =
    from.match(/^(.+?)\s*</);

  if (match) {
    return match[1];
  }

  return from
    .replace(/<.*>/, "")
    .trim();
}

function formatDate(
  dateString: string
) {
  const date =
    new Date(dateString);

  const now = new Date();

  if (
    date.toDateString() ===
    now.toDateString()
  ) {
    return date.toLocaleTimeString(
      [],
      {
        hour: "numeric",
        minute: "2-digit",
      }
    );
  }

  if (
    date.getFullYear() ===
    now.getFullYear()
  ) {
    return date.toLocaleDateString(
      [],
      {
        month: "short",
        day: "numeric",
      }
    );
  }

  return date.toLocaleDateString();
}

function getCategory(
  labels?: string[]
) {
  if (!labels) return null;

  if (
    labels.includes(
      "CATEGORY_SOCIAL"
    )
  ) {
    return {
      text: "Social",
      className:
        "bg-blue-500/20 text-blue-400",
    };
  }

  if (
    labels.includes(
      "CATEGORY_PROMOTIONS"
    )
  ) {
    return {
      text: "Promotions",
      className:
        "bg-green-500/20 text-green-400",
    };
  }

  if (
    labels.includes(
      "CATEGORY_UPDATES"
    )
  ) {
    return {
      text: "Updates",
      className:
        "bg-yellow-500/20 text-yellow-400",
    };
  }

  return null;
}

function EmailRow({
  message,
  selected,
  onToggleSelect,
}: Props) {
  const router = useRouter();

  const queryClient =
    useQueryClient();

  const unread =
    message.labelIds?.includes(
      "UNREAD"
    );

  const sent =
    message.labelIds?.includes(
      "SENT"
    );

  const labels =
    message.labelIds || [];

  const starred =
    labels.includes(
      "STARRED"
    );

  const trash =
    labels.includes(
      "TRASH"
    );

  const archived =
    !labels.includes(
      "INBOX"
    ) &&
    !labels.includes(
      "TRASH"
    ) &&
    !labels.includes(
      "SENT"
    ) &&
    !labels.includes(
      "DRAFT"
    );

  const category =
    getCategory(
      message.labelIds
    );

  const prefetchEmail =
    useCallback(
      async () => {
        router.prefetch(
          `/email/${message.id}`
        );

        await queryClient.prefetchQuery(
          {
            queryKey: [
              "message",
              message.id,
            ],
            queryFn: () =>
              getMessage(
                message.id
              ),
          }
        );
      },
      [
        router,
        queryClient,
        message.id,
      ]
    );

  return (
    <div
      onMouseEnter={
        prefetchEmail
      }
      onClick={() =>
        router.push(
          `/email/${message.id}`
        )
      }
      className="
        grid
        grid-cols-[24px_220px_1fr_120px]
        items-center
        gap-4
        border-b
        border-zinc-800
        px-4
        py-3
        cursor-pointer
        hover:bg-zinc-900
      "
    >
      <div
        onClick={(e) =>
          e.stopPropagation()
        }
      >
        <input
          type="checkbox"
          checked={selected}
          onChange={() =>
            onToggleSelect(
              message.id
            )
          }
        />
      </div>

      <div
        className={`
          flex
          items-center
          gap-2
          truncate
          ${
            unread
              ? "font-semibold text-white"
              : "text-zinc-300"
          }
        `}
      >
        {starred && (
          <span title="Starred">
            ⭐
          </span>
        )}

        {archived && (
          <span title="Archived">
            📦
          </span>
        )}

        {trash && (
          <span title="Trash">
            🗑
          </span>
        )}

        <span className="truncate">
          {sent
            ? "Me"
            : getSender(
                message.from
              )}
        </span>
      </div>

      <div className="flex items-center gap-3 overflow-hidden">
        {category && (
          <span
            className={`rounded-full px-2 py-0.5 text-xs ${category.className}`}
          >
            {category.text}
          </span>
        )}

        <span
          className={`truncate ${
            unread
              ? "font-semibold text-white"
              : ""
          }`}
        >
          {message.subject}
        </span>

        <span className="truncate text-zinc-500">
          — {message.snippet}
        </span>
      </div>

      <div
        className={`
          text-right
          text-sm
          ${
            unread
              ? "font-bold text-white"
              : "text-zinc-400"
          }
        `}
      >
        {formatDate(
          message.date
        )}
      </div>
    </div>
  );
}

export default memo(
  EmailRow,
  (
    prevProps,
    nextProps
  ) =>
    prevProps.selected ===
      nextProps.selected &&
    prevProps.message.id ===
      nextProps.message.id &&
    prevProps.message.labelIds?.join(
      ","
    ) ===
      nextProps.message.labelIds?.join(
        ","
      ) &&
    prevProps.message.subject ===
      nextProps.message.subject &&
    prevProps.message.snippet ===
      nextProps.message.snippet
);