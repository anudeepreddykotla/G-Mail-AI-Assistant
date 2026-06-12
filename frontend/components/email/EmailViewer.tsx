"use client";

import { GmailMessage } from "@/types/gmail";

interface EmailViewerProps {
  message: GmailMessage | null;
}

function getSender(from: string) {
  const match = from.match(/^(.+?)\s*</);

  if (match) {
    return match[1];
  }

  return from;
}

function getInitials(from: string) {
  const sender = getSender(from);

  return sender
    .split(" ")
    .map((s) => s[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();
}

export default function EmailViewer({
  message,
}: EmailViewerProps) {
  if (!message) {
    return (
      <div className="flex h-full items-center justify-center text-zinc-500">
        Select an email
      </div>
    );
  }

  return (
    <div className="h-full overflow-y-auto bg-zinc-950">
      <div className="mx-auto max-w-5xl p-8">
        <div className="mb-8">
          <h1 className="mb-6 text-3xl font-semibold text-white">
            {message.subject}
          </h1>

          <div className="flex items-start gap-4">
            <div
              className="
                flex
                h-10
                w-10
                items-center
                justify-center
                rounded-full
                bg-blue-600
                font-medium
                text-white
              "
            >
              {getInitials(
                message.from
              )}
            </div>

            <div className="flex-1">
              <div className="flex items-center gap-2">
                <span className="font-medium text-white">
                  {getSender(
                    message.from
                  )}
                </span>

                <span className="text-zinc-500">
                  &lt;
                  {
                    message.from.match(
                      /<(.+?)>/
                    )?.[1]
                  }
                  &gt;
                </span>
              </div>

              {message.to && (
                <div className="mt-1 text-sm text-zinc-400">
                  To: {message.to}
                </div>
              )}
            </div>

            <div className="text-sm text-zinc-500">
              {message.date}
            </div>
          </div>
        </div>

        <div
          className="
            rounded-xl
            border
            border-zinc-800
            bg-zinc-900
            p-6
          "
        >
          {message.htmlBody ? (
            <div
              className="
                prose
                prose-invert
                max-w-none
              "
              dangerouslySetInnerHTML={{
                __html:
                  message.htmlBody,
              }}
            />
          ) : (
            <div className="whitespace-pre-wrap text-sm leading-7 text-zinc-200">
              {message.body}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}