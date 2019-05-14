#coding=utf8
import numpy as np
import fft
aa=123-12j
print(aa.real)  # output 实数部分 123.0
print(aa.imag)  # output虚数部分 -12.0


d=np.zeros((100,1),dtype=complex)
#print(d)
d[0].real = 1
d[0].imag = 2
print(d[0])


samp = np.exp(2j * np.pi * np.arange(8) / 8)
# samp[0].real = 1;
fft.ham(d,100)
print(d)