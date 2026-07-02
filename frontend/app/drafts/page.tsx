"use client";

import {
  useEffect,
  useState,
} from "react";

import AppShell from "@/components/layout/AppShell";
import ComposeModal from "@/components/email/ComposeModal";

import {
  getDrafts,
  deleteDraft,
} from "@/services/gmail";

import {
  GmailDraft,
} from "@/types/gmail";

export default function DraftsPage() {
  const [drafts, setDrafts] =
    useState<GmailDraft[]>([]);

  const [loading, setLoading] =
    useState(true);

  const [selectedDraft, setSelectedDraft] =
    useState<GmailDraft | null>(
      null
    );

  const [composeOpen, setComposeOpen] =
    useState(false);

  const loadDrafts = async () => {
    try {
      setLoading(true);

      const response =
        await getDrafts();

      setDrafts(
        response.drafts
      );
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete =
    async (
      draftId: string
    ) => {
      try {
        await deleteDraft(
          draftId
        );

        setDrafts((prev) =>
          prev.filter(
            (draft) =>
              draft.id !== draftId
          )
        );
      } catch (error) {
        console.error(error);
      }
    };

  const handleOpenDraft = (
    draft: GmailDraft
  ) => {
    setSelectedDraft(draft);
    setComposeOpen(true);
  };

  const handleCloseCompose =
    () => {
      setComposeOpen(false);

      setSelectedDraft(
        null
      );

      loadDrafts();
    };

  useEffect(() => {
    loadDrafts();
  }, []);

  return (
    <AppShell>
      <div className="flex h-full flex-col">
        <div
          className="
            border-b
            border-zinc-800
            px-6
            py-4
          "
        >
          <h1
            className="
              text-xl
              font-semibold
            "
          >
            Drafts
          </h1>
        </div>

        <div className="flex-1 overflow-y-auto">
          {loading ? (
            <div className="p-6">
              Loading drafts...
            </div>
          ) : drafts.length === 0 ? (
            <div className="p-6 text-zinc-500">
              No drafts found
            </div>
          ) : (
            drafts.map(
              (draft) => (
                <div
                  key={draft.id}
                  onClick={() =>
                    handleOpenDraft(
                      draft
                    )
                  }
                  className="
                    cursor-pointer
                    border-b
                    border-zinc-800
                    px-6
                    py-4
                    hover:bg-zinc-900
                  "
                >
                  <div
                    className="
                      flex
                      items-start
                      justify-between
                      gap-4
                    "
                  >
                    <div className="flex-1">
                      <div className="font-medium">
                        {draft.subject ||
                          "(No Subject)"}
                      </div>

                      <div
                        className="
                          mt-1
                          text-sm
                          text-zinc-400
                        "
                      >
                        To: {draft.to}
                      </div>

                      <div
                        className="
                          mt-2
                          text-sm
                          text-zinc-500
                        "
                      >
                        {draft.snippet}
                      </div>
                    </div>

                    <button
                      onClick={(e) => {
                        e.stopPropagation();

                        handleDelete(
                          draft.id
                        );
                      }}
                      className="
                        rounded-lg
                        px-3
                        py-2
                        text-sm
                        text-red-400
                        hover:bg-zinc-900
                      "
                    >
                      Delete
                    </button>
                  </div>
                </div>
              )
            )
          )}
        </div>
      </div>
      <ComposeModal
        open={composeOpen}
        onClose={
          handleCloseCompose
        }
        title="Edit Draft"
        draftId={
          selectedDraft?.id
        }
        threadId={
          selectedDraft?.threadId
        }
        initialTo={
          selectedDraft?.to
        }
        initialSubject={
          selectedDraft?.subject
        }
        initialBody={
          selectedDraft?.body
        }
      />
    </AppShell>
  );
}