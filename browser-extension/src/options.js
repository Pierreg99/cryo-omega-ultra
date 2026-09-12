const api=globalThis.browser??globalThis.chrome;
const $=(s)=>document.querySelector(s);
(async()=>{const {gatewayOrigin=''}=await api.storage.local.get({gatewayOrigin:''});$('#gateway').value=gatewayOrigin;})();
$('#save').addEventListener('click',async()=>{const value=$('#gateway').value.trim().replace(/\/$/,'');if(value&& !/^https?:\/\//i.test(value)){ $('#status').textContent='Gateway must use http:// or https://'; return;}await api.storage.local.set({gatewayOrigin:value});$('#status').textContent='Saved.';});
