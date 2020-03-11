import matplotlib.pyplot as plt
import csv

with open("temperature_daily.csv") as rf:
    reader = csv.DictReader(rf)
    items = list(reader)
data={}
for item in items:
    temperature=[]
    #print(type(item['min_temperature']))
    temperature.append(int(item['min_temperature']))
    temperature.append(int(item['max_temperature']))
    data[item['date']]=temperature


plt.figure(num=1, figsize=(50, 20),)
plt.rcParams['savefig.dpi'] = 600 #图片像素
plt.rcParams['figure.dpi'] = 600 #分辨率



month=[' ','January','February','March','April','May','June','July','August','September','October','November','December',]
for i in range(0,13):
    for j in range(1996,2018):
        if i==0 and j!=1996:
            ax = plt.subplot2grid((13, 22), (0, j - 1996), colspan=1)
            plt.text(0.4,0, str(j), fontsize=30)
            plt.xlim(0, 2)
            plt.ylim(0, 2)
            ax.axis('off')
            continue
        if i!=0 and j==1996:
            ax = plt.subplot2grid((13, 22), (i, 0), colspan=1)
            plt.text(0, 0.9,month[i], fontsize=25)
            plt.xlim(0, 3)
            plt.ylim(0, 2)
            ax.axis('off')
            continue
        data_x=[]
        data_min=[]
        data_max=[]
        flag=False
        t_max=0
        t_min=99
        for k in range(1,32):
            year=str(j)+'-'+str(i).zfill(2)+'-'+str(k).zfill(2)
            if year in data.keys():
                flag=True
                data_x.append(k)
                data_min.append(data[year][0])
                data_max.append(data[year][1])
                t_min=min(data[year][0],t_min)
                t_max = max(data[year][1], t_max)

        ax = plt.subplot2grid((13, 22), (i , j - 1996), colspan=1)
        ax.set_facecolor('r')
        ax.plot(data_x, data_min,c='yellow')
        ax.plot(data_x, data_max,c='g')
        plt.xlim(-5,33)

        plt.fill_between([p for p in range(-5,34)],t_min ,t_max, color='b', alpha=(110-t_min)/200)
        ax.axis('off')

plt.savefig("heapmap.png")
plt.show()