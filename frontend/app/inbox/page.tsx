"use client";

import {
  useCallback,
  useEffect,
  useMemo,
  useState,
} from "react";

import debounce from "lodash/debounce";

import {
  useInfiniteQuery,
} from "@tanstack/react-query";

import AppShell from "@/components/layout/AppShell";

import EmailTable from "@/components/email/EmailTable";
import EmailToolbar from "@/components/email/EmailToolbar";

import {
  getMessages,
  searchMessages,
} from "@/services/gmail";

import { GmailMessage } from "@/types/gmail";

export default function InboxPage() {
  const [selectedIds, setSelectedIds] =
    useState<string[]>([]);

  const [searchQuery, setSearchQuery] =
    useState("");

  const [searchResults, setSearchResults] =
    useState<GmailMessage[] | null>(
      null
    );

  const {
    data,
    isLoading,
    refetch,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
  } = useInfiniteQuery({
    queryKey: ["inbox"],
    initialPageParam: null as string | null,
    queryFn: ({ pageParam }) =>
      getMessages({
        maxResults: 20,
        pageToken:
          pageParam || undefined,
      }),
    getNextPageParam: (
      lastPage
    ) =>
      lastPage?.nextPageToken ??
      undefined,
  });

  const messages =
    useMemo(() => {
      if (searchResults) {
        return searchResults;
      }

      const pages =
        data?.pages ?? [];

      return pages.flatMap(
        (page) =>
          page.messages ?? []
      );
    }, [
      data,
      searchResults,
    ]);

  const debouncedSearch =
    useMemo(
      () =>
        debounce(
          async (
            query: string
          ) => {
            try {
              if (
                query.trim() === ""
              ) {
                setSearchResults(
                  null
                );

                await refetch();

                return;
              }

              const response =
                await searchMessages(
                  query
                );

              setSearchResults(
                response.messages
              );
            } catch (error) {
              console.error(
                error
              );
            }
          },
          400
        ),
      [refetch]
    );

  const loadMore =
    useCallback(
      async () => {
        if (
          searchQuery.trim() !==
            "" ||
          !hasNextPage ||
          isFetchingNextPage
        ) {
          return;
        }

        await fetchNextPage();
      },
      [
        searchQuery,
        hasNextPage,
        isFetchingNextPage,
        fetchNextPage,
      ]
    );

  const toggleSelect =
    useCallback(
      (id: string) => {
        setSelectedIds(
          (prev) =>
            prev.includes(id)
              ? prev.filter(
                  (item) =>
                    item !== id
                )
              : [
                  ...prev,
                  id,
                ]
        );
      },
      []
    );

  useEffect(() => {
    debouncedSearch(
      searchQuery
    );

    return () =>
      debouncedSearch.cancel();
  }, [
    searchQuery,
    debouncedSearch,
  ]);

  return (
    <AppShell>
      <div className="flex h-full flex-col">
        <EmailToolbar
          onRefresh={async () => {
            await refetch();
          }}
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
          {isLoading ? (
            <p className="p-4">
              Loading emails...
            </p>
          ) : (
            <EmailTable
              messages={messages}
              selectedIds={selectedIds}
              onToggleSelect={
                toggleSelect
              }
              onEndReached={
                loadMore
              }
            />
          )}
        </div>
      </div>
    </AppShell>
  );
}