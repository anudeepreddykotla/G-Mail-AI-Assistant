"use client";

import { GmailMessage } from "@/types/gmail";

interface EmailListProps {
  messages: GmailMessage[];
  selectedMessageId?: string;
  onSelect: (message: GmailMessage) => void;
}

export default function EmailList({
  messages,
  selectedMessageId,
  onSelect,
}: EmailListProps) {
  return (
    <div className="flex flex-col overflow-auto">
      {messages.map((message) => (
        <div
          key={message.id}
          onClick={() => onSelect(message)}
          className={`cursor-pointer border-b p-4 transition ${
            selectedMessageId === message.id
              ? "bg-blue-50"
              : "hover:bg-gray-50"
          }`}
        >
          <div className="flex items-center justify-between">
            <p className="font-medium truncate">
              {message.from}
            </p>

            <p className="text-sm text-gray-500">
              {new Date(
                message.date
              ).toLocaleDateString()}
            </p>
          </div>

          <h3 className="mt-1 font-semibold truncate">
            {message.subject}
          </h3>

          <p className="mt-1 truncate text-sm text-gray-600">
            {message.snippet}
          </p>
        </div>
      ))}
    </div>
  );
}