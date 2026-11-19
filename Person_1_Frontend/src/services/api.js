const API_URL = import.meta.env.VITE_API_URL;

/**
 * Sends the response object to the backend / AI service.
 * If VITE_API_URL is not set, it just resolves so the UI can be demoed standalone.
 * TEAM: agree on the endpoint + response shape and update this one function.
 */
export async function submitResponse(payload) {
  if (!API_URL) {
    console.info("[UnboxJoy] No VITE_API_URL set. Payload:", payload);
    return { ok: true, mocked: true };
  }

  const res = await fetch(`${API_URL}/recommendations`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(`Request failed (${res.status})`);
  return res.json();
}
