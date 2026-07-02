"use client";

import { useState } from "react";
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
  summarizeEmail,
  summarizeThread,
  generateSmartReplies,
  generateThreadReplies,
  createDraft,
  extractActions,
} from "@/services/gmail";

import { GmailMessage } from "@/types/gmail";

interface Props {
  message: GmailMessage;
  threadCount?: number;
  onRefresh: () => Promise<void>;
}

export default function EmailActions({
  message,
  threadCount = 1,
  onRefresh,
}: Props) {
  const router = useRouter();

  const queryClient =
    useQueryClient();

  const [summary, setSummary] =
    useState<any>(null);

  const [replies, setReplies] =
    useState<string[]>([]);

  const [actions, setActions] =
    useState<
      {
        task: string;
        deadline?: string;
      }[]
    >([]);

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

  const isThread =
    !!message.threadId &&
    threadCount > 1;

  const extractEmail = (
    from: string
  ) => {
    const match =
      from.match(/<(.+?)>/);

    if (match) {
      return match[1];
    }

    return from.trim();
  };

  const invalidateInbox =
    async () => {
      await queryClient.invalidateQueries(
        {
          queryKey: ["inbox"],
        }
      );

      await onRefresh();
    };

  const handleReplySelect =
    async (reply: string) => {
      try {
        const normalizedSubject =
          message.subject
            .toLowerCase()
            .startsWith("re:")
            ? message.subject
            : `Re: ${message.subject}`;

        await createDraft(
          extractEmail(
            message.from
          ),
          normalizedSubject,
          reply,
          message.threadId,
          message.messageId,
          message.messageId
        );

        router.push(
          "/drafts"
        );
      } catch (error) {
        console.error(error);
      }
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
              queryKey: ["inbox"],
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
              queryKey: ["inbox"],
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
              queryKey: ["inbox"],
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
              queryKey: ["inbox"],
            }
          );

          router.push(
            "/inbox"
          );
        },
    });

  const summarizeMutation =
    useMutation({
      mutationFn: () =>
        isThread
          ? summarizeThread(
              message.threadId
            )
          : summarizeEmail(
              message.id
            ),
      onSuccess: (
        data
      ) => {
        setSummary(
          data.summary
        );
      },
    });

  const smartReplyMutation =
    useMutation({
      mutationFn: () =>
        isThread
          ? generateThreadReplies(
              message.threadId
            )
          : generateSmartReplies(
              message.id
            ),
      onSuccess: (
        data
      ) => {
        setReplies([
          data.replies.formal,
          data.replies.casual,
          data.replies.concise,
        ]);
      },
    });

  const actionMutation =
    useMutation({
      mutationFn: () =>
        extractActions(
          message.id
        ),
      onSuccess: (
        data
      ) => {
        setActions(
          data.actions.tasks || []
        );
      },
    });

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2 flex-wrap">
        <button
          onClick={() =>
            router.back()
          }
          className="rounded-lg px-3 py-2 text-sm hover:bg-zinc-900"
        >
          ← Back
        </button>

        <button
          onClick={() =>
            summarizeMutation.mutate()
          }
          className="rounded-lg bg-purple-600 px-3 py-2 text-sm"
        >
          {summarizeMutation.isPending
            ? "Summarizing..."
            : isThread
            ? "✨ Summarize Thread"
            : "✨ Summarize Mail"}
        </button>

        <button
          onClick={() =>
            smartReplyMutation.mutate()
          }
          className="rounded-lg bg-blue-600 px-3 py-2 text-sm"
        >
          {smartReplyMutation.isPending
            ? "Generating..."
            : "⚡ Smart Replies"}
        </button>

        <button
          onClick={() =>
            actionMutation.mutate()
          }
          className="rounded-lg bg-green-600 px-3 py-2 text-sm"
        >
          {actionMutation.isPending
            ? "Extracting..."
            : "📌 Extract Actions"}
        </button>

        {isStarred ? (
          <button
            onClick={() =>
              unstarMutation.mutate()
            }
            className="rounded-lg px-3 py-2 text-sm hover:bg-zinc-900"
          >
            ☆ Unstar
          </button>
        ) : (
          <button
            onClick={() =>
              starMutation.mutate()
            }
            className="rounded-lg px-3 py-2 text-sm hover:bg-zinc-900"
          >
            ⭐ Star
          </button>
        )}

        {isUnread ? (
          <button
            onClick={() =>
              readMutation.mutate()
            }
            className="rounded-lg px-3 py-2 text-sm hover:bg-zinc-900"
          >
            ✓ Mark Read
          </button>
        ) : (
          <button
            onClick={() =>
              unreadMutation.mutate()
            }
            className="rounded-lg px-3 py-2 text-sm hover:bg-zinc-900"
          >
            ✉ Mark Unread
          </button>
        )}

        {!isTrash &&
          isInbox && (
            <button
              onClick={() =>
                archiveMutation.mutate()
              }
              className="rounded-lg px-3 py-2 text-sm hover:bg-zinc-900"
            >
              📦 Archive
            </button>
          )}

        {isArchived && (
          <button
            onClick={() =>
              unarchiveMutation.mutate()
            }
            className="rounded-lg px-3 py-2 text-sm hover:bg-zinc-900"
          >
            📥 Move to Inbox
          </button>
        )}

        {!isTrash && (
          <button
            onClick={() =>
              trashMutation.mutate()
            }
            className="rounded-lg px-3 py-2 text-sm hover:bg-zinc-900"
          >
            🗑 Trash
          </button>
        )}

        {isTrash && (
          <button
            onClick={() =>
              restoreMutation.mutate()
            }
            className="rounded-lg px-3 py-2 text-sm hover:bg-zinc-900"
          >
            ↩ Restore
          </button>
        )}
      </div>

      {summary && (
        <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-4 text-sm text-zinc-300 space-y-4">
          <div className="font-semibold">
            AI Summary
          </div>
          <div>
            {summary.short_summary}
          </div>
        </div>
      )}

      {replies.length > 0 && (
        <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-4 space-y-3">
          <div className="font-semibold">
            Smart Replies
          </div>

          {replies.map(
            (
              reply,
              index
            ) => (
              <button
                key={index}
                onClick={() =>
                  handleReplySelect(
                    reply
                  )
                }
                className="block w-full rounded-lg border border-zinc-800 px-4 py-3 text-left text-sm hover:bg-zinc-800"
              >
                {reply}
              </button>
            )
          )}
        </div>
      )}

      {actions.length > 0 && (
        <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-4 space-y-3">
          <div className="font-semibold">
            Extracted Actions
          </div>

          <ul className="list-disc pl-5 space-y-2 text-sm text-zinc-300">
            {actions.map(
              (
                action,
                index
              ) => (
                <li
                  key={index}
                  className="space-y-1"
                >
                  <div>
                    {action.task}
                  </div>

                  {action.deadline && (
                    <div className="text-xs text-zinc-500">
                      Deadline:{" "}
                      {action.deadline}
                    </div>
                  )}
                </li>
              )
            )}
          </ul>
        </div>
      )}
    </div>
  );
}