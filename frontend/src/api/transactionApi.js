import { apiRequest } from "./apiClient";
const PREFIX = "/transactions"

export async function transferFunds(owner_id="9f6e28e9-23d1-4829-8a9b-1f59d12ae4c6", fromAccountId=82549698, toUserId="30563c62-6451-4aa3-b880-2f2fc26d149a", toAccountId=79284522, amount=2) {
  return apiRequest(PREFIX + "/transfer", {
    method: "POST",
    body: JSON.stringify({
        owner_id: owner_id,
      from_account_number: fromAccountId,
      to_owner_id: toUserId,
      to_account_number: toAccountId,
      amount: amount,
    }),
  });
}


export async function depositFunds(accountId, amount) {
  return apiRequest(PREFIX + "/deposit", {
    method: "POST",
    body: JSON.stringify({
        account_number: accountId,
        amount: amount,
    }),
  });
}

export async function withdrawalFunds(accountId, amount) {
  return apiRequest(PREFIX + "/withdraw", {
    method: "POST",
    body: JSON.stringify({
        account_number: accountId,
        amount: amount,
    }),
  });
}