import { request } from "./httpClient";

export function listConversationsApi(token) {
  return request("/conversations/", { token });
}

export function createConversationApi(token, title = "New Conversation") {
  return request("/conversations/", {
    method: "POST",
    token,
    body: { title },
  });
}

export function listMessagesApi(token, conversationId) {
  return request(`/conversations/${conversationId}/messages`, { token });
}

export function sendMessageApi(token, conversationId, message) {
  return request(`/conversations/${conversationId}/chat`, {
    method: "POST",
    token,
    body: { message },
  });
}

export function deleteConversationApi(token, conversationId) {
  return request(`/conversations/${conversationId}`, {
    method: "DELETE",
    token,
  });
}
