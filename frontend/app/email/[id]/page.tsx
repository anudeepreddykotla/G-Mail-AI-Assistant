"use client";

import { useQuery } from "@tanstack/react-query";

import { useParams } from "next/navigation";

import AppShell from "@/components/layout/AppShell";

import EmailActions from "@/components/email/EmailActions";

import { getMessage } from "@/services/gmail";

function getSender(from: string) {
  const match =
    from.match(/^(.+?)\s*</);

  if (match) {
    return match[1];
  }

  return from;
}

function getInitials(from: string) {
  return getSender(from)
    .split(" ")
    .map((part) => part[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();
}

export default function EmailPage() {
  const params = useParams();

  const messageId =
    params.id as string;

  const {
    data: message,
    isLoading,
    refetch,
  } = useQuery({
    queryKey: [
      "message",
      messageId,
    ],
    queryFn: () =>
      getMessage(
        messageId
      ),
    staleTime: 1000 * 60 * 5,
  });

  return (
    <AppShell>
      <div className="h-full overflow-y-auto">
        {isLoading ? (
          <div className="p-6">
            Loading email...
          </div>
        ) : !message ? (
          <div className="p-6">
            Email not found
          </div>
        ) : (
          <>
            <div
              className="
                sticky
                top-0
                z-50
                border-b
                border-zinc-800
                bg-black
                px-6
                py-4
              "
            >
              <EmailActions
                message={message}
                onRefresh={
                  async () => {
                    await refetch();
                  }
                }
              />
            </div>

            <div className="mx-auto max-w-6xl p-8">
              <h1 className="mb-6 text-3xl font-bold">
                {message.subject}
              </h1>

              <div
                className="
                  mb-8
                  flex
                  items-start
                  gap-4
                  border-b
                  border-zinc-800
                  pb-6
                "
              >
                <div
                  className="
                    flex
                    h-12
                    w-12
                    items-center
                    justify-center
                    rounded-full
                    bg-blue-600
                    font-semibold
                    text-white
                  "
                >
                  {getInitials(
                    message.from
                  )}
                </div>

                <div className="flex-1">
                  <div className="font-medium">
                    {getSender(
                      message.from
                    )}
                  </div>

                  <div className="mt-1 text-sm text-zinc-400">
                    {message.from}
                  </div>

                  {message.to && (
                    <div className="mt-1 text-sm text-zinc-500">
                      To: {message.to}
                    </div>
                  )}
                </div>

                <div className="text-sm text-zinc-500">
                  {message.date}
                </div>
              </div>

              <div
                className="
                  overflow-hidden
                  rounded-xl
                  border
                  border-zinc-800
                  bg-zinc-900
                "
              >
                {message.htmlBody ? (
                  <iframe
                    title="email"
                    srcDoc={
                      message.htmlBody
                    }
                    className="
                      min-h-[1000px]
                      w-full
                      border-0
                      bg-white
                    "
                  />
                ) : (
                  <div
                    className="
                      whitespace-pre-wrap
                      break-words
                      p-6
                      text-base
                      leading-8
                    "
                  >
                    {message.body}
                  </div>
                )}
              </div>
            </div>
          </>
        )}
      </div>
    </AppShell>
  );
}