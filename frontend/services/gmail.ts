import api from "./api";

import {
  GmailMessage,
  GmailMessagesResponse,
} from "@/types/gmail";

interface GetMessagesParams {
  maxResults?: number;
  labelIds?: string[];
  includeSpamTrash?: boolean;
  pageToken?: string;
}

export const getMessages =
  async (
    params?: GetMessagesParams
  ): Promise<GmailMessagesResponse> => {
    const response = await api.get(
      "/gmail/messages",
      {
        params: {
          max_results:
            params?.maxResults,
          label_id:
            params?.labelIds?.[0],
          include_spam_trash:
            params?.includeSpamTrash,
          page_token:
            params?.pageToken,
        },
      }
    );

    return response.data;
  };

export const getMessage =
  async (
    id: string
  ): Promise<GmailMessage> => {
    const response = await api.get(
      `/gmail/messages/${id}`
    );

    return response.data;
  };

export const getThread =
  async (
    threadId: string
  ) => {
    const response =
      await api.get(
        `/gmail/threads/${threadId}`
      );

    return response.data;
  };

export const markRead =
  async (id: string) => {
    const response = await api.post(
      `/gmail/messages/${id}/read`
    );

    return response.data;
  };

export const markUnread =
  async (id: string) => {
    const response = await api.post(
      `/gmail/messages/${id}/unread`
    );

    return response.data;
  };

export const starMessage =
  async (id: string) => {
    const response = await api.post(
      `/gmail/messages/${id}/star`
    );

    return response.data;
  };

export const unstarMessage =
  async (id: string) => {
    const response = await api.post(
      `/gmail/messages/${id}/unstar`
    );

    return response.data;
  };

export const archiveMessage =
  async (id: string) => {
    const response = await api.post(
      `/gmail/messages/${id}/archive`
    );

    return response.data;
  };

export const unarchiveMessage =
  async (id: string) => {
    const response = await api.post(
      `/gmail/messages/${id}/unarchive`
    );

    return response.data;
  };

export const trashMessage =
  async (id: string) => {
    const response = await api.post(
      `/gmail/messages/${id}/trash`
    );

    return response.data;
  };

export const restoreMessage =
  async (id: string) => {
    const response = await api.post(
      `/gmail/messages/${id}/restore`
    );

    return response.data;
  };

export const sendEmail =
  async (
    to: string,
    subject: string,
    body: string
  ) => {
    const response = await api.post(
      "/gmail/send",
      {
        to,
        subject,
        body,
      }
    );

    return response.data;
  };

export const replyToMessage =
  async (
    messageId: string,
    body: string
  ) => {
    const response = await api.post(
      `/gmail/messages/${messageId}/reply`,
      {
        body,
      }
    );

    return response.data;
  };

export const searchMessages =
  async (
    query: string
  ): Promise<GmailMessagesResponse> => {
    const response = await api.get(
      "/gmail/search",
      {
        params: {
          q: query,
        },
      }
    );

    return {
      count: response.data.count,
      messages:
        response.data.messages,
    };
  };

export const getDrafts =
  async () => {
    const response =
      await api.get(
        "/gmail/drafts"
      );

    return response.data;
  };

export const getDraft =
  async (
    draftId: string
  ) => {
    const response =
      await api.get(
        `/gmail/drafts/${draftId}`
      );

    return response.data;
  };

export const deleteDraft =
  async (
    draftId: string
  ) => {
    const response =
      await api.delete(
        `/gmail/drafts/${draftId}`
      );

    return response.data;
  };

// AI FEATURES

export const summarizeEmail =
  async (
    messageId: string
  ) => {
    const response =
      await api.post(
        `/ai/messages/${messageId}/summarize`
      );

    return response.data;
  };

export const summarizeThread =
  async (
    threadId: string
  ) => {
    const response =
      await api.post(
        `/ai/threads/${threadId}/summarize`
      );

    return response.data;
  };

export const generateSmartReplies =
  async (
    messageId: string
  ) => {
    const response =
      await api.post(
        `/ai/messages/${messageId}/reply`
      );

    return response.data;
  };

export const generateThreadReplies =
  async (
    threadId: string
  ) => {
    const response =
      await api.post(
        `/ai/threads/${threadId}/reply`
      );

    return response.data;
  };

export const extractActions =
  async (
    messageId: string
  ) => {
    const response =
      await api.post(
        `/ai/messages/${messageId}/extract`
      );

    return response.data;
  };

export const createDraft =
  async (
    to: string,
    subject: string,
    body: string,
    threadId?: string,
    inReplyTo?: string,
    references?: string
  ) => {
    const response =
      await api.post(
        "/gmail/drafts",
        {
          to,
          subject,
          body,
          thread_id: threadId,
          in_reply_to:
            inReplyTo,
          references,
        }
      );

    return response.data;
  };

export const updateDraft =
  async (
    draftId: string,
    to: string,
    subject: string,
    body: string,
    threadId?: string,
    inReplyTo?: string,
    references?: string
  ) => {
    const response =
      await api.put(
        `/gmail/drafts/${draftId}`,
        {
          to,
          subject,
          body,
          thread_id: threadId,
          in_reply_to:
            inReplyTo,
          references,
        }
      );

    return response.data;
  };

export const sendDraft =
  async (
    draftId: string
  ) => {
    const response =
      await api.post(
        `/gmail/drafts/${draftId}/send`
      );

    return response.data;
  };