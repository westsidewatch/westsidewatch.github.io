// One document-lifetime JSON authority. Revalidate HTTP cache on a fresh page;
// coalesce concurrent/sequential consumers and keep their mutations isolated.
const entries=new Map();
const base=new URL('.',import.meta.url);
export function invalidateCityData(path) {
  if(path===undefined)entries.clear();
  else entries.delete(new URL(path,base).href);
}
export async function loadCityData(path) {
  const url=new URL(path,base).href;
  let task=entries.get(url);
  if(!task) {
    task=(async()=>{
      const response=await fetch(url,{cache:'no-cache'});
      if(!response.ok)throw new Error(`City data unavailable (${response.status}): ${url}`);
      return response.json();
    })();
    entries.set(url,task);
    task.catch(()=>{if(entries.get(url)===task)entries.delete(url);});
  }
  return structuredClone(await task);
}
