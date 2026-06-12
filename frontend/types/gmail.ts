export interface GmailMessage {
  id: string;
  threadId: string;

  subject: string;

  from: string;

  to?: string;

  date: string;

  snippet: string;

  body?: string;

  htmlBody?: string;

  labelIds?: string[];
}

export interface GmailMessagesResponse {
  count: number;

  messages: GmailMessage[];

  nextPageToken?: string;
}

export interface GmailDraft {
  id: string;

  messageId: string;

  threadId?: string;

  subject: string;

  to: string;

  snippet: string;

  body: string;
}

export interface GmailDraftsResponse {
  count: number;

  drafts: GmailDraft[];
}