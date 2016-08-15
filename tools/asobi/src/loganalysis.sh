#!/bin/bash

LOG="access_log"

cat $LOG | awk -v FS='"' '{
  if($2 ~ /\.html|\.js|\.css|\.gif|\.jpg|\.ico/){
    cmd = "echo "$0" >> /tmp/loganalysis_static";
    system(cmd);
  } else{
    cmd = "echo "$0" >> /tmp/loganalysis_dynamic";
    system(cmd);
  }
}'

function count_by_hour(){
  ifile="/tmp/loganalysis_"$1
  cat $ifile | awk '
    BEGIN{i=0; while(i<24){cnt[i] = 0; i++;}}
    {
      i=0; while(i<24){
        re = sprintf("20/Jan/2010:%02d:[0-5][0-9]", i);
        if($0 ~ re){
          cnt[i] = cnt[i] + 1;
          break;
        }
      }
    }
    END{str=cnt[0]; i=1; while(i<24){str = str" "cnt[i]; i++} print str;}
  '
}

cnt_static=`count_by_hour "static"`
cnt_dynamic=`count_by_hour "dynamic"`
cnt_merge=$cnt_static" "$cnt_dynamic
echo -e "Hour\tStatic\tDynamic\tTotal"
echo $cnt_merge | awk '
BEGIN{maxidx=0; max=-1;}
{
  i = 0;
  while(i < 24){
    af = i + 1;
    bf = af + 24;
    a = $af;
    b = $bf;
    tot = a + b;
    if(tot > max){
      maxidx = i;
      max = tot;
    }
    printf("%d\t%d\t%d\t%d\n", i, a, b, tot);
    i++;
  }
}
END{print "\nMax:", max, "visits in hour", maxidx}
'
echo

echo "Most visited pages (top 10):"
cat $LOG | awk -v FS='"' '{print $2}' | sed 's/[A-Z]\+ \(.*\) HTT.*/\1/' |\
sort | uniq -c | sort -nr | head -10
echo

echo "Most active clients (top 10):"
cat $LOG | awk '{print $3}' | sort | uniq -c | sort -nr | head -10
echo

echo "Most common browsers (top 10):"
cat $LOG | awk -v FS='"' '{print $6}' | sort | uniq -c | sort -nr | head -10
echo

echo "Response codes distribution:"
cat $LOG | awk -v FS='"' '{print $3}' | awk '{print $1}' | sort | uniq -c | \
sort -nr
echo
