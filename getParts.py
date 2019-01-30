import cv2 as cv
import numpy as np


class GetParts(object):
    """docstring for GetParts"""

    def __init__(self, arg):
        super(GetParts, self).__init__()
        self.tl = arg[0]
        self.img = arg[1]

    def getUDMirror(self, ptsx, tl, loc):
        # 将列表中的多边形统一以一个水平轴进行对称
        for key in ptsx.keys():
            ptsx[key] = np.array(
                [[j[0], ((tl[1] + loc) + ((tl[1] + loc) - j[1]))] for j in ptsx[key]])
        return ptsx

    def getLRMirror(self, ptsx, tl, loc):
        # 将列表中的多边形统一以一个垂直轴进行对称
        for key in ptsx.keys():
            ptsx[key] = np.array(
                [[((tl[0] + loc) + ((tl[0] + loc) - j[0])), j[1]] for j in ptsx[key]])
        return ptsx

    def getZeroFlag(self, pts, img):
        # 判断这个多边形是否有任何一个顶点是在图片的像素范围之内
        flag = 0
        h = img.shape[0]
        w = img.shape[1]
        for i in pts:
            if i[0] > 0 and i[1] > 0 and i[0] < w and i[1] < h:
                flag = 1
                break
        return flag

    def getMove(self, pts, gap, hov):
        # 将列表中的多边形统一向水平或者垂直方向移动gap
        if hov:
            return np.array([[i[0], i[1] + gap] for i in pts])
        else:
            return np.array([[i[0] + gap, i[1]] for i in pts])

    def getAllTarget(self, ptsx, img, gap, hov, ptdic, offset=0):
        ''' 获取一个多边形list的一个方向（横向或者纵向）上的所有有点的拷贝
            ---------------------------                ---------------------------
            |                         |                |                         |
            |                         |                |                         |
            |                         |                |                         |
            |           |-|           |       -->      ||-||-||-||-||-||-||-||-| |
            |                         |                |                         |
            |                         |                |                         |
            |                         |                |                         |
            |                         |                |                         |
            ---------------------------                ---------------------------
        '''
        # 获取ptsx原始拷贝
        ptss = ptsx.copy()
        # 画出初始图像
        for key in ptsx.keys():
            pts = ptsx[key]
            ptdic[key].append(pts.copy())
            pts = pts.reshape(-1, 1, 2)
            img = cv.polylines(img, [pts], True, (0, 255, 0))

        # 是否改变方向，0为没有1为有
        changeFlag = 0
        # 偏移修正系数
        if not offset:
            offset_num = 0
        else:
            offset_num = 1
        while 1:
            # 整体移动ptsx
            for key in ptsx.keys():
                # print(gap - offset_num // (offset + 1))
                ptsx[key] = self.getMove(
                    ptsx[key], gap - offset_num // (offset + 1), hov)
            if offset_num > 0:
                offset_num += 1
            elif offset_num < 0:
                offset_num -= 1
            # 定义是否还有多边形存在点，0为没有1为有
            zeroFlag = 0
            # 逐个多边形进行判断并绘点
            for key in ptsx.keys():
                # 判断这个多边形是否有点
                if self.getZeroFlag(ptsx[key], img):
                    pts = ptsx[key]
                    pts = pts.reshape(-1, 1, 2)
                    img = cv.polylines(img, [pts], True, (255, 0, 0))
                    # 只要有一个多边形有点就可以继续移动
                    zeroFlag = 1
            # 绘点结束，判断是否要进行下一次移动，如果任何多边形有点则继续移动
            if zeroFlag:
                for key in ptsx.keys():
                    ptdic[key].append(ptsx[key].copy())
                continue
            # 所有多边形没点，并且还未改变过移动方向
            elif not changeFlag:
                # 改变移动方向，ptss回归原始拷贝
                changeFlag = 1
                if offset:
                    offset_num = -1
                gap = (-1) * gap
                ptsx = ptss
                continue
            # 所有多边形没点并且改变过一次移动方向
            else:
                break
        return img

    def get1LR(self, ptsx, img, hgap, vgap, ptdic, offset=0):
        ''' 获取一个多边形list左右一定gap的上下所有多边形
            ---------------------------                ---------------------------
            |                         |                |   |-|               |-| |
            |                         |                |   |-|               |-| |
            |                         |                |   |-|               |-| |
            |           |-|           |       -->      |   |-| hgap |-| hgap |-| |
            |                         |                |   |-|               |-| |
            |                         |                |   |-|               |-| |
            |                         |                |   |-|               |-| |
            |                         |                |   |-|               |-| |
            ---------------------------                ---------------------------
        '''
        ptss = ptsx.copy()
        for key in ptsx.keys():
            ptsx[key] = self.getMove(ptsx[key], hgap, 0)
        img = self.getAllTarget(ptsx, img, vgap, 1, ptdic, offset)
        ptsx = ptss
        for key in ptsx.keys():
            ptsx[key] = self.getMove(ptsx[key], (-1) * hgap, 0)
        img = self.getAllTarget(ptsx, img, vgap, 1, ptdic, offset)
        return img

    def get1UD(self, ptsx, img, hgap, vgap, ptdic, offset=0):
        ''' 获取一个多边形list上下一定gap的左右所有多边形
            --------------------------                 --------------------------
            |                        |                 |                        |
            |                        |                 ||-||-||-||-||-||-||-||-||
            |                        |                 |            vgap        |
            |           |-|          |        -->      |            |-|         |
            |                        |                 |            vgap        |
            |                        |                 ||-||-||-||-||-||-||-||-||
            |                        |                 |                        |
            |                        |                 |                        |
            --------------------------                 --------------------------
        '''
        ptss = ptsx.copy()
        for key in ptsx.keys():
            ptsx[key] = self.getMove(ptsx[key], vgap, 1)
        img = self.getAllTarget(ptsx, img, hgap, 0, ptdic, offset)
        ptsx = ptss
        for key in ptsx.keys():
            ptsx[key] = self.getMove(ptsx[key], (-1) * vgap, 1)
        img = self.getAllTarget(ptsx, img, hgap, 0, ptdic, offset)
        return img

    def getTarget(self, img, tl):
        # 必须重写此函数
        ptdic = {}
        return img, ptdic

    def getAllParts(self, showimg=0, getimg=0):
        '''
        类的调用入口
        :param showimg: 是否展示图片，调试时设置为1
        :param getimg: 是否需要返回图片
        :return:
        '''
        self.img, ptdic = self.getTarget(self.img, self.tl)
        if showimg:
            cv.namedWindow("match", cv.WINDOW_AUTOSIZE)
            cv.imshow("match", self.img)
            cv.waitKey(0)
            cv.destroyAllWindows()
        if not getimg:
            # 返回多边形dic、图片形状
            return ptdic
        else:
            return self.img
