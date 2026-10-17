#!/usr/bin/env python3
import argparse,json,sys
from pathlib import Path
O={"FALSIFIED":0,"OPEN":1,"PREDICTED":2,"VERIFIED":3,"FORMALIZED":4,"PROVEN":5}
R={"id","claim","type","deps","proof","code","dataset","hash","result","status"}
def bad(x): print('ERROR:',x,file=sys.stderr);raise SystemExit(1)
def main():
 a=argparse.ArgumentParser();a.add_argument('ledger',nargs='?',default='ledger/omega.json');p=a.parse_args();d=json.loads(Path(p.ledger).read_text(encoding='utf8'))
 if d.get('ledger')!='QCAL Ω Audit Ledger' or d.get('version')!='1.0.1':bad('invalid header')
 es=d.get('entries',[]);by={}
 for e in es:
  if R-set(e):bad(f"{e.get('id')}: missing fields")
  if e['id'] in by:bad('duplicate '+e['id'])
  if e['status'] not in O:bad('invalid status '+e['status'])
  by[e['id']]=e
 for e in es:
  for dep in e['deps']:
   if dep.startswith('AXIOM_'):continue
   if dep not in by:bad(f"{e['id']}: unknown dependency {dep}")
   if O[e['status']]>O[by[dep]['status']]:bad(f"{e['id']}: inheritance violation via {dep}")
 print('QCAL Ω Audit Ledger: PASS')
 print(json.dumps({'entries':len(es),'counts':{s:sum(x['status']==s for x in es) for s in O}},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
