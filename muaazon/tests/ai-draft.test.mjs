import test from 'node:test';
import assert from 'node:assert/strict';
import {generateAiDraft} from '../ai-draft.mjs';
const base=()=>({
 endpoint:'http://localhost:4020/v1/chat/completions',
 model:'local-test-model',
 consent:true,
 messages:[{role:'user',content:'Write a polite follow-up to a synthetic lead'}],
 fetchImpl:async()=>({ok:true,status:200,json:async()=>({
  choices:[{message:{content:'Draft follow-up, do not send'}}],
 })}),
});
test('accepts local model response as draft only',async()=>{
 const result=await generateAiDraft(base());
 assert.equal(result.text,'Draft follow-up, do not send');
 assert.equal(result.autoSend,false);
 assert.equal(result.reviewRequired,true);
 assert.equal(result.state,'draft');
});
test('rejects missing consent and unallowlisted hosts',async()=>{
 await assert.rejects(generateAiDraft({...base(),consent:false}),/consent/);
 await assert.rejects(generateAiDraft({...base(),endpoint:'https://evil.example/v1/chat/completions'}),/allowlisted/);
});
test('rejects remote plaintext requests even when allowlisted',async()=>{
 await assert.rejects(generateAiDraft({...base(),endpoint:'http://provider.example/v1/chat/completions',allowedHosts:['provider.example']}),/TLS/);
});
test('requires key for remote HTTPS providers',async()=>{
 await assert.rejects(generateAiDraft({...base(),endpoint:'https://provider.example/v1/chat/completions',allowedHosts:['provider.example']}),/API key/);
});
test('never exposes provider response body on errors',async()=>{
 await assert.rejects(generateAiDraft({...base(),fetchImpl:async()=>({ok:false,status:401})}),/HTTP 401/);
});
test('rejects malformed model output',async()=>{
 await assert.rejects(generateAiDraft({...base(),fetchImpl:async()=>({ok:true,status:200,json:async()=>({choices:[]})})}),/Invalid AI response/);
});
test('refuses oversized prompts and malformed endpoint paths',async()=>{
 await assert.rejects(generateAiDraft({...base(),messages:[{role:'user',content:'a'.repeat(8001)}]}),/oversized/);
 await assert.rejects(generateAiDraft({...base(),endpoint:'http://localhost:4020/internal/secrets'}),/chat-completions/);
});
