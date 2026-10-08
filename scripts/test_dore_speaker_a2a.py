#!/usr/bin/env python3
"""End-to-end A2A worker smoke test using a local PNG fixture backend.
Does NOT claim a real AI model was run.
"""
import os,sys,json,tempfile,subprocess,struct,zlib
from pathlib import Path
root=Path(__file__).resolve().parents[1]
def png(path,w=720,h=960):
 def chunk(tag,payload):
  import binascii
  return struct.pack('!I',len(payload))+tag+payload+struct.pack('!I',binascii.crc32(tag+payload)&0xffffffff)
 row=b'\x00'+bytes([255,255,255])*w
 data=b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('!2I5B',w,h,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(row*h))+chunk(b'IEND',b'')
 path.write_bytes(data)
def main():
 with tempfile.TemporaryDirectory() as d:
  base=Path(d)
  p=subprocess.run([sys.executable,str(root/'scripts/prepare_dore_local_image_job.py'),'--speaker','david-pawson','--out',str(base)],capture_output=True,text=True)
  assert p.returncode==0,p.stderr
  job=base/'david-pawson'
  backend=base/'mock_backend.py'
  backend.write_text('import sys\nfrom pathlib import Path\nimport struct,zlib,binascii\ndef c(t,p):return struct.pack("!I",len(p))+t+p+struct.pack("!I",binascii.crc32(t+p)&0xffffffff)\nw,h=720,960\nr=b"\\x00"+bytes([255,255,255])*w\nPath(sys.argv[2]).write_bytes(b"\\x89PNG\\r\\n\\x1a\\n"+c(b"IHDR",struct.pack("!2I5B",w,h,8,2,0,0,0))+c(b"IDAT",zlib.compress(r*h))+c(b"IEND",b""))\n')
  command=f'{sys.executable} {backend} {{prompt_file}} {{output_file}}'
  args=[sys.executable,str(root/'scripts/run_dore_speaker_a2a.py'),'--job',str(job),'--backend-command',command]
  dry=subprocess.run(args+['--dry-run'],capture_output=True,text=True)
  assert dry.returncode==0,dry.stderr
  assert json.loads(dry.stdout)['status']=='READY_FOR_A2A'
  try:import PIL
  except ImportError:
   print('PASS A2A job preparation and dry-run; Pillow unavailable for composite smoke test')
   return
  # Linux CI font is a fixture only; production uses the Mac Chinese font.
  fixture_font=Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
  if fixture_font.exists():args.extend(['--font',str(fixture_font)])
  done=subprocess.run(args,capture_output=True,text=True)
  assert done.returncode==0,done.stderr+done.stdout
  assert (job/'final-cover.png').is_file()
  assert json.loads(done.stdout)['status']=='LOCAL_RENDER_COMPLETE'
  print('PASS local A2A worker end-to-end with fixture backend (NOT an AI render)')
if __name__=='__main__':main()
