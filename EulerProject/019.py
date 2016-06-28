import datetime as dt
initi=dt.date.toordinal(dt.datetime(1901,1,1,0,0))
final=dt.date.toordinal(dt.datetime(2000,12,31,0,0))
ct_sunday1st=0
for i in range(initi,final+1):
    if dt.date.fromordinal(i).weekday()==6 and dt.date.fromordinal(i).day==1:
        ct_sunday1st+=1
print ct_sunday1st
