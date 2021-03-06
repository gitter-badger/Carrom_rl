from Utils import *
import time
import socket
import math
import sys
from thread import *
import ast

import argparse



parser = argparse.ArgumentParser()


parser.add_argument('-p', '--port', dest="PORT", type=int,
                        default=12121,
                        help='Port')


args=parser.parse_args()




host = '127.0.0.1'
port = args.PORT

#holes =[(22.21,22.21),(22.21,800-22.21),(800-22.21,22.21),(800-22.21,800-22.21)]
holes =[(0,0),(0,800),(800,0),(800,800)]
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

def get_coin_max_sep(coin_list) :
    maxi_index = 0
    maxi_dist = 0
    dist = 0
    for i in range(0,len(coin_list)) :
        dist = get_dist(coin_list,i)
        if dist > maxi_dist :
            maxi_dist = dist
            maxi_index = i
    return maxi_index

def get_dist(coin_list, index) :
    dist = 0;
    for j in range(0,len(coin_list)):
        dist = dist + (coin_list[index][1]-coin_list[j][1])*(coin_list[index][1]-coin_list[j][1]) + (coin_list[index][0]-coin_list[j][0])*(coin_list[index][0]-coin_list[j][0])
    return dist

def find_nearest_hole(coin) :
    maxi_index = 0
    maxi_dist = 0
    distance = 0
    for j in range(0,len(holes)):
        distance = dist(holes[j],coin)
        if distance > maxi_dist :
            maxi_dist = distance
            maxi_index = j
    return holes[maxi_index],math.sqrt(maxi_dist)


def get_most_suitable_x(list_of_x,coin_list,to_hit, angle_to_hole) :
    max_max_travelable_dist = 0
    # random.shuffle(list_of_x)
    index = 0
    
    # y = 145
    # x=to_hit[0] + (y-to_hit[1])*math.tan(angle_to_hole)
    # x = max(min(630,x),170)
    # return x,dist(to_hit,(x,y))

    for i in range (0,len(list_of_x)) :
        unobstructed_distance = (to_hit[0] - list_of_x[i])*(to_hit[0] - list_of_x[i]) + (to_hit[1] - 145)*(to_hit[1] - 145)
        #angle = math.atan2((to_hit[1]-145),(to_hit[0]-list_of_x[i]))
        minx = min(list_of_x[i], to_hit[0])
        maxx = max(list_of_x[i], to_hit[0])
        miny = min(145, to_hit[1])
        maxy = max(145, to_hit[1])
        for j in range(0,len(coin_list)):
            if coin_list[j][0] >= minx and coin_list[j][0] <= maxx and coin_list[j][1] >= miny and coin_list[j][1] <= maxy :
                distance = dist(coin_list[j],(list_of_x[i],145))
                if distance < unobstructed_distance :
                    unobstructed_distance = distance
        if unobstructed_distance == dist(to_hit,(list_of_x[i],145)):
            return list_of_x[i], unobstructed_distance

        if unobstructed_distance > max_max_travelable_dist : 
            max_max_travelable_dist = unobstructed_distance
            index = i
    return list_of_x[index], max_max_travelable_dist



#170:630
while 1:
        tm = s.recv(1024)
        try:
            S,r=parse_state_message(tm)
            #print S,r
        except:
            print "Something went wrong",tm

            
        if  len(S["White_Locations"])!=0 or len(S["Black_Locations"])!=0 or len(S["Red_Location"])!=0:
            to_hit_list=S["White_Locations"]+S["Black_Locations"]+S["Red_Location"]
            to_hit = to_hit_list[get_coin_max_sep(to_hit_list)]
            hole,dist1 = find_nearest_hole(to_hit)
            angle_to_hole = math.atan2((to_hit[1]-hole[1]),(to_hit[0]-hole[0]))
            point_to_aim = ((to_hit[0]) - 20.6*math.cos(angle_to_hole),(to_hit[1]) - 20.6*math.sin(angle_to_hole))
            list_of_x = [170,190,210,230,250,270,290,310,330,350,370,390,410,430,450,470,490,510,530,550,570,590,610,630]
            x,dist2 = get_most_suitable_x(list_of_x,to_hit_list,to_hit, angle_to_hole)
            loc = (x,145)
            angle=math.atan2((to_hit[1]-loc[1]),(to_hit[0]-loc[0]))
            if angle < 0:
                angle = angle + 2*3.14
            #a=str(angle)+ ',' + str(float(x-170)/float(460))+','+str(0.5)
            a=str(angle)+ ',' + str(float(x-170)/float(460))+','+str(random.random()/1.25) # Remove in actual test
            #a=str(angle)+ ',' + str(float(x-170)/float(460))+','+str(0.5*dist2/800) # Remove in actual test
        else:
            a=None
        try:
            print a + ":::" + str(to_hit) + "+++" + str(loc)
            s.send(a)
        except:
            print "Error in sending:",  a
	    print "Closing Connection"
	    break
s.close()
