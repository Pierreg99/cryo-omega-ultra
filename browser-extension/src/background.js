const api = globalThis.browser ?? globalThis.chrome;
api.runtime.onInstalled.addListener(() => {
  api.contextMenus.create({id:'cryo-download-link',title:'Download with Cryo',contexts:['link']});
  api.contextMenus.create({id:'cryo-copy-promote',title:'Copy Cryo promotion text',contexts:['page','link']});
});
api.contextMenus.onClicked.addListener(async(info,tab)=>{try{if(info.menuItemId==='cryo-download-link'&&info.linkUrl){await api.downloads.download({url:info.linkUrl,saveAs:true});return;}if(info.menuItemId==='cryo-copy-promote'){const url=info.linkUrl||info.pageUrl||tab?.url||'';const text=`Cryo Omega — ${tab?.title||'Check this out'}\n${url}`;await api.storage.local.set({lastPromotion:text});if(tab?.id!=null)await api.tabs.sendMessage(tab.id,{type:'COPY_TEXT',text}).catch(()=>{});}}catch(error){console.error('Cryo context action failed',error);}});
api.downloads.onCreated.addListener(async(item)=>{const state=await api.storage.local.get({queue:[]});const queue=Array.isArray(state.queue)?state.queue:[];queue.unshift({id:item.id,url:item.url,filename:item.filename||'',state:item.state});await api.storage.local.set({queue:queue.slice(0,100)});});
api.downloads.onChanged.addListener(async(delta)=>{const state=await api.storage.local.get({queue:[]});const queue=(state.queue||[]).map(entry=>{if(entry.id!==delta.id)return entry;if(delta.state)entry.state=delta.state.current;if(delta.filename)entry.filename=delta.filename.current;return entry;});await api.storage.local.set({queue});});
api.commands?.onCommand.addListener((command)=>{if(command==='open-manager')api.action.openPopup?.().catch?.(()=>{});});
