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


// AI TYPES

export interface EmailSummaryResponse {
  message_id: string;

  summary: string;
}

export interface SmartReplyResponse {
  message_id: string;

  replies: string[];
}

export interface ActionExtractionResponse {
  message_id: string;

  actions: string[];
}

export interface PriorityResponse {
  message_id: string;

  priority: string;
}