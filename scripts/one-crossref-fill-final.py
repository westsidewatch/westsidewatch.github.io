from pathlib import Path
import json,re,zipfile,io,os
summary=json.loads(Path('audit-output/one-crossref-summary.json').read_text(encoding='utf-8'))
conflict_refs=['創世記 1:26–28','創世記 12:3','詩篇 110:4','創世記 12:1–4','啟示錄 5:5','路加福音 1:46–55','希伯來書 12:28–29','申命記 17:14–20','以賽亞書 40:31','彌迦書 6:6–8','羅馬書 12:19','詩篇 2:6','路加福音 1:32–33','民數記 24:17','撒母耳記下 7:12–16','民數記 6:24–26','羅馬書 3:13','路加福音 1:51–53','雅各書 3:5–10','羅馬書 3:10–12','提摩太後書 3:15–17','以西結書 34:11–16','約翰福音 10:11','約翰福音 8:12','創世記 1章','出埃及記 14章','以賽亞書 5:1–7','以賽亞書 44:9–20','以賽亞書 55:1','以賽亞書 25:8','以賽亞書 61:1','以賽亞書 42:1','耶利米書 31:31–34','以賽亞書 40:3–5','詩篇 2:7','以賽亞書 22:22','但以理書 7:13–14','創世記 3:15','出埃及記 24:8','詩篇 110:1','申命記 6:5']
refs=sorted(set(summary['uniqueReferences'])|set(conflict_refs))
archive=Path(os.environ.get('CUVT_USFM_ZIP','/tmp/cmn-cu89t_usfm.zip'))
if not archive.is_file(): raise SystemExit(f'CUV archive missing: {archive}')
z=zipfile.ZipFile(io.BytesIO(archive.read_bytes()));book_files={}
for name in z.namelist():
    if not name.lower().endswith(('.usfm','.sfm')): continue
    text=z.read(name).decode('utf-8-sig',errors='replace');m=re.search(r'^\\id\s+([1-3]?[A-Z]{2,3})\b',text,re.M)
    if m: book_files[m.group(1)]=text
name_to_code={'創世記':'GEN','出埃及記':'EXO','利未記':'LEV','民數記':'NUM','申命記':'DEU','約書亞記':'JOS','撒母耳記下':'2SA','列王紀上':'1KI','列王紀下':'2KI','歷代志上':'1CH','歷代志下':'2CH','詩篇':'PSA','箴言':'PRO','以賽亞書':'ISA','耶利米書':'JER','耶利米哀歌':'LAM','以西結書':'EZK','但以理書':'DAN','彌迦書':'MIC','哈該書':'HAG','馬太福音':'MAT','路加福音':'LUK','約翰福音':'JHN','羅馬書':'ROM','哥林多後書':'2CO','以弗所書':'EPH','歌羅西書':'COL','提摩太後書':'2TI','希伯來書':'HEB','雅各書':'JAS','啟示錄':'REV'}
def clean(s):
    s=re.sub(r'\\f\s.*?\\f\*','',s);s=re.sub(r'\\x\s.*?\\x\*','',s)
    s=re.sub(r'\\w\s+([^|\\]+)(?:\|[^\\]*)?\\w\*',r'\1',s)
    s=re.sub(r'\\(?:add|nd|pn|qt|k|em|bd|it)\s*','',s);s=re.sub(r'\\(?:add|nd|pn|qt|k|em|bd|it)\*','',s)
    s=re.sub(r'\\[A-Za-z0-9+_-]+\*?\s*','',s)
    return re.sub(r'\s+',' ',s).strip()
parsed={}
for code,text in book_files.items():
    chapters={};ch=None;current_keys=[]
    for raw in text.splitlines():
        if raw.startswith('\\c '):
            try: ch=int(raw.split()[1]);chapters.setdefault(ch,{})
            except: pass
            current_keys=[];continue
        if raw.startswith('\\v ') and ch is not None:
            m=re.match(r'\\v\s+(\d+)(?:-(\d+))?\s*(.*)',raw)
            if m:
                a=int(m.group(1));b=int(m.group(2) or a);record=[a,b,clean(m.group(3))];current_keys=list(range(a,b+1))
                for v in current_keys: chapters[ch][v]=record
            continue
        if current_keys and ch is not None and raw and not raw.startswith('\\c '):
            extra=clean(raw)
            if extra:
                record=chapters[ch][current_keys[0]];record[2]=(record[2]+' '+extra).strip()
    parsed[code]=chapters
def passage(ref):
    book,loc=ref.rsplit(' ',1);code=name_to_code.get(book);loc=loc.replace('章','')
    if not code or code not in parsed: raise KeyError(f'book unavailable: {ref}; code={code}; found={sorted(book_files)}')
    chapters=parsed[code];pieces=[];seen=set()
    def add_record(ch,v):
        rec=chapters.get(ch,{}).get(v)
        if not rec: raise KeyError(f'missing verse {ref} -> {ch}:{v}')
        key=(ch,rec[0],rec[1])
        if key not in seen:
            if not rec[2]: raise KeyError(f'empty verse {ref} -> {ch}:{v}')
            seen.add(key);pieces.append(rec[2])
    if ':' in loc:
        cpart,vpart=loc.split(':',1);ch=int(cpart)
        if ',' in vpart: verses=[int(v) for v in vpart.split(',')]
        elif '–' in vpart:
            a,b=map(int,vpart.split('–',1));verses=list(range(a,b+1))
        else: verses=[int(vpart)]
        for v in verses: add_record(ch,v)
    else:
        if '–' in loc: a,b=map(int,loc.split('–',1));chs=range(a,b+1)
        else: chs=[int(loc)]
        for ch in chs:
            if ch not in chapters: raise KeyError(f'missing chapter {ref} -> {ch}')
            for v in sorted(chapters[ch]): add_record(ch,v)
    return ''.join(pieces)
scripture={ref:passage(ref) for ref in refs}
js='''/* ONE complete reviewed cross-reference Scripture canonicalization layer.\n * Source: Chinese Union Version, New Punctuation (Traditional), Public Domain via eBible.\n * Exact reference match only; never promotes explanation text into Scripture.\n */\n(()=>{\n  "use strict";const D=window.ONE_DATA;if(!D?.studyBooks)return;const scriptureByReference='''+json.dumps(scripture,ensure_ascii=False,separators=(',',':'))+''';let applied=0;\n  for(const book of Object.values(D.studyBooks))for(const study of Object.values(book?.chapterStudies||{}))for(const row of (Array.isArray(study?.connections)?study.connections:[])){if(!Array.isArray(row))continue;const scripture=scriptureByReference[String(row[0]||'').trim()];if(scripture){row[3]=scripture;applied++;}}\n  window.ONE_CROSS_REFERENCE_COMPLETE_FILL={applied,references:Object.keys(scriptureByReference).length};\n})();\n'''
Path('static/one/one-cross-reference-scripture-complete.js').write_text(js,encoding='utf-8')
audit='''/* Read-only cross-reference integrity audit. Never renders UI. */\n(()=>{\n  "use strict";const D=window.ONE_DATA;if(!D?.studyBooks)return;const missingRows=[],explanationCopied=[],relationshipCopied=[],conflicts=[];const byRef=new Map();let total=0,verified=0;\n  for(const [bookNo,book] of Object.entries(D.studyBooks))for(const [chapterNo,study] of Object.entries(book?.chapterStudies||{}))for(const [index,row] of (Array.isArray(study?.connections)?study.connections:[]).entries()){if(!Array.isArray(row))continue;total++;const reference=String(row[0]||'').trim(),relationship=String(row[1]||'').trim(),explanation=String(row[2]||'').trim(),scripture=String(row[3]||'').trim();const meta={book:Number(bookNo),name:book.name,chapter:Number(chapterNo),index,reference};if(!scripture){missingRows.push(meta);continue;}verified++;if(explanation&&scripture===explanation)explanationCopied.push(meta);if(relationship&&scripture===relationship)relationshipCopied.push(meta);if(reference){const prior=byRef.get(reference);if(prior&&prior.scripture!==scripture)conflicts.push({reference,first:prior.meta,second:meta});else if(!prior)byRef.set(reference,{scripture,meta});}}\n  const ok=!missingRows.length&&!explanationCopied.length&&!relationshipCopied.length&&!conflicts.length;window.ONE_CROSS_REFERENCE_GLOBAL_AUDIT={ok,total,verified,missingRows,explanationCopied,relationshipCopied,conflicts};document.documentElement.dataset.oneCrossReferenceAudit=ok?'PASS':`FAIL:${missingRows.length}`;\n})();\n'''
Path('static/one/one-cross-reference-scripture-global-audit.js').write_text(audit,encoding='utf-8')
p=Path('static/one/index.html');s=p.read_text(encoding='utf-8');s=s.replace('<script src="./one-cross-reference-scripture-hebrews.js?v=20260821a"></script>','<script src="./one-cross-reference-scripture-complete.js?v=20260821a"></script>');p.write_text(s,encoding='utf-8')
pre=Path('scripts/one-crossref-preflight.sh');s=pre.read_text(encoding='utf-8');s=s.replace('HEBREWS="static/one/one-cross-reference-scripture-hebrews.js"','COMPLETE="static/one/one-cross-reference-scripture-complete.js"');s=s.replace('"$AUDIT" "$HEBREWS" "$MAJOR" "$WISDOM" "$CANONICAL"','"$AUDIT" "$COMPLETE" "$MAJOR" "$WISDOM" "$CANONICAL"');s=s.replace(" 'one-cross-reference-scripture-hebrews.js',"," 'one-cross-reference-scripture-complete.js',");s=s.replace('"$WISDOM" "$MAJOR" "$HEBREWS"','"$WISDOM" "$MAJOR" "$COMPLETE"');pre.write_text(s,encoding='utf-8')
print(json.dumps({'canonicalizedReferences':len(scripture),'booksFound':len(book_files)},ensure_ascii=False))
