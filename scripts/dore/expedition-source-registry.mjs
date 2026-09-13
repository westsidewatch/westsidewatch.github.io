export const expeditionSources = [
  { id:'met', domain:'museum', mode:'bulk-csv', authority:'A', repo:'metmuseum/openaccess', asset:'MetObjects.csv', rights:'item-level/open-access' },
  { id:'cooper-hewitt', domain:'design', mode:'bulk-csv', authority:'A', repo:'cooperhewitt/collection', asset:'meta/objects.csv', rights:'item-level' },
  { id:'aic', domain:'museum', mode:'bulk-json', authority:'A', repo:'art-institute-of-chicago/api-data', asset:'json/artworks', rights:'item-level/is_public_domain' },
  { id:'smithsonian', domain:'museum-design', mode:'api-or-bulk', authority:'A', repo:'Smithsonian/OpenAccess', rights:'CC0/item-level' },
  { id:'rijksmuseum', domain:'museum', mode:'oai-api', authority:'A', rights:'item-level' },
  { id:'vam', domain:'museum-design', mode:'collections-api', authority:'A', rights:'item-level' },
  { id:'loc', domain:'editorial-photography-print', mode:'json-api', authority:'A', rights:'item-level' }
];

export const expeditionDomains = [
  'editorial','typography','painting','illustration','photography','film','architecture','interior','furniture','industrial-design','web','motion','historical-visual-systems','christian-screen','church-architecture'
];
