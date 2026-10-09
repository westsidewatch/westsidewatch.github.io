#!/usr/bin/env python3
"""A2A-compatible local Doré image job executor.
Run ON the Mac mini via existing A2A agent shell runner; no remote shell access implied.
Image backend is a configurable local command, never a paid API.
"""
import argparse,json,subprocess,shlex,sys,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def run(job_dir,backend_command,dry_run=False,font=None):
 job_dir=Path(job_dir).resolve()
 job=json.loads((job_dir/'job.json').read_text(encoding='utf-8'))
 if job.get('schema')!='dore.local-image-job.v0':raise ValueError('Unsupported job schema')
 portrait=job.get('constraints',{}).get('portraitSynthesis')
 if not isinstance(portrait,bool):raise ValueError('Invalid portrait mode')
 if portrait and not (job_dir/'editorial-quality.json').is_file():raise ValueError('Portrait mode requires editorial quality and reference contract')
 prompt=(job_dir/job['imagePromptFile']).resolve()
 output=(job_dir/job['expectedOutput']).resolve()
 if prompt.parent!=job_dir or output.parent!=job_dir:raise ValueError('Job path escape')
 if not prompt.exists():raise FileNotFoundError(prompt)
 command=shlex.split(backend_command)
 if not command:raise ValueError('Empty local image backend')
 # Only configured local executable. No shell=True and no automatic installation.
 argv=[part.replace('{prompt_file}',str(prompt)).replace('{output_file}',str(output)) for part in command]
 if not any('{prompt_file}' in part for part in command) or not any('{output_file}' in part for part in command):
  raise ValueError('Backend must accept {prompt_file} and {output_file} placeholders')
 if dry_run:
  print(json.dumps({'status':'READY_FOR_A2A','argv':argv,'job':str(job_dir)},ensure_ascii=False))
  return
 if output.exists():raise FileExistsError('Refusing to overwrite existing generated image: '+str(output))
 result=subprocess.run(argv,cwd=str(ROOT),capture_output=True,text=True,timeout=1800,check=False)
 if result.returncode:
  raise RuntimeError(f'Local backend failed ({result.returncode}): {result.stderr[-1600:]}')
 if not output.is_file() or output.stat().st_size==0:raise RuntimeError('Backend returned success without output PNG')
 composite=[sys.executable,str(ROOT/'scripts/composite_dore_speaker_cover.py'),'--job',str(job_dir)]
 if font:composite.extend(['--font',str(font)])
 result=subprocess.run(composite,cwd=str(ROOT),capture_output=True,text=True,timeout=120,check=False)
 if result.returncode:raise RuntimeError('Composite failed: '+result.stderr[-1600:]+result.stdout[-800:])
 print(json.dumps({'status':'LOCAL_RENDER_COMPLETE','background':str(output),'finalCover':str(job_dir/'final-cover.png'),'published':False},ensure_ascii=False))
def main():
 p=argparse.ArgumentParser()
 p.add_argument('--job',required=True)
 p.add_argument('--backend-command',default=os.environ.get('DORE_LOCAL_IMAGE_BACKEND',''))
 p.add_argument('--dry-run',action='store_true')
 p.add_argument('--font',help='Explicit font for compositor, including CI fixtures')
 a=p.parse_args()
 if not a.backend_command:raise SystemExit('Set DORE_LOCAL_IMAGE_BACKEND with {prompt_file} and {output_file} placeholders')
 run(a.job,a.backend_command,a.dry_run,a.font)
if __name__=='__main__':main()
