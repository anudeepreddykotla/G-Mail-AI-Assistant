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