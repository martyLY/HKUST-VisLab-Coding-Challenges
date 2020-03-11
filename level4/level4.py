# -*- coding: utf-8 -*-
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
#import seaborn as sns
import csv
import json
import random
import operator

#sns.set(color_codes=True)

class track(object):
    def __init__(self,position,title,name,stream,url,data,region):
        self.position=position
        self.title=title
        self.name=name
        self.stream=int(stream)
        self.url=url
        self.data=data
        self.region=region

def read_cvs():
    f = csv.reader(open('data.csv', 'r'))
    data=[]
    for i in f:
        if i[5].split('-')[0] == '2017':
            data.append(track(i[0],i[1],i[2],i[3],i[4],i[5],i[6]))
    print('##finish load cvs')
    return data

def read_json():
    with open('countries.json', 'r', encoding='utf-8') as f:
        d_list = json.load(f)
        country_dic = {}
        for key, value in d_list.items():
            country_dic[key]=value['continent']
    print('##finish load json')
    return country_dic


def randomcolor():
    colorArr = ['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
    color = ""
    for i in range(6):
        color += colorArr[random.randint(0,14)]
    return "#"+color


def find_top_track_stream(data):
    tracks = {}
    for i in data:
        if i.title in tracks.keys():
            tracks[i.title] += 1
        else:
            tracks[i.title] = 1
    sorted(tracks.items(), key=lambda x: x[1], reverse=True)
    cell=[]
    pvalue=[]
    for c, p in tracks.items():
        cell.append(c)
        pvalue.append(p)

    cell=cell[:10]
    print(cell)
    pvalue=pvalue[:10]
    print(pvalue)

    width = 0.20
    index = np.arange(len(cell))
    p1 = np.arange(0, len(cell), 0.01)
    p2 = 0.05 + p1 * 0

    figsize = (10, 8)
    plt.plot(p1, p2, color='red', label='5% significance level')
    plt.bar(index, pvalue, width, color="#87CEFA")
    plt.xlabel('song title')
    plt.ylabel('stream value')
    plt.title('top10_track')
    plt.xticks(index, cell, fontsize=5)
    plt.legend(bbox_to_anchor=(1.05, 0), loc=3, borderaxespad=0)
    plt.savefig('top10_track.png', dpi=400)

def find_top_name_stram(data):
    artists={}
    for i in data:
        if i.name in artists.keys():
            artists[i.name] += 1
        else:
            artists[i.name] = 1
    sorted(artists.items(), key=lambda x: x[1], reverse=True)
    a=[]
    n=[]
    for artist,num in artists.items():
        a.append(artist)
        n.append(num)

    labels = a[:10]
    share = n[:10]

    print(labels)
    print(share)

    explode = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    plt.pie(share, explode=explode, labels=labels,
            colors=['c', 'r', 'gray', 'g', 'y', 'b', 'm', 'lightgreen', 'lightskyblue', 'lightcoral'], autopct='%1.1f%%', shadow=False, startangle=50)
    plt.axis('equal')

    plt.title('Top 10 Artist with the most streams')

    plt.savefig('top10_artist.png', dpi=400)


def find_top_track_region(data):
    NA={}
    EU={}
    AS={}
    SA={}
    OC={}
    country_dic=read_json()
    for i in data:
        if i.region.upper() in country_dic.keys():
            if country_dic[i.region.upper()]=='NA':
                if i.title in NA.keys():
                    NA[i.title] += 1
                else:
                    NA[i.title]=1
            if country_dic[i.region.upper()]=='EU':
                if i.title in EU.keys():
                    EU[i.title] += 1
                else:
                    EU[i.title]=1
            if country_dic[i.region.upper()]=='AS':
                if i.title in AS.keys():
                    AS[i.title] += 1
                else:
                    AS[i.title]=1
            if country_dic[i.region.upper()]=='SA':
                if i.title in SA.keys():
                    SA[i.title] += 1
                else:
                    SA[i.title]=1
            if country_dic[i.region.upper()]=='OC':
                if i.title in OC.keys():
                    OC[i.title] += 1
                else:
                    OC[i.title]=1

    sorted(NA.items(), key=lambda x: x[1], reverse=True)
    sorted(EU.items(), key=lambda x: x[1], reverse=True)
    sorted(AS.items(), key=lambda x: x[1], reverse=True)
    sorted(SA.items(), key=lambda x: x[1], reverse=True)
    sorted(OC.items(), key=lambda x: x[1], reverse=True)


    track_NA = list(NA.keys())[:10]
    track_EU = list(EU.keys())[:10]
    track_AS = list(AS.keys())[:10]
    track_SA = list(SA.keys())[:10]
    track_OC = list(OC.keys())[:10]

    print('##finish load figure data')

    same = [x for x in track_NA if x in track_EU and x in track_AS and x in track_SA and x in track_OC]
    defer = [y for y in (track_NA + track_EU + track_AS + track_SA + track_OC) if y not in same]

    bar_num = len(same) + len(defer)

    fig, ax = plt.subplots()
    x_data = ['NA', 'EU', 'AS', 'SA', 'OC']
    y_data={}
    for num in range(len(same)):
        col=[]
        col.append(NA[same[num]])
        col.append(EU[same[num]])
        col.append(AS[same[num]])
        col.append(SA[same[num]])
        col.append(OC[same[num]])
        y_data[same[num]]=col
    for num in range(len(defer)):
        if defer[num] in track_NA:
            col=[]
            col.append(NA[defer[num]])
            col.append(int(0))
            col.append(0)
            col.append(0)
            col.append(0)
        if defer[num] in track_EU:
            col = []
            col.append(0)
            col.append(EU[defer[num]])
            col.append(0)
            col.append(0)
            col.append(0)
        if defer[num] in track_AS:
            col = []
            col.append(0)
            col.append(0)
            col.append(AS[defer[num]])
            col.append(0)
            col.append(0)
        if defer[num] in track_SA:
            col = []
            col.append(0)
            col.append(0)
            col.append(0)
            col.append(SA[defer[num]])
            col.append(0)
        if defer[num] in track_OC:
            col = []
            col.append(0)
            col.append(0)
            col.append(0)
            col.append(0)
            col.append(OC[defer[num]])
        y_data[defer[num]] = col

    j=1
    for y_key,y_vaule in y_data.items():
        plt.bar(x=x_data, height=y_vaule, label=y_key, color=randomcolor(), alpha=0.8)
        if j==10:
            for x, y in enumerate(y_vaule):
                plt.text(x, y + 100, '%s' % y, ha='center', va='top',fontsize=6)
        j+=1
    bar_width = 0.3
    plt.subplots_adjust(right=0.6)

    plt.title("top10_track_region")

    plt.xlabel("region")
    plt.ylabel("stream")

    plt.legend(bbox_to_anchor=(1.05, 0), loc=3, borderaxespad=0, ncol=4, markerscale=0.5,fancybox=True, fontsize=8)
    plt.savefig('top10_track_region.png', dpi=400)



def plt_ShapeOfYou(data):
    record={}
    for i in data:
        if i.title=='Shape of You':
            record[i.data]=i.stream
    unsorted_record=record
    record=sorted(record.items(), key=lambda x: x[1], reverse=True)
    j=1
    ranking_record={}
    for key in record:
        ranking_record[key[0]]=j
        j+=1
    final_record={}
    for key1,vaule1 in unsorted_record.items():
        for key2,vaule2 in ranking_record.items():
            if key1==key2:
                dr=[]
                dr.append(vaule1)
                dr.append(vaule2)
                final_record[key1]=dr


    X_values = final_record.keys()
    Y_values_1=[]
    Y_values_2=[]
    for v in final_record.values():
        Y_values_1.append(v[0])
        Y_values_2.append(v[1])
    print ('finish load figure data')

    fig, ax1 = plt.subplots(figsize=(12, 9))
    title = ('The Number of Players Drafted and Average Career WS/48\nfor each Draft (1966-2014)')
    plt.title(title, fontsize=20)
    plt.grid(axis='y', color='grey', linestyle='--', lw=0.5, alpha=0.5)
    plt.tick_params(axis='both', labelsize=14)
    plot1 = ax1.plot(X_values, Y_values_1, 'b', label='No. of Players Drafted')
    ax1.plot(X_values, Y_values_1, 'b', label='No. of Players Drafted')
    ax1.set_ylabel('Number of Players Drafted', fontsize=18)
    ax1.set_ylim(0, 28000)
    for tl in ax1.get_yticklabels():
        tl.set_color('b')
    ax2 = ax1.twinx()
    plot2 = ax2.plot(X_values, Y_values_2, 'g', label='Avg WS/48')
    ax2.plot(X_values, Y_values_2, 'g', label='Avg WS/48')
    ax2.set_ylabel('Win Shares Per 48 minutes', fontsize=18)
    ax2.set_ylim(0, 380)
    ax2.tick_params(axis='y', labelsize=14)
    for tl in ax2.get_yticklabels():
        tl.set_color('g')
    #ax2.set_xlim(1966, 2014.15)
    lines = plot1 + plot2
    ax1.legend(lines, [l.get_label() for l in lines])
    ax1.set_yticks(np.linspace(ax1.get_ybound()[0], ax1.get_ybound()[1], 9))
    ax2.set_yticks(np.linspace(ax2.get_ybound()[0], ax2.get_ybound()[1], 9))
    for ax in [ax1, ax2]:
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
    # fig.text(0.1, 0.02,
    #          'The original content: http://savvastjortjoglou.com/nba-draft-part02-visualizing.html\nPorter: MingYan',
    #          fontsize=10)
    plt.savefig("ShapeOfYou.png", dpi=400)

def plt_ShapeOfYou_mouth(data):
    record={}
    for i in data:
        if i.title=='Shape of You':
            if i.data.split('-')[1] in record.keys():
                record[i.data.split('-')[1]] += i.stream
            else:
                record[i.data.split('-')[1]]=i.stream
    unsorted_record=record
    record=sorted(record.items(), key=lambda x: x[1], reverse=True)
    j=1
    ranking_record={}
    for key in record:
        ranking_record[key[0]]=j
        j+=1
    final_record={}
    for key1,vaule1 in unsorted_record.items():
        for key2,vaule2 in ranking_record.items():
            if key1==key2:
                dr=[]
                dr.append(vaule1)
                dr.append(vaule2)
                final_record[key1]=dr

    final_record=sorted(final_record.items(), key=lambda x: x[0])
    print (final_record)

    X_values=[]
    Y_values_1 = []
    Y_values_2 = []
    for first_l in final_record:
        X_values.append(first_l[0])
        Y_values_1.append(first_l[1][0])
        Y_values_2.append(first_l[1][1])
    print ('finish load figure data')

    fig, ax1 = plt.subplots(figsize=(12, 9))
    title = ('The Number of Players Drafted and Average Career WS/48\nfor each Draft (1966-2014)')
    plt.title(title, fontsize=20)
    plt.grid(axis='y', color='grey', linestyle='--', lw=0.5, alpha=0.5)
    plt.tick_params(axis='both', labelsize=14)
    plot1 = ax1.plot(X_values, Y_values_1, 'b', label='No. of Players Drafted')
    ax1.plot(X_values, Y_values_1, 'b', label='No. of Players Drafted')
    ax1.set_ylabel('Number of Players Drafted', fontsize=18)
    #ax1.set_ylim(0, 50000)
    for tl in ax1.get_yticklabels():
        tl.set_color('b')
    ax2 = ax1.twinx()
    plot2 = ax2.plot(X_values, Y_values_2, 'g', label='Avg WS/48')
    ax2.plot(X_values, Y_values_2, 'g', label='Avg WS/48')
    ax2.set_ylabel('Win Shares Per 48 minutes', fontsize=18)
    ax2.set_ylim(0, 12)
    ax2.tick_params(axis='y', labelsize=14)
    for tl in ax2.get_yticklabels():
        tl.set_color('g')
    #ax2.set_xlim(1966, 2014.15)
    lines = plot1 + plot2
    ax1.legend(lines, [l.get_label() for l in lines])
    ax1.set_yticks(np.linspace(ax1.get_ybound()[0], ax1.get_ybound()[1], 9))
    ax2.set_yticks(np.linspace(ax2.get_ybound()[0], ax2.get_ybound()[1], 9))
    for ax in [ax1, ax2]:
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
    # fig.text(0.1, 0.02,
    #          'The original content: http://savvastjortjoglou.com/nba-draft-part02-visualizing.html\nPorter: MingYan',
    #          fontsize=10)
    plt.savefig("ShapeOfYou2.png", dpi=400)


# find_top_track_stream()

data=read_cvs()
# #find_top_track_region(data)
find_top_track_stream(data)
