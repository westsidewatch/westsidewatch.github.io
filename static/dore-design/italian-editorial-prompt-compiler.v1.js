/* DORÉ Design — evidence-aware prompt compiler v1.
   Historical evidence remains authority. Generated prompts are compiler output. */
(function(){
  function uniq(xs){return [...new Set(xs.filter(Boolean))]}
  function moduleOf(key){return key.split(':')[0].trim()}
  function tokenOf(key){return key.slice(key.indexOf(':')+1).trim()}
  function compile({publication,eraLabel,base,selected,evidenceItems,fingerprintDb}){
    const ids=uniq(selected.flatMap(key=>{
      const token=tokenOf(key);
      return evidenceItems.filter(x=>(x.tokens||[]).includes(token)&&x.image).map(x=>x.id);
    }));
    const fps=ids.map(id=>(fingerprintDb.items||[]).find(x=>x.evidenceId===id)).filter(Boolean);
    const selectedModules=uniq(selected.map(moduleOf));
    const constraints=[];
    selectedModules.forEach(module=>fps.forEach(fp=>(fp.dimensions?.[module]||[]).forEach(rule=>constraints.push(`${module}: ${rule}`))));
    const transferable=uniq(fps.flatMap(fp=>fp.transferable||[]));
    const forbidden=uniq(fps.flatMap(fp=>fp.forbidden||[]));
    const unsupported=uniq(fps.flatMap(fp=>fp.unsupportedInvention||[]));
    const fidelity=uniq(fps.map(fp=>fp.fidelityQuestion));
    const lineage=base||`Preserve the supplied source subject while working inside the selected ${publication} / ${eraLabel} editorial lineage. Do not copy logos or mastheads.`;
    if(!selected.length)return `${lineage}\n\nNo visual grammar selected yet.`;
    let out=`${lineage}\n\nAUTHORITY ORDER — binding:\n1. The selected historical evidence controls concrete visual content, geometry, material, crop and spatial relationships.\n2. The selected evidence fingerprint controls how those observed relationships transfer to the new subject.\n3. Italian lineage / DESIGN DNA may guide design judgement, restraint and editorial intelligence only. It must not invent concrete materials, architecture, furniture, image regions, grids, colors or motifs that are absent from the selected evidence.\n\nDESIGN DNA — selected canonical grammar:\n- ${selected.join('\n- ')}`;
    if(constraints.length){out+=`\n\nEVIDENCE FINGERPRINT — binding visual relationships from the selected historical specimen:\n- ${uniq(constraints).join('\n- ')}`}
    if(transferable.length){out+=`\n\nTRANSFERABLE — these may change while keeping the same visual role:\n- ${transferable.join('\n- ')}`}
    if(forbidden.length){out+=`\n\nFORBIDDEN INVENTION — do not add structures absent from the selected evidence:\n- ${forbidden.join('\n- ')}`}
    if(unsupported.length){out+=`\n\nDNA LEAKAGE GATE — unsupported concrete invention is forbidden:\n- ${unsupported.join('\n- ')}`}
    if(fidelity.length){out+=`\n\nFIDELITY CHECK:\n- ${fidelity.join('\n- ')}`}
    out+=`\n\nBefore finalizing, remove every concrete visual element that came only from a stereotype of ${publication} / Italian design rather than from the selected evidence or the supplied source subject.\n\nVisual evidence authority: ${ids.join(', ')||'none selected'}. Historical evidence controls visual identity; lineage grammar controls design DNA. Generated images remain evaluation-only and are never historical authority.`;
    return out;
  }
  window.DoreItalianPromptCompiler={compile};
})();
