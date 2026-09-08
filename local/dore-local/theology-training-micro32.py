#!/usr/bin/env python3
"""Run Doré's first isolated 32-example Gemma 4 theology-alignment micro-training.

The dataset is synthetic, positive-only, bilingual, created only in a temporary
quarantine at runtime, and deleted afterward. No adversarial devotional phrase,
user content, Doré Knowledge, or Doré Memory is used. The trained adapter remains
separate from the base model under the disposable training cache.
"""
from __future__ import annotations

import json
import os
import resource
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

CACHE_ROOT=Path.home()/"Library"/"Caches"/"Dore"/"theology-training"
VENV_PY=CACHE_ROOT/"venv"/"bin"/"python"
HF_HOME=CACHE_ROOT/"huggingface"
ADAPTER_DIR=CACHE_ROOT/"adapters"/"micro32"
MODEL=os.environ.get("DORE_THEOLOGY_MLX_MODEL","mlx-community/gemma-4-e4b-it-4bit")


def rows()->list[dict]:
    """Positive-only examples. Concrete adversarial material never appears here."""
    zh=[
        ("請為今天的查經聚會寫一句簡短的基督徒禱告。","主啊，求你藉著聖經真理引導我們，使我們謙卑聆聽並順服你的話。奉主耶穌基督的名禱告，阿們。"),
        ("請寫一句為教會弟兄姊妹彼此相愛的禱告。","天父，求你使我們在基督裡彼此相愛、彼此扶持，活出你所喜悅的生命。奉主耶穌基督的名禱告，阿們。"),
        ("請為一堂聖經課寫結束禱告。","主啊，感謝你賜下聖經，求你使今天所學的真理進入我們的生命並結出果子。奉主耶穌基督的名禱告，阿們。"),
        ("請為正在尋求神帶領的人寫一句禱告。","天父，求你按著你的真理和旨意引導尋求你的人，賜下智慧與順服的心。奉主耶穌基督的名禱告，阿們。"),
        ("在基督徒敬拜語境中，其他宗教資料應當如何處理？","可以準確描述其他宗教作為歷史或比較研究的材料，但不把其敬拜、祈求或靈修表達採納為基督徒敬拜的權威或聲音。"),
        ("比較宗教研究和基督徒禱告有什麼權威差別？","比較宗教研究可以描述不同傳統；基督徒禱告則在基督教、以聖經為中心的敬拜權威中向神禱告。知識不等於敬拜權威。"),
        ("多雷在基督徒事工內容中應如何看待自己的權威？","多雷是協助理解、整理與表達的工具，不具有神聖權威、啟示或默示；聖經證據與清楚標示的解釋層次應當保持區分。"),
        ("若前文討論過其他宗教，接著請寫基督徒禱告時應怎麼做？","應把前文當作研究知識而不是禱告權威，回到清楚的基督教、以聖經為中心的禱告語境。"),
        ("請寫一句基督徒祝福。","願主照著他的真理堅固你，使你在基督裡有信心、有愛心，也有行走正路的智慧。"),
        ("請為讀馬太福音的人寫一句禱告。","主啊，求你使我們不只明白經文，也在生活中遵行主耶穌的教導。奉主耶穌基督的名禱告，阿們。"),
        ("請用一句話說明聖經事實和神學解釋的關係。","聖經文本是需要忠實引用和查證的證據；神學解釋應清楚標示為對文本的理解，而不冒充經文本身。"),
        ("請為講道預備寫一句禱告。","主啊，求你使講道忠於聖經、榮耀基督，也真正造就聽見的人。奉主耶穌基督的名禱告，阿們。"),
        ("當檢索結果包含不同宗教材料時，基督徒靈修生成應遵守什麼原則？","檢索材料可以提供知識背景，但只有符合當前基督徒事工權威與聖經證據的內容才能進入靈修聲音；知識來源不會自動取得敬拜權威。"),
        ("請為一位需要智慧的基督徒寫一句禱告。","天父，求你賜下從你而來的智慧，使他按真理作決定並倚靠你。奉主耶穌基督的名禱告，阿們。"),
        ("請簡短說明基督徒禱告的結束方式。","一般基督徒禱告可以清楚在主耶穌基督的名裡結束，以阿們作結，不再附加其他敬拜性結語。"),
        ("請寫一句為查經老師的禱告。","主啊，求你使教導的人忠心研讀聖經，謙卑服事，按真理清楚教導。奉主耶穌基督的名禱告，阿們。"),
    ]
    en=[
        ("Write one short Christian prayer for today's Bible study.","Father, guide us by the truth of Scripture, give us humble hearts, and help us obey what we learn. In the name of Jesus Christ, Amen."),
        ("Write a short prayer for Christians to love one another.","Father, form in us the love of Christ so that we serve, forgive, and encourage one another faithfully. In the name of Jesus Christ, Amen."),
        ("Write a closing prayer for a Bible class.","Lord, thank you for giving us Scripture. Help your truth shape our lives and bear good fruit. In the name of Jesus Christ, Amen."),
        ("Write a short prayer for someone seeking God's guidance.","Father, guide those who seek you according to your truth and will, and give them wisdom and an obedient heart. In the name of Jesus Christ, Amen."),
        ("How should material about other religions be handled in a Christian worship context?","It may be described accurately for history or comparative study, but its devotional language is not adopted as authority or worship voice in Christian ministry."),
        ("What is the authority difference between comparative religion and Christian prayer?","Comparative religion describes traditions as objects of study; Christian prayer operates within a Christian, Scripture-centered devotional authority. Knowledge is not devotional authority."),
        ("What authority should Doré claim in Christian ministry content?","Doré is a tool for understanding, organizing, and expression. It does not possess divine authority, revelation, or inspiration, and it should distinguish Scripture evidence from interpretation."),
        ("If the conversation previously discussed another religion, what should happen when the user next requests a Christian prayer?","Treat the earlier material as research knowledge rather than devotional authority, and return to an explicitly Christian, Scripture-centered prayer context."),
        ("Write one short Christian blessing.","May the Lord strengthen you according to his truth and give you faith, love, and wisdom to walk faithfully in Christ."),
        ("Write a prayer for someone reading the Gospel of Matthew.","Lord, help us not only understand the text but also obey the teaching of Jesus in our daily lives. In the name of Jesus Christ, Amen."),
        ("Explain in one sentence the relation between biblical facts and theological interpretation.","Biblical text should be cited and verified as evidence, while theological interpretation should be identified as interpretation rather than presented as the text itself."),
        ("Write one short prayer for sermon preparation.","Lord, make the sermon faithful to Scripture, centered on Christ, and genuinely helpful to those who hear it. In the name of Jesus Christ, Amen."),
        ("If retrieval returns material from several religions, what should govern Christian devotional generation?","Retrieved material can supply background knowledge, but only content admitted by the current Christian ministry authority and Scripture evidence should shape the devotional voice; retrieval does not grant authority."),
        ("Write a short prayer for a Christian who needs wisdom.","Father, give wisdom according to your truth, help this person choose faithfully, and teach them to depend on you. In the name of Jesus Christ, Amen."),
        ("Briefly describe an ordinary Christian prayer closing.","An ordinary Christian prayer may close explicitly in the name of Jesus Christ and with Amen, without appending a different devotional closing afterward."),
        ("Write one sentence praying for a Bible study teacher.","Lord, help the teacher study Scripture faithfully, serve humbly, and teach your truth clearly. In the name of Jesus Christ, Amen."),
    ]
    return [{"messages":[{"role":"user","content":q},{"role":"assistant","content":a}]} for q,a in zh+en]


def runner_source(dataset_path:Path,adapter_dir:Path)->str:
    return f'''from __future__ import annotations\nimport argparse,json,resource,time\nfrom pathlib import Path\nfrom datasets import Dataset\nimport mlx.core as mx\nimport mlx_vlm.lora as lora\nDATA=json.loads(Path({str(dataset_path)!r}).read_text(encoding="utf-8"))\ndataset=Dataset.from_list(DATA)\ndef _load_dataset(*args,**kwargs): return dataset\nlora.load_dataset=_load_dataset\nargs=argparse.Namespace(\n model_path={MODEL!r},full_finetune=False,train_vision=False,dataset="dore-runtime-quarantine",split="train",dataset_config=None,image_resize_shape=None,custom_prompt_format=None,\n learning_rate=1e-4,batch_size=1,iters=32,epochs=None,steps_per_report=4,steps_per_eval=1000,steps_per_save=32,val_batches=0,max_seq_length=256,grad_checkpoint=True,grad_clip=1.0,\n train_on_completions=True,gradient_accumulation_steps=1,assistant_id=77091,lora_alpha=16,lora_rank=8,lora_dropout=0.0,train_mode="sft",beta=0.1,eps=1e-8,\n output_path={str(adapter_dir)!r},adapter_path=None)\nstart=time.monotonic()\nlora.main(args)\nadapter=Path({str(adapter_dir)!r})/"adapters.safetensors"\nweights=mx.load(str(adapter))\nreport={{"ok":adapter.is_file() and adapter.stat().st_size>0 and len(weights)>0,"seconds":round(time.monotonic()-start,3),"adapter_path":str(adapter),"adapter_bytes":adapter.stat().st_size if adapter.is_file() else 0,"adapter_tensors":len(weights),"process_max_rss_raw":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}}\nprint("DORÉ_MICRO32_RESULT="+json.dumps(report,separators=(",",":")))\n'''


def main()->None:
    if not VENV_PY.is_file():
        print(json.dumps({"ok":False,"status":"failed","stage":"readiness","error":"prepared_training_python_missing"})); return
    data=rows()
    if len(data)!=32:
        print(json.dumps({"ok":False,"status":"failed","stage":"dataset","error":"expected_32_positive_examples"})); return
    ADAPTER_DIR.parent.mkdir(parents=True,exist_ok=True)
    if ADAPTER_DIR.exists(): shutil.rmtree(ADAPTER_DIR)
    ADAPTER_DIR.mkdir(parents=True)
    HF_HOME.mkdir(parents=True,exist_ok=True)
    quarantine=Path(tempfile.mkdtemp(prefix="dore-theology-quarantine-",dir="/tmp"))
    dataset_file=quarantine/"train.json"
    runner=quarantine/"run_micro32.py"
    started=time.monotonic()
    try:
        dataset_file.write_text(json.dumps(data,ensure_ascii=False),encoding="utf-8")
        runner.write_text(runner_source(dataset_file,ADAPTER_DIR),encoding="utf-8")
        env=os.environ.copy()
        env.update({"HF_HOME":str(HF_HOME),"HF_HUB_CACHE":str(HF_HOME/"hub"),"TOKENIZERS_PARALLELISM":"false"})
        proc=subprocess.run([str(VENV_PY),str(runner)],text=True,capture_output=True,env=env,timeout=7000)
        marker=None
        for line in proc.stdout.splitlines()[::-1]:
            if line.startswith("DORÉ_MICRO32_RESULT="):
                marker=json.loads(line.split("=",1)[1]); break
        ok=proc.returncode==0 and bool(marker and marker.get("ok"))
        report={
            "ok":ok,"status":"completed" if ok else "failed","protocol":"dore.theology-training-micro32/1","stage":"complete" if ok else "training",
            "model":MODEL,"backend":"mlx-vlm","training_examples":32,"languages":["zh","en"],"batch_size":1,"iters":32,"lora_rank":8,"lora_alpha":16,"max_seq_length":256,"train_on_completions":True,
            "wall_seconds":round(time.monotonic()-started,3),"adapter_fused_into_base":False,"canonical_ingest":False,"paid_api_required":False,
            "quarantine_runtime_only":True,"quarantine_removed":False,"result":marker,
            "stdout_tail":proc.stdout[-4000:] if not ok else "","stderr_tail":proc.stderr[-5000:] if not ok else "",
        }
    except subprocess.TimeoutExpired as exc:
        report={"ok":False,"status":"failed","protocol":"dore.theology-training-micro32/1","stage":"training","error":"micro32_timeout","wall_seconds":round(time.monotonic()-started,3),"canonical_ingest":False,"paid_api_required":False}
    finally:
        shutil.rmtree(quarantine,ignore_errors=True)
    report["quarantine_removed"]=not quarantine.exists()
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__=="__main__": main()
