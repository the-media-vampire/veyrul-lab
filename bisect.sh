#!/usr/bin/env bash
# ComfyUI custom-node halving-search helper
# Procedure: Comfy-Org/docs troubleshooting/custom-node-issues.mdx commit 4a9f856b
# Source record: art_01M6JVW9DS5T7W9T9659ARG0S2 rev 2 (Veyrul)
# Requires: bash>=4, python3. Does NOT start/stop ComfyUI.
set -euo pipefail
STATE=.bisect_state.json
die(){ echo "ERROR: $*" >&2; exit 1; }
need_state(){ [[ -f $STATE ]] || die "No session. Run: bisect.sh start <nodes_dir> <staging_dir>"; }

start(){
  [[ $# -eq 2 ]] || die "Usage: bisect.sh start <nodes_dir> <staging_dir>"
  local nd=$1 st=$2
  [[ -d $nd ]] || die "Not found: $nd"
  [[ -f $STATE ]] && die "Session active. Run: bisect.sh reset first."
  mkdir -p "$st"
  local bk="${nd%/}_backup_$(date +%Y%m%dT%H%M%S).tar.gz"
  echo "Backup -> $bk"; tar -czf "$bk" -C "$(dirname "$nd")" "$(basename "$nd")"
  python3 - "$nd" "$st" "$bk" <<'PY'
import sys,json,os,shutil
nd,st,bk=sys.argv[1],sys.argv[2],sys.argv[3]
all_=sorted([d for d in os.listdir(nd) if os.path.isdir(os.path.join(nd,d))])
n=len(all_); assert n>=2,f"Need >=2 node dirs, found {n}"
half=n//2
for nm in all_[:half]: shutil.move(os.path.join(nd,nm),st)
json.dump({"nd":nd,"st":st,"bk":bk,"round":1,
  "staged":all_[:half],"history":[]},open('.bisect_state.json','w'),indent=2)
print(f"Round 1: moved {half}/{n} to staging. {n-half} active.")
print("Start ComfyUI normally, then: bisect.sh good | bad")
PY
}

good(){
  need_state
  python3 - <<'PY'
import json,os,shutil
s=json.load(open('.bisect_state.json'))
staged=s['staged']
if len(staged)==1:
  print(f"Suspect: {staged[0]}. Run reset to restore all.")
elif len(staged)==0:
  print("No staged nodes; session may be complete. Run reset.")
else:
  half=len(staged)//2; restore=staged[:half]
  for nm in restore: shutil.move(os.path.join(s['st'],nm),s['nd'])
  s['staged']=staged[half:]; s['history'].append({'r':s['round'],'result':'good','restored':restore})
  s['round']+=1
  json.dump(s,open('.bisect_state.json','w'),indent=2)
  print(f"Restored {len(restore)}. {len(s['staged'])} still staged. Restart ComfyUI and test.")
PY
}

bad(){
  need_state
  python3 - <<'PY'
import json,os,shutil
s=json.load(open('.bisect_state.json'))
active=sorted([d for d in os.listdir(s['nd']) if os.path.isdir(os.path.join(s['nd'],d))])
if len(active)==1:
  print(f"Suspect: {active[0]}. Run reset to restore all.")
elif len(active)==0:
  print("No active nodes remain. Run reset.")
else:
  half=len(active)//2; move=active[:half]
  for nm in move: shutil.move(os.path.join(s['nd'],nm),s['st'])
  s['staged']=s.get('staged',[])+move
  s['history'].append({'r':s['round'],'result':'bad','moved':move})
  s['round']+=1
  json.dump(s,open('.bisect_state.json','w'),indent=2)
  print(f"Moved {half} to staging. {len(active)-half} active. Restart ComfyUI and test.")
PY
}

reset_(){
  need_state
  python3 - <<'PY'
import json,os,shutil
s=json.load(open('.bisect_state.json'))
for nm in s.get('staged',[]):
  src=os.path.join(s['st'],nm)
  if os.path.exists(src): shutil.move(src,s['nd']); print(f"  restored {nm}")
os.remove('.bisect_state.json'); print("Session cleared.")
PY
}

status_(){
  need_state
  python3 - <<'PY'
import json
s=json.load(open('.bisect_state.json'))
print(f"Round {s['round']} | staged: {len(s.get('staged',[]))}")
for h in s.get('history',[]): print(f"  r{h['r']}: {h['result']}")
PY
}

case "${1:-}" in
  start)  shift; start "$@";;
  good)   good;;
  bad)    bad;;
  reset)  reset_;;
  status) status_;;
  *) echo "Usage: bisect.sh {start <nodes_dir> <staging_dir>|good|bad|reset|status}"; exit 1;;
esac