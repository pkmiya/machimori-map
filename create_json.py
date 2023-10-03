# coding: UTF-8
import json
from datetime import date, datetime
from DB import DB
import requests

def iktoaddress(lat, lon):
    url = "https://www.finds.jp/ws/rgeocode.php?json&lat="+str(lat)+"&lon="+str(lon)
    response = requests.get(url)
    js = json.loads(response.text)
    pm = js['result']['prefecture']['pname']+js['result']['municipality']['mname']
    try:
        sh = js['result']['local'][0]['section']+js['result']['local'][0]['homenumber']
        return pm+sh
    except KeyError:
        return pm

class My_Json():
    def data_molding(self, okind, odata, skind, sdata, inuserdata, user_flag):
        db = DB()
        plot_list = []
        for ulis in inuserdata:
            plot_dict = {}
            if user_flag == 0:
                plot_dict['buzzer_num'] = ulis[0]
            elif user_flag == 1:
                plot_dict['buzzer_num'] = -1
            plot_dict['lat'] = ulis[1]
            plot_dict['lon'] = ulis[2]
            plot_list.append(plot_dict)
        
        for olis in odata:
            if olis[6] == 1:
                continue
            plot_dict = {}
            plot_dict['kind'] = okind
            plot_dict['lat'] = olis[3]
            plot_dict['lon'] = olis[4]
            plot_dict['time'] = olis[5].strftime('%Y/%m/%d %H:%M:%S')
            plot_dict['case'] = olis[7]
            plot_dict['buzzer_num'] = olis[2]
            plot_dict['address'] = iktoaddress(olis[3], olis[4])
            plot_list.append(plot_dict)

        for slis in sdata:
            plot_dict = {}
            plot_dict['kind'] = skind
            plot_dict['lat'] = slis[2]
            plot_dict['lon'] = slis[3]
            plot_dict['name'] = slis[4]
            plot_dict['address'] = slis[1]
            plot_dict['img'] = slis[7]
            plot_list.append(plot_dict)
        return plot_list

if __name__ == '__main__':
    i_json = My_Json()
    #i_json.data_molding()
