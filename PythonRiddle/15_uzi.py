import datetime

for yr in range(2006,1006,-10):
    if yr%4==0:
        if datetime.date(yr,1,1).weekday() == 3:
            print yr

# 27 - January - 1756 - Mozart's birthday
