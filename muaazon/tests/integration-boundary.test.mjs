import test from 'node:test';
import assert from 'node:assert/strict';
import { createDraft, transition, STATUS, redactLog } from '../integration-boundary.mjs';
const input = () => ({provider:'leadflow',purpose:'new lead followup',createdBy:'sales-agent',
 contact:{email:'demo@example.test'},payload:{leadId:'sample-1',message:'Draft only'}});
test('draft has no external dispatch', () => {
 const d=createDraft(input());
 assert.equal(d.status,STATUS.DRAFT); assert.ok(d.payloadDigest.length===64);
 assert.equal('payload' in d,false); assert.equal('contact' in d,false);
 assert.throws(()=>transition(d,'dispatch','sales-agent'),/Invalid state/);
});
test('independent approval required', () => {
 const d=createDraft(input());
 assert.throws(()=>transition(d,'approve','sales-agent'),/Independent/);
 const approved=transition(d,'approve','reviewer');
 assert.equal(approved.status,STATUS.APPROVED);
 assert.equal(approved.approvedBy,'reviewer');
 assert.throws(()=>transition(approved,'dispatch','reviewer'),/disabled/);
});
test('rejection is terminal',()=> {
 const d=transition(createDraft(input()),'reject','reviewer');
 assert.equal(d.status,STATUS.REJECTED);
 assert.throws(()=>transition(d,'approve','reviewer'),/Invalid/);
});
test('unapproved providers and malformed payload rejected',()=>{
 assert.throws(()=>createDraft({...input(),provider:'stripe'}),/Unsupported/);
 assert.throws(()=>createDraft({...input(),contact:{email:'bad'}}),/Valid/);
 assert.throws(()=>createDraft({...input(),payload:{v:'x'.repeat(17000)}}),/large/);
});
test('audit log excludes contact and payload',()=>{
 const logged=redactLog(createDraft(input()));
 assert.equal('contact' in logged,false); assert.equal('payload' in logged,false);
});
