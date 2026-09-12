import { cp, mkdir, rm } from 'node:fs/promises';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
const exec=promisify(execFile);
const root=new URL('../',import.meta.url).pathname;
const dist=`${root}dist`;
await rm(dist,{recursive:true,force:true});
await mkdir(dist,{recursive:true});
await exec('python3',[`${root}scripts/render-icons.py`]);
const targets=['chrome','brave','edge','opera','firefox'];
for(const target of targets){const out=`${dist}/${target}`;await mkdir(out,{recursive:true});const manifest=target==='firefox'?'manifest.firefox.json':'manifest.json';await cp(`${root}${manifest}`,`${out}/manifest.json`);for(const dir of ['src','assets'])await cp(`${root}${dir}`,`${out}/${dir}`,{recursive:true});await cp(`${root}README.md`,`${out}/README.md`);await exec('zip',['-qr',`${dist}/cryo-omega-${target}.zip`,'.'],{cwd:out});}
await exec('zip',['-qr',`${dist}/cryo-omega-firefox.xpi`,'.'],{cwd:`${dist}/firefox`});
console.log(`Built ${targets.length} browser ZIP packages plus Firefox XPI in ${dist}`);
