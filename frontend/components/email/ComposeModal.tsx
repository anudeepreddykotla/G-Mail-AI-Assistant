"use client";

import {
  useEffect,
  useState,
} from "react";

import { sendEmail } from "@/services/gmail";

interface Props {
  open: boolean;

  onClose: () => void;

  initialTo?: string;

  initialSubject?: string;

  initialBody?: string;

  title?: string;
}

export default function ComposeModal({
  open,
  onClose,
  initialTo = "",
  initialSubject = "",
  initialBody = "",
  title = "New Message",
}: Props) {
  const [to, setTo] =
    useState("");

  const [subject, setSubject] =
    useState("");

  const [body, setBody] =
    useState("");

  const [sending, setSending] =
    useState(false);

  useEffect(() => {
    if (open) {
      setTo(initialTo);
      setSubject(initialSubject);
      setBody(initialBody);
    }
  }, [
    open,
    initialTo,
    initialSubject,
    initialBody,
  ]);

  if (!open) return null;

  const handleSend =
    async () => {
      try {
        setSending(true);

        await sendEmail(
          to,
          subject,
          body
        );

        setTo("");
        setSubject("");
        setBody("");

        onClose();
      } catch (error) {
        console.error(error);
      } finally {
        setSending(false);
      }
    };

  return (
    <div
      className="
        fixed
        inset-0
        z-50
        flex
        items-center
        justify-center
        bg-black/60
      "
    >
      <div
        className="
          w-full
          max-w-2xl
          rounded-xl
          border
          border-zinc-800
          bg-zinc-950
          p-6
        "
      >
        <h2 className="mb-4 text-xl font-semibold">
          {title}
        </h2>

        <input
          value={to}
          onChange={(e) =>
            setTo(e.target.value)
          }
          placeholder="To"
          className="
            mb-3
            w-full
            rounded
            border
            border-zinc-800
            bg-black
            p-3
          "
        />

        <input
          value={subject}
          onChange={(e) =>
            setSubject(
              e.target.value
            )
          }
          placeholder="Subject"
          className="
            mb-3
            w-full
            rounded
            border
            border-zinc-800
            bg-black
            p-3
          "
        />

        <textarea
          value={body}
          onChange={(e) =>
            setBody(e.target.value)
          }
          placeholder="Write your email..."
          rows={12}
          className="
            mb-4
            w-full
            rounded
            border
            border-zinc-800
            bg-black
            p-3
          "
        />

        <div className="flex justify-end gap-2">
          <button
            onClick={onClose}
            className="
              rounded
              px-4
              py-2
              hover:bg-zinc-900
            "
          >
            Cancel
          </button>

          <button
            onClick={handleSend}
            disabled={sending}
            className="
              rounded
              bg-blue-600
              px-4
              py-2
            "
          >
            {sending
              ? "Sending..."
              : "Send"}
          </button>
        </div>
      </div>
    </div>
  );
}