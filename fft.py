# -*- coding: UTF-8 -*-
import math
import numpy as np
class fft:
    PI = np.pi
    # define MAX(a,b)    (((a) > (b)) ? (a) : (b))
    # define    PI	(4.0*atan(1.0))
    #def PSD(ref double[] sigfloat, int estsize, int slice, int wtype, double samping_rate, ref double[]mag, ref double[] F):
    def PSD(sigfloat, estsize, slice, wtype, samping_rate, mag, F):
        #** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** /
        #* 给大炮的程序中需加入这个 * /
        # ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** /
        samp = np.zeros((slice,1),dtype=complex)
        Window = 0
        ovlap=slice / 2; #默认选择重叠数据为1 / 2 nfft
        if (slice == 0):
            return;
        numav = 2 * (estsize / slice) - 1; # estsize和slice需为2的n次方
        #for (j=0; j < numav; j++):
        for j in range(0,numav):
            #for (k=0; k < slice; k++):
            for k in range(0,slice):
                index = j * (slice-ovlap) + k;
                samp[k].real = sigfloat[index];
                samp[k].imag = 0;
            if (wtype == 1):
                Window = fft.ham(samp, slice)
            # elif (wtype == 2):
            #     Window = han(ref samp, slice)
            # elif (wtype == 3):
            #     Window = triang(ref samp, slice);
            # elif (wtype == 4):
            #     Window = black(ref samp, slice);
            # elif (wtype == 5):
            #     Window = harris(ref samp, slice);
            m = math.log(slice,2)
            samp_new = fft(samp, math.pow(2,m))
            for k in range(0,slice):
                tempflt = samp[k].real * samp[k].real;
                tempflt += samp[k].imag * samp[k].imag;
                mag[k] += tempflt;


        for k in range (0, slice/2):
            d_k=k;
            d_slice=slice;
            mag[k]= mag[k] / (Window * numav) / (samping_rate / 2); #功率谱的幅值调整与matlab一致
            F[k]=d_k * (samping_rate / d_slice); #频率值

# / ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** **
# log2 - 基2求对数函数
#
# 函数返回以2为底的输入整数的对数值的整数.
#     如果对数值位于两个整数之间, 则返回较大值.
# ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** * /
# def log2(x):
#     if (x == 0):
#         return (-1); #zero is an error, return -1
#     x = x -1 #*get the max index, x - 1 * /
#     for (mask = 1, i = 0;; mask *= 2, i++) {
#     if (x == 0)
#         return (i); / * return log2 if allzero * /
#     x = x & (~mask); / *AND
#     off
#     a
#     bit * /
#     }
#     }
# / ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** *
# ham - Hamming
# 窗函数
#
# 输入参数:
# COMPLEX * x: 输入复数数组指针;
# int n: 输入数组长度.
# 输出参数:
# 加窗后结果放在输入数组中返回,
# ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** * /

def ham(x, n):
    # int i;
    # double ham, factor,
    Window1 = 0;
    factor = 8.0 * math.atan(1.0) / (n - 1);
    for i in range(0,n):
        ham = 0.54 - 0.46 * math.cos(factor * i);
        x[i].real = x[i].real * ham;
        x[i].imag = x[i].imag * ham;
        Window1 += ham * ham;
    return Window1;

# / ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** *
# han - Hanning 窗函数
#
# 输入参数:
# COMPLEX * x: 输入复数数组指针;
# int n: 输入数组长度.
#     输出参数:
# 加窗后结果放在输入数组中返回,
# 无输出参数.
# ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** * /
#
# private
# static
# double
# han(ref
# COMPLEX[]
# x, int
# n)
# {
# int
# i;
# double
# factor, han, Window2 = 0;;
#
# factor = 8.0 * Math.Atan(1.0) / (n - 1);
# for (i = 0; i < n; i++){
#     han = 0.5 - 0.5 * Math.Cos(factor * i);
# x[i].real *= han;
# x[i].imag *= han;
# Window2 += han * han;
# }
# return Window2;
# }
#
# / ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** *
# triang - triangle
# 窗函数
#
# 输入参数:
# COMPLEX * x: 输入复数数组指针;
# int
# n: 输入数组长度.
#     输出参数:
# 加窗后结果放在输入数组中返回,
# 无输出参数.
#
#     void
# triang(COMPLEX *, int
# n)
# ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** * /
#
# private
# static
# double
# triang(ref
# COMPLEX[]
# x, int
# n)
# {
# int
# i;
# double
# tri, a, Window3 = 0;
# a = 2.0 / (n - 1);
#
# for (i = 0; i <= (n-1) / 2 ; i++) {
# tri = i * a;
# x[i].real *= tri;
# x[i].imag *= tri;
# Window3 += tri * tri;
# }
# for (; i < n; i++) {
#     tri = 2.0 - i * a;
# x[i].real *= tri;
# x[i].imag *= tri;
# Window3 += tri * tri;
# }
# return Window3;
# }
#
# / ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** *
# black - Blackman
# 窗函数
#
# 输入参数:
# COMPLEX * x: 输入复数数组指针;
# int
# n: 输入数组长度.
#     输出参数:
# 加窗后结果放在输入数组中返回,
# 无输出参数.
#
#     void
# black(COMPLEX * x, int
# n)
# ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** * /
#
# private
# static
# double
# black(ref
# COMPLEX[]
# x, int
# n)
# {
# int
# i;
# double
# black, factor, Window4 = 0;
#
# factor = 8.0 * Math.Atan(1.0) / (n - 1);
# for (i=0; i < n; ++i){
#     black = 0.42 - 0.5 * Math.Cos(factor * i) + 0.08 * Math.Cos(2 * factor * i);
# x[i].real *= black;
# x[i].imag *= black;
# Window4 += black * black;
# }
# return Window4;
# }
#
# / ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** *
# harris - 4
# term
# Blackman - Harris
# 窗函数
#
# 输入参数:
# COMPLEX * x: 输入复数数组指针;
# int
# n: 输入数组长度.
#     输出参数:
# 加窗后结果放在输入数组中返回,
# 无输出参数.
#
#     void
# harris(COMPLEX * x, int
# n)
# ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** * /
#
# private
# static
# double
# harris(ref
# COMPLEX[]
# x, int
# n)
# {
# int
# i;
# double
# harris, factor, arg, Window5 = 0;
#
# factor = 8.0 * Math.Atan(1.0) / n;
# for (i=0; i < n; ++i){
#     arg = factor * i;
# harris = 0.35875 - 0.48829 * Math.Cos(arg) + 0.14128 * Math.Cos(2 * arg)
# - 0.01168 * Math.Cos(3 * arg);
# x[i].real *= harris;
# x[i].imag *= harris;
# Window5 += arg * arg;
# }
# return Window5;
# }
# }
# }



