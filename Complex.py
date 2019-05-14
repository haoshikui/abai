class Complex(object):
  '''''创建一个静态属性用来记录类版本号'''
  version=1.0
  '''''创建个复数类，用于操作和初始化复数'''
  def __init__(self,rel=15,img=15j):
    self.realPart=rel
    self.imagPart=img
  #创建复数
  def creatComplex(self):
    return self.realPart+self.imagPart
  #获取输入数字部分的虚部
  def getImg(self):
    #把虚部转换成字符串
    img=str(self.imagPart)
    #对字符串进行切片操作获取数字部分
    img=img[:-1]
    return float(img)