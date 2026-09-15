/* DORÉ Design — grounded evidence prompt compiler v2.
   Concrete visual instructions come only from the exact selected historical image observation.
   Lineage grammar is context; manual fingerprints are not prompt authority. */
(function(){
  const DIMS=['layout','image','typography','material','density','sequence','irony','emergence'];
  function uniq(xs){return [...new Set(xs.filter(Boolean))]}
  function moduleOf(key){return key.split(':')[0].trim()}
  function compile({publication,eraLabel,base,selected,selectedEvidenceIds,observationDb}){
    const dims=uniq(selected.map(moduleOf).filter(x=>DIMS.includes(x)));
    const ids=uniq(selectedEvidenceIds||[]);
    const observations=ids.map(id=>(observationDb?.items||[]).find(x=>x.evidence?.id===id)).filter(Boolean);
    const lineage=base||`Preserve the supplied source image and subject identity. Work within the selected ${publication} / ${eraLabel} editorial lineage without copying logos or mastheads.`;
    if(!selected.length)return `${lineage}\n\nNo visual grammar selected yet.`;
    if(!ids.length)return `${lineage}\n\nNo exact historical evidence image selected. Prompt compilation is blocked rather than falling back to a lineage stereotype.`;
    if(!observations.length)return `${lineage}\n\nThe selected historical evidence has no grounded visual observation yet. Prompt compilation is blocked; inspect this exact image before generating concrete design instructions.`;
    let out=`${lineage}\n\nAUTHORITY ORDER — binding:\n1. The exact selected historical image is concrete visual authority.\n2. Grounded observations produced by inspecting that exact image supply composition, crop, typography, material, density and other visible relationships.\n3. Italian lineage / DESIGN DNA is context only and may not invent concrete visual content.\n4. Manually authored fingerprint prose is not prompt authority.\n\nDESIGN DNA — selected canonical grammar (context only):\n- ${selected.join('\n- ')}`;
    observations.forEach(obs=>{
      const ev=obs.evidence||{}, observer=obs.observer||{};
      out+=`\n\nEXACT HISTORICAL EVIDENCE\n- evidence: ${ev.id}\n- source: ${ev.sourceUri}\n- observer: ${observer.providerKind||'unknown'} / ${observer.providerId||'unknown'}\n- image inspected: ${obs.provenance?.imageInspected===true?'yes':'no'}`;
      out+=`\n\nGROUNDED 8D OBSERVATION — selected dimensions only:`;
      dims.forEach(dim=>{
        const item=obs.dimensions?.[dim];
        if(!item||item.status==='insufficient'){
          out+=`\n- ${dim}: insufficient visual evidence; do not invent this dimension.`;
        }else{
          out+=`\n- ${dim}:`;
          (item.facts||[]).forEach(f=>{out+=`\n  - ${f}`});
        }
      });
    });
    out+=`\n\nGROUNDING CONTRACT\n- Preserve the observed spatial relationships and hierarchy when transferring to the supplied subject.\n- Subject identity and copy may change only where the user requests it; their visual roles should follow the observed evidence.\n- Do not add architecture, furniture, grids, colors, motifs, image regions or materials merely because they are associated with ${publication}, Italian design or modernism.\n- If the selected image does not establish a dimension, leave it unconstrained rather than inventing evidence.\n\nFINAL FIDELITY RULE\nThe result should remain recognizably derived from the selected evidence image's design relationships even when subject or copy changes. Remove every concrete element whose only justification is a generic style association.\n\nVisual evidence authority: ${ids.join(', ')}. Generated images remain evaluation-only and are never historical authority.`;
    return out;
  }
  window.DoreItalianPromptCompiler={compile};
})();
