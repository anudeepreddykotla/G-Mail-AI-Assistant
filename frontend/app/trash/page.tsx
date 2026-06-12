"use client";

import { useEffect, useState } from "react";

import AppShell from "@/components/layout/AppShell";

import EmailTable from "@/components/email/EmailTable";
import EmailToolbar from "@/components/email/EmailToolbar";

import {
  getMessages,
  searchMessages,
} from "@/services/gmail";

import { GmailMessage } from "@/types/gmail";

export default function TrashPage() {
  const [messages, setMessages] =
    useState<GmailMessage[]>([]);

  const [loading, setLoading] =
    useState(true);

  const [selectedIds, setSelectedIds] =
    useState<string[]>([]);

  const [searchQuery, setSearchQuery] =
    useState("");

  const [nextPageToken, setNextPageToken] =
    useState<string>();

  const [loadingMore, setLoadingMore] =
    useState(false);

  const loadMessages = async () => {
    try {
      const response =
        await getMessages({
          maxResults: 50,
          labelIds: ["TRASH"],
          includeSpamTrash: true,
        });

      setMessages(
        response.messages
      );

      setNextPageToken(
        response.nextPageToken
      );
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const loadMore =
    async () => {
      if (
        !nextPageToken ||
        loadingMore
      ) {
        return;
      }

      try {
        setLoadingMore(true);

        const response =
          await getMessages({
            maxResults: 50,
            labelIds: ["TRASH"],
            includeSpamTrash: true,
            pageToken:
              nextPageToken,
          });

        setMessages((prev) => [
          ...prev,
          ...response.messages,
        ]);

        setNextPageToken(
          response.nextPageToken
        );
      } catch (error) {
        console.error(error);
      } finally {
        setLoadingMore(false);
      }
    };

  const toggleSelect = (
    id: string
  ) => {
    setSelectedIds((prev) =>
      prev.includes(id)
        ? prev.filter(
            (item) => item !== id
          )
        : [...prev, id]
    );
  };

  useEffect(() => {
    loadMessages();
  }, []);

  useEffect(() => {
    const runSearch =
      async () => {
        try {
          if (
            searchQuery.trim() === ""
          ) {
            await loadMessages();
            return;
          }

          const response =
            await searchMessages(
              searchQuery
            );

          setMessages(
            response.messages.filter(
              (message) =>
                message.labelIds?.includes(
                  "TRASH"
                )
            )
          );
        } catch (error) {
          console.error(error);
        }
      };

    const timer = setTimeout(
      runSearch,
      400
    );

    return () =>
      clearTimeout(timer);
  }, [searchQuery]);

  return (
    <AppShell>
      <div className="flex h-full flex-col">
        <EmailToolbar
          onRefresh={loadMessages}
          selectedIds={selectedIds}
          clearSelection={() =>
            setSelectedIds([])
          }
          searchQuery={searchQuery}
          onSearchChange={
            setSearchQuery
          }
        />

        <div className="flex-1 overflow-auto">
          {loading ? (
            <p className="p-4">
              Loading emails...
            </p>
          ) : (
            <>
              <EmailTable
                messages={messages}
                selectedIds={selectedIds}
                onToggleSelect={
                  toggleSelect
                }
              />

              {nextPageToken && (
                <div className="p-4">
                  <button
                    onClick={
                      loadMore
                    }
                    disabled={
                      loadingMore
                    }
                    className="
                      w-full
                      rounded-lg
                      border
                      border-zinc-800
                      px-4
                      py-3
                      hover:bg-zinc-900
                    "
                  >
                    {loadingMore
                      ? "Loading..."
                      : "Load More"}
                  </button>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </AppShell>
  );
}