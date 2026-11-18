#!/bin/bash
cd "C:\Users\Mavis\.zcode\workspace\draft-c487a057-1004-49d8-94d6-d0be05ad5252\jewelry-platform" || exit 1
export PATH="$PATH:/d/Git/cmd"
for i in $(seq 1 40); do
  echo "===== ATTEMPT $i ====="
  if git push -u origin main; then
    echo "PUSH_SUCCESS"
    exit 0
  fi
  echo "attempt $i failed, sleeping 20s..."
  sleep 20
done
echo "PUSH_FAILED_ALL_ATTEMPTS"
exit 1
