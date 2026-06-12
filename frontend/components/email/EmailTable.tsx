"use client";

import {
  memo,
  useMemo,
} from "react";

import {
  List,
  type ListChildComponentProps,
} from "react-window";

import { GmailMessage } from "@/types/gmail";

import EmailRow from "./EmailRow";

interface Props {
  messages: GmailMessage[];

  selectedIds: string[];

  onToggleSelect: (
    id: string
  ) => void;

  onEndReached?: () => void;
}

interface RowData {
  messages: GmailMessage[];

  selectedSet: Set<string>;

  onToggleSelect: (
    id: string
  ) => void;
}

function Row({
  index,
  style,
  messages,
  selectedSet,
  onToggleSelect,
}: ListChildComponentProps<RowData>) {
  const message =
    messages[index];

  return (
    <div style={style}>
      <EmailRow
        message={message}
        selected={selectedSet.has(
          message.id
        )}
        onToggleSelect={
          onToggleSelect
        }
      />
    </div>
  );
}

function EmailTable({
  messages,
  selectedIds,
  onToggleSelect,
  onEndReached,
}: Props) {
  const selectedSet =
    useMemo(
      () =>
        new Set(selectedIds),
      [selectedIds]
    );

  const rowData =
    useMemo(
      () => ({
        messages,
        selectedSet,
        onToggleSelect,
      }),
      [
        messages,
        selectedSet,
        onToggleSelect,
      ]
    );

  return (
    <div className="flex h-full flex-col">
      <div
        className="
          grid
          grid-cols-[24px_220px_1fr_120px]
          gap-4
          border-b
          border-zinc-800
          px-4
          py-2
          text-xs
          uppercase
          tracking-wide
          text-zinc-500
        "
      >
        <div></div>
        <div>From</div>
        <div>Subject</div>
        <div className="text-right">
          Date
        </div>
      </div>

      <div className="flex-1 overflow-hidden">
        <List
          rowComponent={Row}
          rowCount={
            messages.length
          }
          rowHeight={64}
          rowProps={rowData}
          onRowsRendered={({
            stopIndex,
          }) => {
            if (
              stopIndex >=
              messages.length - 3
            ) {
              onEndReached?.();
            }
          }}
          style={{
            height: "100%",
            width: "100%",
          }}
        />
      </div>
    </div>
  );
}

export default memo(
  EmailTable
);