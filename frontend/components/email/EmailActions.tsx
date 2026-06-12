"use client";

import { useRouter } from "next/navigation";

import {
  useMutation,
  useQueryClient,
} from "@tanstack/react-query";

import {
  archiveMessage,
  unarchiveMessage,
  markRead,
  markUnread,
  starMessage,
  unstarMessage,
  trashMessage,
  restoreMessage,
} from "@/services/gmail";

import { GmailMessage } from "@/types/gmail";

interface Props {
  message: GmailMessage;

  onRefresh: () => Promise<void>;
}

export default function EmailActions({
  message,
  onRefresh,
}: Props) {
  const router = useRouter();

  const queryClient =
    useQueryClient();

  const labels =
    message.labelIds || [];

  const isUnread =
    labels.includes("UNREAD");

  const isStarred =
    labels.includes("STARRED");

  const isTrash =
    labels.includes("TRASH");

  const isInbox =
    labels.includes("INBOX");

  const isArchived =
    !labels.includes("INBOX") &&
    !labels.includes("TRASH") &&
    !labels.includes("SENT") &&
    !labels.includes("DRAFT");

  const invalidateInbox =
    async () => {
      await queryClient.invalidateQueries(
        {
          queryKey: ["inbox"],
        }
      );

      await onRefresh();
    };

  const readMutation =
    useMutation({
      mutationFn: () =>
        markRead(message.id),
      onSuccess:
        invalidateInbox,
    });

  const unreadMutation =
    useMutation({
      mutationFn: () =>
        markUnread(message.id),
      onSuccess:
        invalidateInbox,
    });

  const starMutation =
    useMutation({
      mutationFn: () =>
        starMessage(message.id),
      onSuccess:
        invalidateInbox,
    });

  const unstarMutation =
    useMutation({
      mutationFn: () =>
        unstarMessage(
          message.id
        ),
      onSuccess:
        invalidateInbox,
    });

  const archiveMutation =
    useMutation({
      mutationFn: () =>
        archiveMessage(
          message.id
        ),
      onSuccess:
        async () => {
          await queryClient.invalidateQueries(
            {
              queryKey: [
                "inbox",
              ],
            }
          );

          router.push(
            "/inbox"
          );
        },
    });

  const unarchiveMutation =
    useMutation({
      mutationFn: () =>
        unarchiveMessage(
          message.id
        ),
      onSuccess:
        async () => {
          await queryClient.invalidateQueries(
            {
              queryKey: [
                "inbox",
              ],
            }
          );

          router.push(
            "/inbox"
          );
        },
    });

  const trashMutation =
    useMutation({
      mutationFn: () =>
        trashMessage(
          message.id
        ),
      onSuccess:
        async () => {
          await queryClient.invalidateQueries(
            {
              queryKey: [
                "inbox",
              ],
            }
          );

          router.push(
            "/inbox"
          );
        },
    });

  const restoreMutation =
    useMutation({
      mutationFn: () =>
        restoreMessage(
          message.id
        ),
      onSuccess:
        async () => {
          await queryClient.invalidateQueries(
            {
              queryKey: [
                "inbox",
              ],
            }
          );

          router.push(
            "/inbox"
          );
        },
    });

  return (
    <div
      className="
        flex
        items-center
        gap-2
        flex-wrap
      "
    >
      <button
        onClick={() =>
          router.back()
        }
        className="
          rounded-lg
          px-3
          py-2
          text-sm
          hover:bg-zinc-900
        "
      >
        ← Back
      </button>

      {isStarred ? (
        <button
          onClick={() =>
            unstarMutation.mutate()
          }
          className="
            rounded-lg
            px-3
            py-2
            text-sm
            hover:bg-zinc-900
          "
        >
          ☆ Unstar
        </button>
      ) : (
        <button
          onClick={() =>
            starMutation.mutate()
          }
          className="
            rounded-lg
            px-3
            py-2
            text-sm
            hover:bg-zinc-900
          "
        >
          ⭐ Star
        </button>
      )}

      {isUnread ? (
        <button
          onClick={() =>
            readMutation.mutate()
          }
          className="
            rounded-lg
            px-3
            py-2
            text-sm
            hover:bg-zinc-900
          "
        >
          ✓ Mark Read
        </button>
      ) : (
        <button
          onClick={() =>
            unreadMutation.mutate()
          }
          className="
            rounded-lg
            px-3
            py-2
            text-sm
            hover:bg-zinc-900
          "
        >
          ✉ Mark Unread
        </button>
      )}

      {!isTrash && isInbox && (
        <button
          onClick={() =>
            archiveMutation.mutate()
          }
          className="
            rounded-lg
            px-3
            py-2
            text-sm
            hover:bg-zinc-900
          "
        >
          📦 Archive
        </button>
      )}

      {isArchived && (
        <button
          onClick={() =>
            unarchiveMutation.mutate()
          }
          className="
            rounded-lg
            px-3
            py-2
            text-sm
            hover:bg-zinc-900
          "
        >
          📥 Move to Inbox
        </button>
      )}

      {!isTrash && (
        <button
          onClick={() =>
            trashMutation.mutate()
          }
          className="
            rounded-lg
            px-3
            py-2
            text-sm
            hover:bg-zinc-900
          "
        >
          🗑 Trash
        </button>
      )}

      {isTrash && (
        <button
          onClick={() =>
            restoreMutation.mutate()
          }
          className="
            rounded-lg
            px-3
            py-2
            text-sm
            hover:bg-zinc-900
          "
        >
          ↩ Restore
        </button>
      )}
    </div>
  );
}