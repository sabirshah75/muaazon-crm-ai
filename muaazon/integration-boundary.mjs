// Muaazon integration boundary — deliberately no outbound network calls.
// ES module: Node 24, no external dependencies.
import { createHash, randomUUID } from 'node:crypto';

export const PROVIDERS = Object.freeze(['leadflow', 'agency', 'klaviyo']);
export const STATUS = Object.freeze({
  DRAFT: 'draft', APPROVED: 'approved', REJECTED: 'rejected',
  DISPATCHED: 'dispatched', FAILED: 'failed',
});
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export function createDraft({ provider, purpose, contact, payload, createdBy }) {
  if (!PROVIDERS.includes(provider)) throw new Error('Unsupported provider');
  if (!purpose || typeof purpose !== 'string' || purpose.length > 160)
    throw new Error('Purpose required (max 160 characters)');
  if (!createdBy || typeof createdBy !== 'string') throw new Error('Actor required');
  if (!contact || typeof contact.email !== 'string' || !EMAIL_RE.test(contact.email))
    throw new Error('Valid contact email required');
  if (!payload || typeof payload !== 'object' || Array.isArray(payload))
    throw new Error('Payload must be an object');
  const canonical = JSON.stringify(payload);
  if (canonical.length > 16_384) throw new Error('Payload too large');
  // Never store plaintext contact information or payloads in the audit event.
  const digest = createHash('sha256').update(canonical).digest('hex');
  return Object.freeze({
    id: randomUUID(), provider, purpose, createdBy,
    payloadDigest: digest, status: STATUS.DRAFT,
    createdAt: new Date().toISOString(), approvedBy: null,
  });
}

export function transition(draft, action, actor) {
  if (!draft || typeof actor !== 'string' || !actor.trim()) throw new Error('Actor required');
  if (draft.status === STATUS.DRAFT && action === 'approve') {
    if (draft.createdBy === actor) throw new Error('Independent approver required');
    return Object.freeze({ ...draft, status: STATUS.APPROVED, approvedBy: actor });
  }
  if (draft.status === STATUS.DRAFT && action === 'reject') {
    return Object.freeze({ ...draft, status: STATUS.REJECTED, approvedBy: null });
  }
  if (draft.status === STATUS.APPROVED && action === 'dispatch') {
    throw new Error('External dispatch disabled until adapter certification');
  }
  throw new Error('Invalid state transition');
}

export function redactLog(event) {
  const { id, provider, purpose, createdBy, approvedBy, status, payloadDigest, createdAt } = event;
  return { id, provider, purpose, createdBy, approvedBy, status, payloadDigest, createdAt };
}
