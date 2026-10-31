// Provider-neutral, approval-only AI draft generator.
// Not wired to live CRM or external providers by default. No automatic sending.
const LOCAL_HOSTS = Object.freeze(['localhost', '127.0.0.1', '[::1]']);

export async function generateAiDraft({
  endpoint, apiKey, model, messages, consent = false,
  allowedHosts = LOCAL_HOSTS, fetchImpl = globalThis.fetch, timeoutMs = 15_000,
}) {
  if (consent !== true) throw new Error('Explicit data-processing consent required');
  if (typeof endpoint !== 'string' || typeof model !== 'string' || !model.trim())
    throw new Error('Endpoint and model required');
  const url = new URL(endpoint);
  const hostname = url.hostname.toLowerCase();
  if (!allowedHosts.includes(hostname)) throw new Error('AI provider host not allowlisted');
  if (url.username || url.password || url.search || url.hash)
    throw new Error('Provider endpoint must not contain credentials or query parameters');
  if (!['/v1/chat/completions', '/chat/completions'].includes(url.pathname))
    throw new Error('Expected chat-completions API endpoint');
  if (url.protocol !== 'https:' && !(url.protocol === 'http:' && LOCAL_HOSTS.includes(hostname)))
    throw new Error('TLS required for nonlocal AI providers');
  if (!LOCAL_HOSTS.includes(hostname) && !apiKey)
    throw new Error('API key required for remote provider');
  if (!Array.isArray(messages) || messages.length === 0 || messages.length > 12 ||
      !messages.every(m => m && ['system','user','assistant'].includes(m.role) &&
        typeof m.content === 'string' && m.content.length <= 8000))
    throw new Error('Invalid or oversized messages');
  if (!Number.isInteger(timeoutMs) || timeoutMs < 1000 || timeoutMs > 60000)
    throw new Error('Invalid request timeout');
  const response = await fetchImpl(url.toString(), {
    method:'POST',
    headers:{
      'content-type':'application/json',
      ...(apiKey ? {authorization:`Bearer ${apiKey}`} : {}),
    },
    body:JSON.stringify({model, messages, temperature:0.2, max_tokens:800}),
    signal:AbortSignal.timeout(timeoutMs),
    redirect:'error',
  });
  if (!response.ok) throw new Error(`AI provider request failed (HTTP ${response.status})`);
  const payload = await response.json();
  const text = payload?.choices?.[0]?.message?.content;
  if (typeof text !== 'string' || !text.trim() || text.length > 16000)
    throw new Error('Invalid AI response');
  return Object.freeze({
    text:text.trim(), model, state:'draft',
    reviewRequired:true, autoSend:false,
  });
}
