class Complex(object):
  '''''����һ����̬����������¼��汾��'''
  version=1.0
  '''''�����������࣬���ڲ����ͳ�ʼ������'''
  def __init__(self,rel=15,img=15j):
    self.realPart=rel
    self.imagPart=img
  #��������
  def creatComplex(self):
    return self.realPart+self.imagPart
  #��ȡ�������ֲ��ֵ��鲿
  def getImg(self):
    #���鲿ת�����ַ���
    img=str(self.imagPart)
    #���ַ���������Ƭ������ȡ���ֲ���
    img=img[:-1]
    return float(img)