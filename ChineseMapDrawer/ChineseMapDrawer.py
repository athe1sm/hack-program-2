import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.colors import rgb2hex
import numpy as np
import pandas as pd
def Chinese_Map_Drawer(colortype):
    '''

    '''
    fig = plt.figure()
#    ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.8])

    map = Basemap(projection='mill',
              llcrnrlat=14,  # left corner latitude
              llcrnrlon=72,  # left corner longitude
              urcrnrlat=55,  # right corner latitude
              urcrnrlon=137,  # right corner longitude
              resolution='h',
              area_thresh=10000
                  )

    # map.drawmapboundary(fill_color='aqua')    # foreground color
    map.readshapefile('./gadm36_CHN_shp/gadm36_CHN_1/gadm36_CHN_1', 'NAME_1', drawbounds=True)  # mainland China
    map.drawcountries(linewidth=1.5)
    map.drawmapboundary()

    font1 = {'family': 'courier_new', 'weight' : 'normal', 'size' : 10}

    # labels = [left,right,top,bottom]
    map.drawmeridians(np.arange(0, 360, 15),labels=[0,1,1,0])  # 绘制经线
    map.drawparallels(np.arange(-90, 90, 15), labels=[0,1,1,0])  # 绘制纬线

    df = pd.read_csv('./ChineseMapDrawer/CHN_POP_CASE.csv',encoding='gbk')
    new_index_list = []
    for i in df["NAME_1"]:
        i = i.replace(" ", "")
        new_index_list.append(i)
    new_index = {"regions": new_index_list}
    new_index = pd.DataFrame(new_index)
    df = pd.concat([df, new_index], axis=1)
    df = df.drop(["NAME_1"], axis=1)
    df.set_index("regions", inplace=True)
    provinces = map.NAME_1_info
    statenames = []
    colors = {}
    if colortype =='YlGn_r':
        cmap = plt.cm.YlGn_r
    elif colortype =='YlGn':
        cmap = plt.cm.YlGn
    elif colortype =='mono':
        cmap = plt.cm.Greys_r
    
        
    vmax = 30
    vmin = 0

    for each_province in provinces:
        province_name = each_province['NL_NAME_1']
        pro_eng = each_province['NAME_1'].replace(" ", "")
        p = province_name.split('|')
        if len(p) > 1:
            s = p[1]
        else:
            s = p[0]
        s = s[:2]
        if s == '黑龍':
            s = '黑龙江'
        if s == '内蒙':
            s = '内蒙古'
        statenames.append(s)
        CPM = df['CPM'][s] #get case per million
        colors[s] = cmap(1-np.sqrt((CPM - vmin) / (vmax - vmin)))[:3]

    ax = plt.gca()
    for nshape, seg in enumerate(map.NAME_1):
        color = rgb2hex(colors[statenames[nshape]])
        poly = Polygon(seg, facecolor=color, edgecolor=color)
        ax.add_patch(poly)
    #plt.show()


    def draw_scatter_map(map, lon, lat, label, save=False, save_format='.svg'):
        value = np.array(df['cases'], dtype=float)
        size = (value / np.mean(value))* 65
        x, y = map(lon, lat)
        map.scatter(x, y, s=size, c='r', alpha=0.7, zorder=10)
        ax.set_xlabel(label, font1)
        if save:
            fig.savefig(label + save_format)
        plt.show()


    lon = np.array(df['lon'])
    lat = np.array(df['lat'])
    draw_scatter_map(map, lon, lat, "\nCovid-19 cases distribution in Mainland China", save=True, save_format='.png')

if __name__=='__main__':
    Chinese_Map_Drawer('mono')
