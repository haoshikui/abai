#!/usr/bin/python
# -*- coding: UTF-8 -*-
from struct import *
import struct
import binascii
import datetime
import time
import commonlib
import string
import os
import cx_Oracle
import math
fs = open("xaa.bin", "rb")
count = 0
Tsat = 0.0;
Tsat0 = 0.0;
Tsatpr = 0.0;
Tsat1 = 0.0;
data_num = 0#解析的总数据组数
Tsat_sum_error_num = 0
Tsat_missing_Num = 0
Acc_Sum_error = 0
data_1hz = []
data_4hz = []
data_quality_list = []
timetamp = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
fs_state = open( "状态量监测信号" + timetamp + ".txt","w+")
fs_state.writelines("year-month-day hour:minute:second Tacc Tsat Voltage_5V Voltage_12V Voltage_60V Voltage_Vb Ctl_state w2" +"\n");
fs_state.writelines("year-month-day hour:minute:second s s V V V V 0H 0d" +"\n");
fs_temperature = open("四路温度信号" + timetamp + ".txt","w+");
fs_temperature.writelines("year-month-day hour:minute:second Tacc Tsat T1 T2 T3 T4");
fs_temperature.writelines("year-month-day hour:minute:second s s oC oC oC oC");
fs_Verror = open("六通道传感电压" + timetamp + ".txt","w+");
fs_Verror.writelines("year-month-day hour:minute:second Tacc Tsat Ctl_state x1 x2 x3 y z1 z2");
fs_Verror.writelines("year-month-day hour:minute:second s s 0H V V V V V V");
fs_VerrorDOF = open("六自由度残差电压" + timetamp + ".txt","w+");
fs_VerrorDOF.writelines("year-month-day hour:minute:second Tacc Tsat Ctl_state X Y Z Rx Ry Rz");
fs_VerrorDOF.writelines("year-month-day hour:minute:second s s 0H V V V V V V");
fs_DPerror = open("六自由度位移残差" + timetamp + ".txt","w+");
fs_DPerror.writelines("year-month-day hour:minute:second Tacc Tsat Ctl_state dpx dpy dpz dprx dpry dprz");
fs_DPerror.writelines("year-month-day hour:minute:second s s 0H um um um mrad mrad mrad");
fs_Vfed = open("六自由度反馈电压" + timetamp + ".txt","w+")
fs_Vfed.writelines("year-month-day hour:minute:second Tacc Tsat Ctl_state X_Vfed Y_Vfed Z_Vfed RX_Vfed RY_Vfed RZ_Vfed");
fs_Vfed.writelines("year-month-day hour:minute:second s s 0H V V V V V V");
fs_afed = open("六自由度反馈加速度" + timetamp + ".txt","w+")
fs_afed.writelines("year-month-day hour:minute:second Tacc Tsat Ctl_state X_afed Y_afed Z_afed RX_afed RY_afed RZ_afed");
fs_afed.writelines("year-month-day hour:minute:second s s 0H m/s2 m/s2 m/s2 rad/s2 rad/s2 rad/s2");
fs_Vtemp = open("四路温度传感器电压" + timetamp + ".txt","w+")
fs_Vtemp.writelines("year-month-day hour:minute:second Tacc Tsat Vt1 Vt2 Vt3 Vt4");
fs_Vtemp.writelines("year-month-day hour:minute:second s s V V V V");
try:
    while fs.tell() < os.path.getsize("xaa.bin")-160:
        str_tmp = fs.read(5)
        #text = int.from_bytes(str, byteorder='big')
        #data_raw = struct.unpack('i' * 2, str)
        hexstr = binascii.b2a_hex(str_tmp)
        #print("读取的字符串是 : ", hexstr)
        string = hexstr.decode()
        barray = bytearray.fromhex(string)
        if (barray[0] == 0x99) and (barray[1] == 0x68) and (barray[2] == 0x00) and (barray[3] == 0x68) and (barray[4] == 0x33):
            # count = count +1
            # print(count)
            # print("haha")
            fs.seek(-5,1)
            input_fs = fs.read(155);
            hexstr = binascii.b2a_hex(input_fs)
            #print("读取的字符串是 : ", hexstr)
            string = hexstr.decode()
            input = bytearray.fromhex(string)
            #根据加速度计帧尾标识99,63，判断确认是否为一包数据，加入转换计算代码
            print(fs.tell())
            if ((input[150] == 0x99) and (input[151] == 0x63)):
                #print("haha")
                summ = input[154]; # 数据包中的SUM校验码
                sum1 = 0;
                for index in range(154): # 以前是j=10
                     sum1 += input[index];
                sum1 = sum1 - (0x99 + 0x68) * 15 - 0x99 - 0x63 - 1 - 2 - 3 - 4 - 5 - 6 - 7 - 8 - 9 - 0x0A - 0x0B - 0x0C - 0x0D - 0x0E - 0x0F - 0x68;
                sum1 = sum1 % 256; # 取最低的1个字节
                if (summ == sum1):# sum校验d
                    fs.seek(-165,1)
                    #print("test1")
                    input_fs = fs.read(10)
                    hexstr = binascii.b2a_hex(input_fs)
                    string = hexstr.decode()
                    test = bytearray.fromhex(string)
                    if ((test[0] == 0x4F) and (test[1] == 0x08) and (test[2] == 0x80)):
                        sum_temp = test[2];
                        for index in range(3,9): # 读取6个字节（星时），依次存入数组test[]
                            sum_temp += test[index];
                        if (test[9] == sum_temp % 256): # sum校验
                            Tsat = test[3] * 16777216 + test[4] * 65536 + test[5] * 256 + test[6] + (test[7] * 256 + test[8]) * 0.001; # 前四个字节单位为秒，后2个字节单位为毫秒
                            #print("test2")
                            if (int(Tsat0) == 0):
                                Tsat0 = Tsat
                        else:
                            Tsat_sum_error_num += 1
                    else: # 未出现星时广播标识，退回到起始位置
                         # fs.Seek(-10, SeekOrigin.Current);
                        Tsat_missing_Num += 1
                    fs.seek(155,1)
                    Voltage_5V = input[8] * 5 / 128.0# input[14]=w3
                    Voltage_12V = input[9] * 5 / 128.0 # input[15]=w4
                    Voltage_60V = input[13] * 5 / 128.0 # input[19]=w5
                    x1 = input[14] * 256 + input[15]
                    x2 = input[16] * 256 + input[17]
                    x3 = input[18] * 256 + input[19]
                    y = input[23] * 256 + input[24]
                    z1 = input[25] * 256 + input[26]
                    z2 = input[27] * 256 + input[28]
                    if (x1 >= 32768):
                        x1 = x1 - 65536
                    x1 = x1 * 5 / 32768.0
                    if (x2 >= 32768):
                        x2 = x2 - 65536
                    x2 = x2 * 5 / 32768.0
                    if (x3 >= 32768):
                        x3 = x3 - 65536
                    x3 = x3 * 5 / 32768.0
                    if (y >= 32768):
                        y = y - 65536
                    y = y * 5 / 32768.0
                    if (z1 >= 32768):
                        z1 = z1 - 65536
                    z1 = z1 * 5 / 32768.0
                    if (z2 >= 32768):
                        z2 = z2 - 65536
                    z2 = z2 * 5 / 32768.0
                    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                    Ctl_state = round(input[29])
                    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # /
                    Voltage_Vb = input[33] * 256 + input[34]
                    if (Voltage_Vb >= 32768):
                        Voltage_Vb = Voltage_Vb - 65536
                    Voltage_Vb = Voltage_Vb * 5 / 32768.0
                    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                    T1 = input[35] * 256 + input[36]
                    T2 = input[37] * 256 + input[38]
                    T3 = input[39] * 256 + input[43]
                    T4 = input[44] * 256 + input[45]
                    if (T1 >= 32768):
                        T1 = T1 - 65536
                    T1 = T1 * 5 / 32768.0

                    if (T2 >= 32768):
                        T2 = T2 - 65536
                    T2 = T2 * 5 / 32768.0

                    if (T3 >= 32768):
                        T3 = T3 - 65536
                    T3 = T3 * 5 / 32768.0

                    if (T4 >= 32768):
                        T4 = T4 - 65536
                    T4 = T4 * 5 / 32768.0
                    Vt1 = T1
                    Vt2 = T2
                    Vt3 = T3
                    Vt4 = T4

                    T1 = 332.44763 - 224.42236 * T1 + 63.37451 * T1 * T1 - 7.10285 * T1 * T1 * T1 # 将电压转换为温度
                    T2 = 407.76424 - 286.87752 * T2 + 81.92208 * T2 * T2 - 8.95061 * T2 * T2 * T2 # 将电压转换为温度
                    T3 = 343.72737 - 235.1239 * T3 + 66.81767 * T3 * T3 - 7.45991 * T3 * T3 * T3 # 将电压转换为温度
                    T4 = 399.67404 - 280.94112 * T4 + 80.24316 * T4 * T4 - 8.78317 * T4 * T4 * T4 # 将电压转换为温度
                    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # /
                    X_Vfed_1 = input[46] * 65536 + input[47] * 256 + input[48]
                    Y_Vfed_1 = input[49] * 65536 + input[53] * 256 + input[54]
                    Z_Vfed_1 = input[55] * 65536 + input[56] * 256 + input[57]
                    RX_Vfed_1 = input[58] * 65536 + input[59] * 256 + input[63]
                    RY_Vfed_1 = input[64] * 65536 + input[65] * 256 + input[66]
                    RZ_Vfed_1 = input[67] * 65536 + input[68] * 256 + input[69]

                    if (X_Vfed_1 >= 8388608):
                        X_Vfed_1 = X_Vfed_1 - 16777216
                    X_Vfed_1 = X_Vfed_1 * 10 / 8388608.0

                    if (Y_Vfed_1 >= 8388608):
                        Y_Vfed_1 = Y_Vfed_1 - 16777216
                    Y_Vfed_1 = Y_Vfed_1 * 10 / 8388608.0

                    if (Z_Vfed_1 >= 8388608):
                        Z_Vfed_1 = Z_Vfed_1 - 16777216
                    Z_Vfed_1 = Z_Vfed_1 * 10 / 8388608.0

                    if (RX_Vfed_1 >= 8388608):
                        RX_Vfed_1 = RX_Vfed_1 - 16777216
                    RX_Vfed_1 = RX_Vfed_1 * 10 / 8388608.0

                    if (RY_Vfed_1 >= 8388608):
                        RY_Vfed_1 = RY_Vfed_1 - 16777216
                    RY_Vfed_1 = RY_Vfed_1 * 10 / 8388608.0

                    if (RZ_Vfed_1 >= 8388608):
                        RZ_Vfed_1 = RZ_Vfed_1 - 16777216
                    RZ_Vfed_1 = RZ_Vfed_1 * 10 / 8388608.0
                    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # /

                    X_Vfed_2 = input[73] * 65536 + input[74] * 256 + input[75]
                    Y_Vfed_2 = input[76] * 65536 + input[77] * 256 + input[78]
                    Z_Vfed_2 = input[79] * 65536 + input[83] * 256 + input[84]
                    RX_Vfed_2 = input[85] * 65536 + input[86] * 256 + input[87]
                    RY_Vfed_2 = input[88] * 65536 + input[89] * 256 + input[93]
                    RZ_Vfed_2 = input[94] * 65536 + input[95] * 256 + input[96]

                    if (X_Vfed_2 >= 8388608):
                        X_Vfed_2 = X_Vfed_2 - 16777216
                    X_Vfed_2 = X_Vfed_2 * 10 / 8388608.0

                    if (Y_Vfed_2 >= 8388608):
                        Y_Vfed_2 = Y_Vfed_2 - 16777216
                    Y_Vfed_2 = Y_Vfed_2 * 10 / 8388608.0

                    if (Z_Vfed_2 >= 8388608):
                        Z_Vfed_2 = Z_Vfed_2 - 16777216
                    Z_Vfed_2 = Z_Vfed_2 * 10 / 8388608.0

                    if (RX_Vfed_2 >= 8388608):
                        RX_Vfed_2 = RX_Vfed_2 - 16777216
                    RX_Vfed_2 = RX_Vfed_2 * 10 / 8388608.0

                    if (RY_Vfed_2 >= 8388608):
                        RY_Vfed_2 = RY_Vfed_2 - 16777216
                    RY_Vfed_2 = RY_Vfed_2 * 10 / 8388608.0

                    if (RZ_Vfed_2 >= 8388608):
                        RZ_Vfed_2 = RZ_Vfed_2 - 16777216
                    RZ_Vfed_2 = RZ_Vfed_2 * 10 / 8388608.0
                    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

                    X_Vfed_3 = input[97] * 65536 + input[98] * 256 + input[99]
                    Y_Vfed_3 = input[103] * 65536 + input[104] * 256 + input[105]
                    Z_Vfed_3 = input[106] * 65536 + input[107] * 256 + input[108]
                    RX_Vfed_3 = input[109] * 65536 + input[113] * 256 + input[114]
                    RY_Vfed_3 = input[115] * 65536 + input[116] * 256 + input[117]
                    RZ_Vfed_3 = input[118] * 65536 + input[119] * 256 + input[123]

                    if (X_Vfed_3 >= 8388608):
                        X_Vfed_3 = X_Vfed_3 - 16777216
                    X_Vfed_3 = X_Vfed_3 * 10 / 8388608.0

                    if (Y_Vfed_3 >= 8388608):
                        Y_Vfed_3 = Y_Vfed_3 - 16777216
                    Y_Vfed_3 = Y_Vfed_3 * 10 / 8388608.0

                    if (Z_Vfed_3 >= 8388608):
                        Z_Vfed_3 = Z_Vfed_3 - 16777216
                    Z_Vfed_3 = Z_Vfed_3 * 10 / 8388608.0

                    if (RX_Vfed_3 >= 8388608):
                        RX_Vfed_3 = RX_Vfed_3 - 16777216
                    RX_Vfed_3 = RX_Vfed_3 * 10 / 8388608.0

                    if (RY_Vfed_3 >= 8388608):
                        RY_Vfed_3 = RY_Vfed_3 - 16777216
                    RY_Vfed_3 = RY_Vfed_3 * 10 / 8388608.0

                    if (RZ_Vfed_3 >= 8388608):
                        RZ_Vfed_3 = RZ_Vfed_3 - 16777216
                    RZ_Vfed_3 = RZ_Vfed_3 * 10 / 8388608.0
                    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

                    X_Vfed_4 = input[124] * 65536 + input[125] * 256 + input[126]
                    Y_Vfed_4 = input[127] * 65536 + input[128] * 256 + input[129]
                    Z_Vfed_4 = input[133] * 65536 + input[134] * 256 + input[135]
                    RX_Vfed_4 = input[136] * 65536 + input[137] * 256 + input[138]
                    RY_Vfed_4 = input[139] * 65536 + input[143] * 256 + input[144]
                    RZ_Vfed_4 = input[145] * 65536 + input[146] * 256 + input[147]
                    Tacc = (input[148] * 65536 + input[149] * 256 + input[153]) / 10.0

                    if (X_Vfed_4 >= 8388608):
                        X_Vfed_4 = X_Vfed_4 - 16777216
                    X_Vfed_4 = X_Vfed_4 * 10 / 8388608.0

                    if (Y_Vfed_4 >= 8388608):
                        Y_Vfed_4 = Y_Vfed_4 - 16777216
                    Y_Vfed_4 = Y_Vfed_4 * 10 / 8388608.0

                    if (Z_Vfed_4 >= 8388608):
                        Z_Vfed_4 = Z_Vfed_4 - 16777216
                    Z_Vfed_4 = Z_Vfed_4 * 10 / 8388608.0

                    if (RX_Vfed_4 >= 8388608):
                        RX_Vfed_4 = RX_Vfed_4 - 16777216
                    RX_Vfed_4 = RX_Vfed_4 * 10 / 8388608.0

                    if (RY_Vfed_4 >= 8388608):
                        RY_Vfed_4 = RY_Vfed_4 - 16777216
                    RY_Vfed_4 = RY_Vfed_4 * 10 / 8388608.0

                    if (RZ_Vfed_4 >= 8388608):
                        RZ_Vfed_4 = RZ_Vfed_4 - 16777216
                    RZ_Vfed_4 = RZ_Vfed_4 * 10 / 8388608.0
                    if (Ctl_state == 0x00 or Ctl_state == 0x10 or Ctl_state == 0x10 or Ctl_state == 0x80):
                        Hs_x = 0.87E6
                        Hs_y = 0.61E6
                        Hs_z = 0.56E6
                        Hs_rx = 4.64E3
                        Hs_ry = 8.92E3
                        Hs_rz = 4.46E3
                        # # 单位V / um, V / um, V / um, V / mrad, V / mrad, V / mrad
                    elif (Ctl_state == 0x30 or Ctl_state == 0x40 or Ctl_state == 0x50 or Ctl_state == 0x60 or Ctl_state == 0x70):
                        Hs_x = 3.48E6
                        Hs_y = 2.43E6
                        Hs_z = 2.25E6
                        Hs_rx = 18.56E3
                        Hs_ry = 35.67E3
                        Hs_rz = 17.83E3
                    else:
                        print("控制参数错误")

    # # / REV5
    # .2
    # 修改Ha赋值方式（重要！）
                    if (Voltage_Vb < 1.5):
                        Ha_x = 2.0 * 0.001
                        Ha_y = 8.6 * 0.0001
                        Ha_z = 8.1 * 0.0001
                        Ha_rx = 2.55 * 0.01
                        Ha_ry = 0.15
                        Ha_rz = 7.4 * 0.01
                    # 单位m / s2 / v, m / s2 / v, m / s2 / v, rad / s2 / v, rad / s2 / v, rad / s2 / v
                    # Vb = 20.0;
                    else:
                        Ha_x = 4.0 * 0.001
                        Ha_y = 1.72 * 0.001
                        Ha_z = 1.62 * 0.001
                        Ha_rx = 5.1 * 0.01
                        Ha_ry = 0.30
                        Ha_rz = 0.15
                    # 单位m / s2 / v, m / s2 / v, m / s2 / v, rad / s2 / v, rad / s2 / v, rad / s2 / v
                    # Vb = 40.0;
                    # # 将电容传感器各极板对输出电压转换为各自由度残差电压 # REV4
                    # .1
                    # 新增
                    #
                    Verr_X = 2 * x1 + x2 + x3
                    Verr_Y = y
                    Verr_Z = z1 + z2
                    Verr_Rx = z2 - z1
                    Verr_Ry = -2 * x1 + x2 + x3
                    Verr_Rz = -x2 + x3

                    dpx = 1000000 * Verr_X / Hs_x
                    dpy = 1000000 * Verr_Y / Hs_y
                    dpz = 1000000 * Verr_Z / Hs_z
                    dprx = 1000 * Verr_Rx / Hs_rx
                    dpry = 1000 * Verr_Ry / Hs_ry
                    dprz = 1000 * Verr_Rz / Hs_rz

                    X_afed_1 = X_Vfed_1 * Ha_x
                    Y_afed_1 = Y_Vfed_1 * Ha_y
                    Z_afed_1 = Z_Vfed_1 * Ha_z
                    RX_afed_1 = RX_Vfed_1 * Ha_rx
                    RY_afed_1 = RY_Vfed_1 * Ha_ry
                    RZ_afed_1 = RZ_Vfed_1 * Ha_rz

                    X_afed_2 = X_Vfed_2 * Ha_x
                    Y_afed_2 = Y_Vfed_2 * Ha_y
                    Z_afed_2 = Z_Vfed_2 * Ha_z
                    RX_afed_2 = RX_Vfed_2 * Ha_rx
                    RY_afed_2 = RY_Vfed_2 * Ha_ry
                    RZ_afed_2 = RZ_Vfed_2 * Ha_rz

                    X_afed_3 = X_Vfed_3 * Ha_x
                    Y_afed_3 = Y_Vfed_3 * Ha_y
                    Z_afed_3 = Z_Vfed_3 * Ha_z
                    RX_afed_3 = RX_Vfed_3 * Ha_rx
                    RY_afed_3 = RY_Vfed_3 * Ha_ry
                    RZ_afed_3 = RZ_Vfed_3 * Ha_rz

                    X_afed_4 = X_Vfed_4 * Ha_x
                    Y_afed_4 = Y_Vfed_4 * Ha_y
                    Z_afed_4 = Z_Vfed_4 * Ha_z
                    RX_afed_4 = RX_Vfed_4 * Ha_rx
                    RY_afed_4 = RY_Vfed_4 * Ha_ry
                    RZ_afed_4 = RZ_Vfed_4 * Ha_rz

                    if Tacc > 0 and Tsat > 4: # 时间码为0的数据（二次电源主备切换时），各信号均为0，整包舍弃，可在后续处理时进行插值
                        if (Tsat == Tsatpr): # 连续四帧数据Tsat相同时，以第一帧Tsat为基准，计算出后续三帧的Tsat # Rev5.1
                            Tsat = Tsat + 1
                        if (Tsat - Tsatpr == -1):
                            Tsat = Tsat + 2
                        if (Tsat - Tsatpr == -2):
                            Tsat = Tsat + 3
                        Tsatpr = Tsat
                    # ** ** ** ** ** 将星上时转化为北京时，加在每个输出文件的开头 ** ** ** ** ** * #
                        Tsatint = (int)(Tsat)
                        #print("test3")
                        timestr_totxt = commonlib.date_convert(Tsatint+28800)
                        fs_state.writelines(timestr_totxt + " " + '%.2f' % Tacc + " " + '%.3f' % Tsat + " " + '%.6f' % Voltage_5V + " " + '%.6f' % Voltage_12V + " " + '%.6f' % Voltage_60V + " " + '%.6f' % Voltage_Vb + " "+ hex(Ctl_state) + " "+ str(input[13] % 16)+ "\n")
                        fs_temperature.writelines(timestr_totxt + " " + '%.2f' % Tacc + " " + '%.3f' % Tsat + " " + '%.6f' % T1 + " " + '%.6f' % T2 + " " + '%.6f' % T3 + " " + '%.6f' % T4);
                        fs_Verror.writelines(timestr_totxt + " " + '%.2f' % Tacc + " " + '%.3f' % Tsat + " " + hex(Ctl_state) + " " + '%.6f' % x1 + " " + '%.6f' % x2 + " " + '%.6f' % x3 + " " + '%.6f' % y + " " + '%.6f' % z1 + " " + '%.6f' % z2);
                        fs_VerrorDOF.writelines(timestr_totxt + " " + '%.2f' % Tacc + " " + '%.3f' % Tsat + " " + hex(Ctl_state) + " " + '%.6f' % Verr_X + " " + '%.6f' % Verr_Y + " " + '%.6f' % Verr_Z + " " + '%.6f' % Verr_Rx + " " + '%.6f' % Verr_Ry + " " + '%.6f' % Verr_Rz);
                        fs_Vfed.writelines(timestr_totxt + " " + '%.2f' % (Tacc+0.00) + " " + '%.3f' % (Tsat + 0.00) + " " + hex(Ctl_state) + " " + '%.6f' % X_Vfed_1 + " " + '%.6f' % Y_Vfed_1 + " " + '%.6f' % Z_Vfed_1 + " " + '%.6f' % RX_Vfed_1 + " " + '%.6f' % RY_Vfed_1 + " " + '%.6f' % RZ_Vfed_1);
                        fs_Vfed.writelines(timestr_totxt + " " + '%.2f' % (Tacc+0.25) + " " + '%.3f' % (Tsat + 0.25) + " " + hex(Ctl_state) + " " + '%.6f' % X_Vfed_2 + " " + '%.6f' % Y_Vfed_2 + " " + '%.6f' % Z_Vfed_2 + " " + '%.6f' % RX_Vfed_2 + " " + '%.6f' % RY_Vfed_2 + " " + '%.6f' % RZ_Vfed_2);
                        fs_Vfed.writelines(timestr_totxt + " " + '%.2f' % (Tacc+0.50) + " " + '%.3f' % (Tsat + 0.50) + " " + hex(Ctl_state) + " " + '%.6f' % X_Vfed_3 + " " + '%.6f' % Y_Vfed_3 + " " + '%.6f' % Z_Vfed_3 + " " + '%.6f' % RX_Vfed_3 + " " + '%.6f' % RY_Vfed_3 + " " + '%.6f' % RZ_Vfed_3);
                        fs_Vfed.writelines(timestr_totxt + " " + '%.2f' % (Tacc+0.75) + " " + '%.3f' % (Tsat + 0.75) + " " + hex(Ctl_state) + " " + '%.6f' % X_Vfed_4 + " " + '%.6f' % Y_Vfed_4 + " " + '%.6f' % Z_Vfed_4 + " " + '%.6f' % RX_Vfed_4 + " " + '%.6f' % RY_Vfed_4 + " " + '%.6f' % RZ_Vfed_4);
                        fs_DPerror.writelines(timestr_totxt + " " + '%.2f' % Tacc + " " + '%.3f' % Tsat + " " + hex(Ctl_state) + " " + '%.8f' % dpx + " " + '%.8f' % dpy + " " + '%.8f' % dpz + " " + '%.8f' % dprx + " " + '%.8f' % dpry + " " + '%.8f' % dprz);
                        fs_afed.writelines(timestr_totxt + " " + '%.2f' % (Tacc+0.00) + " " + '%.3f' % (Tsat + 0.00) + " " + hex(Ctl_state) + " " + '%.12f' % X_afed_1 + " " + '%.12f' % Y_afed_1 + " " + '%.12f' % Z_afed_1 + " " + '%.12f' % RX_afed_1 + " " + '%.12f' % RY_afed_1 + " " + '%.12f' % RZ_afed_1);
                        fs_afed.writelines(timestr_totxt + " " + '%.2f' % (Tacc+0.25) + " " + '%.3f' % (Tsat + 0.25) + " " + hex(Ctl_state) + " " + '%.12f' % X_afed_2 + " " + '%.12f' % Y_afed_2 + " " + '%.12f' % Z_afed_2 + " " + '%.12f' % RX_afed_2 + " " + '%.12f' % RY_afed_2 + " " + '%.12f' % RZ_afed_2);
                        fs_afed.writelines(timestr_totxt + " " + '%.2f' % (Tacc+0.50) + " " + '%.3f' % (Tsat + 0.50) + " " + hex(Ctl_state) + " " + '%.12f' % X_afed_3 + " " + '%.12f' % Y_afed_3 + " " + '%.12f' % Z_afed_3 + " " + '%.12f' % RX_afed_3 + " " + '%.12f' % RY_afed_3 + " " + '%.12f' % RZ_afed_3);
                        fs_afed.writelines(timestr_totxt + " " + '%.2f' % (Tacc+0.75) + " " + '%.3f' % (Tsat + 0.75) + " " + hex(Ctl_state) + " " + '%.12f' % X_afed_4 + " " + '%.12f' % Y_afed_4 + " " + '%.12f' % Z_afed_4 + " " + '%.12f' % RX_afed_4 + " " + '%.12f' % RY_afed_4 + " " + '%.12f' % RZ_afed_4);
                        fs_Vtemp.writelines(timestr_totxt + " " + '%.2f' % Tacc + " " + '%.3f' % Tsat + " " + '%.6f' % Vt1 + " " + '%.6f' % Vt2 + " " + '%.6f' % Vt3 + " " + '%.6f' % Vt4)
                        Tsat1 = Tsat;
                        date_timestr = datetime.datetime.strptime(timestr_totxt, "%Y-%m-%d %H:%M:%S")
                        data_1hz.append((date_timestr,Tsat,Tacc,Voltage_5V,Voltage_12V,Voltage_60V,x1,x2,x3,y,z1,z2,Ctl_state,Voltage_Vb,T1,T2,T3,T4,dpx,dpy,dpz,dprx,dpry,dprz,Verr_X,Verr_Y,Verr_Z,Verr_Rx,Verr_Ry,Verr_Rz))
                        data_4hz.append((date_timestr, Tsat, Tacc, X_afed_1, Y_afed_1, Z_afed_1, RX_afed_1, RY_afed_1,RZ_afed_1, X_Vfed_1, Y_Vfed_1, Z_Vfed_1, RX_Vfed_1, RY_Vfed_1, RZ_Vfed_1,Ctl_state))
                        data_4hz.append((date_timestr, Tsat+0.25, Tacc+0.25, X_afed_2, Y_afed_2, Z_afed_2, RX_afed_2, RY_afed_2,RZ_afed_2, X_Vfed_2, Y_Vfed_2, Z_Vfed_2, RX_Vfed_2, RY_Vfed_2, RZ_Vfed_2,Ctl_state))
                        data_4hz.append((date_timestr, Tsat+0.5, Tacc+0.5, X_afed_3, Y_afed_3, Z_afed_3, RX_afed_3, RY_afed_3,RZ_afed_3, X_Vfed_3, Y_Vfed_3, Z_Vfed_3, RX_Vfed_3, RY_Vfed_3, RZ_Vfed_3,Ctl_state))
                        data_4hz.append((date_timestr, Tsat+0.75, Tacc+0.75, X_afed_4, Y_afed_4, Z_afed_4, RX_afed_4, RY_afed_4,RZ_afed_4, X_Vfed_4, Y_Vfed_4, Z_Vfed_4, RX_Vfed_4, RY_Vfed_4, RZ_Vfed_4,Ctl_state))
                        data_num += 1 #包计数
                        if(len(data_1hz) == 100):
                            conn = cx_Oracle.Connection('cge/cge_123@127.0.0.1:1521/orcl')
                            # 获取操作游标
                            cursor = conn.cursor()
                            cursor.prepare("INSERT INTO MY_DATA_1HZ (BJTIME,TSAT,TACC,Voltage_5V,Voltage_12V,Voltage_60V,x1,x2,x3,y,z1,z2,Ctl_state,Voltage_Vb,T1,T2,T3,T4,dpx,dpy,dpz,dprx,dpry,dprz,Verr_X,Verr_Y,Verr_Z,Verr_Rx,Verr_Ry,Verr_Rz) VALUES (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13,:14,:15,:16,:17,:18,:19,:20,:21,:22,:23,:24,:25,:26,:27,:28,:29,:30)")
                            try:
                                cursor.executemany(None, data_1hz)
                                conn.commit()
                                cursor.close()
                            except cx_Oracle.DatabaseError as exc:
                                error, = exc.args
                            cursor = conn.cursor()
                            cursor.prepare("INSERT INTO MY_DATA_4HZ (BJTIME,TSAT,TACC,X_afed,Y_afed,Z_afed,RX_afed,RY_afed,RZ_afed,X_Vfed,Y_Vfed,Z_Vfed,RX_Vfed,RY_Vfed,RZ_Vfed,Ctl_state) VALUES (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13,:14,:15,:16)")
                            try:
                                cursor.executemany(None, data_4hz)
                                conn.commit()
                                cursor.close()
                                conn.close()
                            except cx_Oracle.DatabaseError as exc:
                                error, = exc.args
                            data_1hz.clear()
                            data_4hz.clear()
                        if (abs(Verr_X) <= 0.5 and abs(Verr_Y) <= 0.5 and abs(Verr_Z) <= 0.5 and abs(Verr_Rx) <= 0.5 and abs(Verr_Ry) <= 0.5 and abs(Verr_Rz) <= 0.5):
                            data_quality_count += 1
                        else:
                            data_quality_list.append(data_quality_count)
                            data_quality_count = 0
                else:#sum校验不符合要求，则不处理该包数据
                    Tacc = (input[148] * 65536 + input[149] * 256 + input[153]) / 10.0
                    Acc_Sum_error +=1
                    a = 0;
            else:
                fs.seek(-154, 1)
        else:
            fs.seek(-4,0)
        if (len(data_1hz) > 0 and len(data_1hz) < 100 ):
            conn = cx_Oracle.Connection('cge/cge_123@127.0.0.1:1521/orcl')
            # 获取操作游标
            cursor = conn.cursor()
            cursor.prepare(
                "INSERT INTO MY_DATA_1HZ (BJTIME,TSAT,TACC,Voltage_5V,Voltage_12V,Voltage_60V,x1,x2,x3,y,z1,z2,Ctl_state,Voltage_Vb,T1,T2,T3,T4,dpx,dpy,dpz,dprx,dpry,dprz,Verr_X,Verr_Y,Verr_Z,Verr_Rx,Verr_Ry,Verr_Rz) VALUES (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13,:14,:15,:16,:17,:18,:19,:20,:21,:22,:23,:24,:25,:26,:27,:28,:29,:30)")
            try:
                cursor.executemany(None, data_1hz)
                conn.commit()
                cursor.close()
            except cx_Oracle.DatabaseError as exc:
                error, = exc.args
            cursor = conn.cursor()
            cursor.prepare(
                "INSERT INTO MY_DATA_4HZ (BJTIME,TSAT,TACC,X_afed,Y_afed,Z_afed,RX_afed,RY_afed,RZ_afed,X_Vfed,Y_Vfed,Z_Vfed,RX_Vfed,RY_Vfed,RZ_Vfed,Ctl_state) VALUES (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13,:14,:15,:16)")
            try:
                cursor.executemany(None, data_4hz)
                conn.commit()
                cursor.close()
                conn.close()
            except cx_Oracle.DatabaseError as exc:
                error, = exc.args
            data_1hz.clear()
            data_4hz.clear()
finally:
    fs.close()