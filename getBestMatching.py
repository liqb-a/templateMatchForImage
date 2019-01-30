import cv2 as cv


class GetBestMatching(object):
    """docstring for GetBestMatching"""

    def __init__(self, modelPath, threshold):
        super(GetBestMatching, self).__init__()
        self.m = self.getModel(modelPath)
        self.threshold = threshold

    def gaussianThreshold(self, img, showimg=0):
        # 图片进行二值化
        gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
        binary = cv.adaptiveThreshold(
            gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 15, 10)
        if showimg:
            cv.namedWindow('GAUSSIAN', cv.WINDOW_AUTOSIZE)
            cv.imshow('GAUSSIAN', binary)
        return binary

    def getModel(self, path):
        # 获取模板
        m = cv.imread(path, cv.IMREAD_GRAYSCALE)
        return m

    def getMore(self, img, m):
        # 对目标图片进行模板的匹配，返回最大值与位置
        res0 = cv.matchTemplate(img, m, cv.TM_CCOEFF_NORMED)
        min_val0, max_val0, min_loc0, max_loc0 = cv.minMaxLoc(res0)
        return max_val0, max_loc0

    def resizePic(self, img):
        ''' resize图片和返回最大匹配
            如果需要改变图片分辨率需要继承并重写此函数，如：
            if img.shape[:2] == (432, 576):
                img = cv.resize(img, (558, 421), cv.INTER_CUBIC)
            elif img.shape[:2] == (768, 1024):
                img = np.rot90(img)
                img = np.rot90(img)
                img = np.rot90(img)
                img = cv.resize(img, (634, 846), cv.INTER_CUBIC)
        '''
        return img

    def getBest(self, img, m):
        # 输出最终模板匹配值的结果并返回
        img = self.resizePic(img)
        max_val, max_loc = self.getMore(img, m)
        print('    END:%f' % (max_val))
        if max_val >= self.threshold:
            return max_val, max_loc, img
        else:
            return 0, 0, img

    def getWhich(self, img, m):
        # 获取目标图片的最好匹配val和位置loc
        max_val, max_loc, img = self.getBest(img, m)
        if max_val == 0:
            return 0, 0, img
        return max_val, max_loc, img

    def getWhere(self, img, showimg=0):
        '''

        :param img: 输入图片路径
        :param showimg: 是否展示图片（调试时需要设置为1）
        :return: 返回最佳匹配点，以及图片（resize后的）或者 0 和 原图img
        '''
        # 1、保存原始未处理图像便于画图
        img = cv.imread(img)
        c_img = img.copy()

        # 2、或者模板并对图像进行二值化处理
        c_img = self.gaussianThreshold(c_img)
        print('进行匹配：')

        # 3、获取最好匹配位置
        max_val, max_loc, c_img = self.getWhich(c_img, self.m)
        if max_val == 0:  # return 没有一个大于0.75的匹配
            print('Error')
            if showimg:
                cv.namedWindow("match", cv.WINDOW_AUTOSIZE)
                cv.imshow("match", img)
                cv.waitKey(0)
                cv.destroyAllWindows()
            return [0, img]

        # 4、如果二值化的图片有过拉伸处理这里对要进行画图的原图也进行同样的处理
        img = self.resizePic(img)

        # 5、获取最佳位置以及模板大小，并把最佳匹配在图中画出来
        th, tw = self.m.shape[:2]
        tl = max_loc
        br = (tl[0] + tw, tl[1] + th)
        cv.rectangle(img, tl, br, (0, 0, 255), 1)

        # 6、返回模板位置以及resize后的图片便于展示
        if showimg:
            cv.namedWindow("match", cv.WINDOW_AUTOSIZE)
            cv.imshow("match", img)
            cv.waitKey(0)
            cv.destroyAllWindows()
        return [tl, img]
