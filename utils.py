import cv2 as cv
import numpy as np
import os
import datetime
from getBestMatching import GetBestMatching
from getParts import GetParts
from defectComparison import DefectComparison


def getJPG(path, li=0):
    # 返回一个文件夹下所有jpg文件名，li==1代表将地址和文件名拆开返回
    list_name = []
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if file[-3:].lower() == 'jpg' and not os.path.isdir(file_path):
            if not li:
                list_name.append(file_path)
            else:
                list_name.append([path, file])
        if os.path.isdir(file_path):
            list_name += getJPG(file_path, li)
    return list_name


class GetBestMatchinger(GetBestMatching):
    """
    docstring for GetBestMatchinger
        这是一个用于获取模板所对应的最佳位置的类
        需要重写的函数有resizePic：用于多种分辨率下的图形变化使图片一致
        如果不需要变换删掉底下的重写就行，原本类是默认不变的
        这里的重写适用于零件5300
    """

    def __init__(self, modelPath, threshold):
        super(GetBestMatchinger, self).__init__(modelPath, threshold)

    def resizePic(self, img):
        ''' resize图片和返回最大匹配
            如果需要改变图片分辨率需要继承并重写此函数，如：
        '''
        if img.shape[:2] == (432, 576):
            img = cv.resize(img, (558, 421), cv.INTER_CUBIC)
        elif img.shape[:2] == (768, 1024):
            img = np.rot90(img)
            img = np.rot90(img)
            img = np.rot90(img)
            img = cv.resize(img, (634, 846), cv.INTER_CUBIC)
        return img


class GetPartser(GetParts):
    """
    docstring for GetPartser
        这是一个用于获得每一个零件位置的类
        需要修改的只有getTarget：用于描点的函数
        具体定义请看下方，在这里重写，这里原本的适用于5300
    """

    def __init__(self, arg):
        super(GetPartser, self).__init__(arg)

    def getTarget(self, img, tl):
        '''
        此函数一共分为三个功能：
            1、定义piex长宽
            1、从模板匹配的最优点找到piex的起始点
            2、标记各个零件的坐标画多边形
            3、从一组零件变化画出其他所有零件
        '''

        '''
         1、ptsx 为所画组零件的list
            ptdic 用于放所有的零件
            hgap 为piex的左右宽度
            vgap 为piex的上下高度
            offset为是否进行偏移回归，0为不回归
                否则为每 (offset+1) 个piex回归1个像素
        '''
        ptsx = {}
        ptdic = {}
        hgap = 454
        vgap = 152
        offset = 0

        # 2、从模板匹配的最优点找到piex的起始点
        tl = [tl[0] + 37, tl[1] + 23]

        # 3、标记各个零件的坐标画多边形
        # M1-1
        ptdic['M1-1'] = []
        ptsx['M1-1'] = np.array([[tl[0] + 19, tl[1] + 174], [tl[0] + 19, tl[1] + 140],
                                 [tl[0] + 27, tl[1] + 131], [tl[0] + 40, tl[1] + 131],
                                 [tl[0] + 47, tl[1] + 140], [tl[0] + 47, tl[1] + 154],
                                 [tl[0] + 458, tl[1] +
                                     154], [tl[0] + 458, tl[1] + 164],
                                 [tl[0] + 47, tl[1] + 164], [tl[0] + 47, tl[1] + 174]])

        # M1-2
        ptdic['M1-2'] = []
        ptsx['M1-2'] = np.array([[tl[0] - 23, tl[1] + 78], [tl[0] - 23, tl[1] + 85],
                                 [tl[0] + 36, tl[1] + 85], [tl[0] + 36, tl[1] + 78]])

        # M1-3
        ptdic['M1-3'] = []
        ptsx['M1-3'] = np.array([[tl[0] - 3, tl[1] + 110], [tl[0] - 3, tl[1] + 117],
                                 [tl[0] + 19, tl[1] + 117], [tl[0] + 19, tl[1] + 110]])

        # M2-1
        ptdic['M2-1'] = []
        ptsx['M2-1'] = np.array([[tl[0] + 28, tl[1] + 137], [tl[0] + 23, tl[1] + 143],
                                 [tl[0] + 22, tl[1] + 138], [tl[0] + 15, tl[1] + 138],
                                 [tl[0] + 15, tl[1] + 153], [tl[0] + 1, tl[1] + 153],
                                 [tl[0] + 1, tl[1] + 17], [tl[0] + 15, tl[1] + 17],
                                 [tl[0] + 15, tl[1] + 130], [tl[0] + 24, tl[1] + 130]])

        # M2-2
        ptdic['M2-2'] = []
        ptsx['M2-2'] = np.array([[tl[0] + 23, tl[1] + 167], [tl[0] + 28, tl[1] + 167],
                                 [tl[0] + 28, tl[1] + 144], [tl[0] + 31, tl[1] + 141],
                                 [tl[0] + 34, tl[1] + 141], [tl[0] + 38, tl[1] + 144],
                                 [tl[0] + 38, tl[1] + 167], [tl[0] + 43, tl[1] + 167],
                                 [tl[0] + 43, tl[1] + 143], [tl[0] + 38, tl[1] + 137],
                                 [tl[0] + 28, tl[1] + 137], [tl[0] + 23, tl[1] + 143]])

        # M2-3
        ptdic['M2-3'] = []
        ptsx['M2-3'] = np.array([[tl[0] + 31, tl[1] + 144], [tl[0] + 35, tl[1] + 144],
                                 [tl[0] + 35, tl[1] + 179], [tl[0] + 39, tl[1] + 179],
                                 [tl[0] + 39, tl[1] + 193], [tl[0] + 24, tl[1] + 193],
                                 [tl[0] + 24, tl[1] + 179], [tl[0] + 31, tl[1] + 179]])

        # Main
        ptdic['Main'] = []
        ptsx['Main'] = np.array([[tl[0], tl[1]], [tl[0], tl[1] + 152],
                                 [tl[0] + 454, tl[1] + 152], [tl[0] + 454, tl[1]]])

        # add
        ptdic['add'] = []
        ptsx['add'] = np.array([[tl[0] - 29, tl[1] + 83], [tl[0] - 29, tl[1] + 155],
                                [tl[0] + 53, tl[1] + 155], [tl[0] + 53, tl[1] + 83]])

        # 4、从一组零件变化画出其他所有零件
        ptss = ptsx.copy()
        img = self.getAllTarget(ptsx, img, hgap, 0, ptdic, offset)

        ptsx = ptss.copy()
        img = self.get1UD(ptsx, img, hgap, 2 * vgap, ptdic, offset)

        ptsx = ptss.copy()
        img = self.get1UD(ptsx, img, hgap, 4 * vgap, ptdic, offset)

        ptsx = ptss.copy()
        img = self.get1UD(ptsx, img, hgap, 6 * vgap, ptdic, offset)

        ptsx = ptss.copy()
        img = self.get1UD(ptsx, img, hgap, 8 * vgap, ptdic, offset)

        ptsx = self.getLRMirror(ptss, tl, 234)
        ptss = ptsx.copy()

        img = self.get1UD(ptsx, img, hgap, vgap, ptdic, offset)

        ptsx = ptss.copy()
        img = self.get1UD(ptsx, img, hgap, 3 * vgap, ptdic, offset)

        ptsx = ptss.copy()
        img = self.get1UD(ptsx, img, hgap, 5 * vgap, ptdic, offset)

        ptsx = ptss.copy()
        img = self.get1UD(ptsx, img, hgap, 7 * vgap, ptdic, offset)

        return img, ptdic


class DefectComparisoner(DefectComparison):
    """
    docstring for DefectComparisoner：
        这是一个用于故障对比的类
        这个类可能需要修改的部分是：
            getReturn：不同的零件要求输出结果不同
            getQOut：其中的M1，M2是list需要改变
        可以直接在这里重写这两个函数就可以直接使用，
        这里原本的这两个函数适用于零件5300
    """

    def __init__(self, ptdic, shape, picpath, resizedef):
        super(DefectComparisoner, self).__init__(
            ptdic, shape, picpath, resizedef)


def onepictureparts(modelPath, picPath, threshold):
    # 获取一张图片的所有零件匹配情况并画图
    start = datetime.datetime.now()
    matcher = GetBestMatchinger(modelPath, threshold)
    res = matcher.getWhere(picPath, showimg=0)
    end = datetime.datetime.now()
    print('    得到最佳匹配所花时间%fs:' %
          ((end - start).seconds + (((end - start).microseconds) / 1e6)))
    if res[0] == 0:
        print('GG')
        return
    getter = GetPartser(res)
    getter.getAllParts(showimg=1)


def onepictureout(modelPath, picPath, target, threshold):
    # 获取一张图片的所有零件匹配情况并画图，并与预制的故障图片或者np多边形进行比对输出结果
    start = datetime.datetime.now()
    matcher = GetBestMatchinger(modelPath, threshold)
    res = matcher.getWhere(picPath, showimg=0)
    end = datetime.datetime.now()
    print('    得到最佳匹配所花时间%fs:' %
          ((end - start).seconds + (((end - start).microseconds) / 1e6)))
    if res[0] == 0:
        print('GG')
        return
    getter = GetPartser(res)
    ptdic = getter.getAllParts(showimg=1)
    start = datetime.datetime.now()
    if isinstance(target, str):
        comparisoner = DefectComparisoner(
            ptdic, res[1].shape, target, matcher.resizePic)
        output = comparisoner.getQOut()
    elif isinstance(target, np.ndarray):
        comparisoner = DefectComparisoner(
            ptdic, res[1].shape, '', matcher.resizePic)
        output = comparisoner.getQOut(target)
    end = datetime.datetime.now()
    print('    进行故障比对所花时间%fs:' %
          ((end - start).seconds + (((end - start).microseconds) / 1e6)))
    print(output)


def pathparts(path, modelPath, threshold, writepath=0):
    # 获取目标位置下的所有图片的所有零件匹配情况并画图，可选择只是看或者还是输出
    start_ = datetime.datetime.now()
    s = 0
    for i in getJPG(path, li=1):
        s += 1
        start = datetime.datetime.now()
        matcher = GetBestMatchinger(modelPath, threshold)
        res = matcher.getWhere(os.path.join(i[0], i[1]), showimg=0)
        end = datetime.datetime.now()
        print('    得到最佳匹配所花时间%fs:' %
              ((end - start).seconds + (((end - start).microseconds) / 1e6)))
        if res[0] == 0:
            print('GG')
            continue
        start = datetime.datetime.now()
        getter = GetPartser(res)
        if not writepath:
            getter.getAllParts(showimg=1)
            end = datetime.datetime.now()
        else:
            img = getter.getAllParts(showimg=0, getimg=1)
            end = datetime.datetime.now()
            print('    获取所有零件位置所花时间%fs:' %
                  ((end - start).seconds + (((end - start).microseconds) / 1e6)))
            name = '%s%s' % (writepath, i[1])
            cv.imwrite(name, img)
    end_ = datetime.datetime.now()
    if writepath:
        print('    平均获取每件零件位置所花时间%fs:' %
              (((end_ - start_).seconds + (((end_ - start_).microseconds) / 1e6)) / s))


def pathout(path, modelPath, target, threshold):
    # 获取目标位置下的所有图片的所有零件匹配情况并画图，并与预制的故障图片或者np多边形进行比对输出结果
    start_ = datetime.datetime.now()
    s = 0
    for i in getJPG(path):
        s += 1
        start = datetime.datetime.now()
        matcher = GetBestMatchinger(modelPath, threshold)
        res = matcher.getWhere(i, showimg=0)
        end = datetime.datetime.now()
        print('    得到最佳匹配所花时间%fs:' %
              ((end - start).seconds + (((end - start).microseconds) / 1e6)))
        if res[0] == 0:
            print('GG')
            continue
        start = datetime.datetime.now()
        getter = GetPartser(res)
        ptdic = getter.getAllParts(showimg=0)
        end = datetime.datetime.now()
        print('    获取所有零件位置所花时间%fs:' %
              ((end - start).seconds + (((end - start).microseconds) / 1e6)))
        start = datetime.datetime.now()
        if isinstance(target, str):
            comparisoner = DefectComparisoner(
                ptdic, res[1].shape, target, matcher.resizePic)
            output = comparisoner.getQOut()
        elif isinstance(target, np.ndarray):
            comparisoner = DefectComparisoner(
                ptdic, res[1].shape, '', matcher.resizePic)
            output = comparisoner.getQOut(target)
        end = datetime.datetime.now()
        print('    进行故障比对所花时间%fs:' %
              ((end - start).seconds + (((end - start).microseconds) / 1e6)))
        print(output)
    end_ = datetime.datetime.now()
    print('    平均获取每件零件位置并进行故障对比所花时间%fs:' %
          (((end_ - start_).seconds + (((end_ - start_).microseconds) / 1e6)) / s))
