# -*- coding: utf-8 -*-
import os
import time
import codecs
import jieba
import csv
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

from collections import defaultdict, Counter
from imageio import imread
from wordcloud import WordCloud
from .app import app
from .utils import is_number, zip_files


jieba.load_userdict(app.config['STOPWORDS_FILE'])  # 导入用户自定义词典用于jieba分词


class SmartWordCloud:
    def __init__(self, text, filename=None):
        self.text = self._normalize_text(text)
        self.filename = filename
        self.word_counts = self._optimize_segments()

    @staticmethod
    def _normalize_text(text):
        if os.path.isfile(text):  # 文件类型
            with codecs.open(text, 'r', encoding='utf-8') as text:
                text_lines = text.readlines()
        elif isinstance(text, list):
            text_lines = test
        elif isinstance(text, str):
            text_lines = [text]
        else:
            raise Exception("Not support to normalize the type '%s'" % type(text))

        return text_lines

    def _get_counts(self) -> dict:
        """
        获取所有分词的词频统计
        """
        word_counts = defaultdict(int)

        for line in self.text:
            line = line.replace('\n', '')

            words = jieba.cut(line, cut_all=False)

            for word in words:
                if word != '':
                    word_counts[word] += 1

        return word_counts  # {'词a': 100,'词b': 90,'词c':80}

    def _optimize_segments(self):
        """
        删除分词结果中的单个字/符号/数字
        """
        counts = self._get_counts()
        purified = {word: counts[word] for word in counts if not (len(word) == 1 or is_number(word))}

        return purified

    def save_counts(self):
        """
        将分词词频统计结果保存到excel文件
        """
        file_name = '词频统计' + '_' + str(int(time.time())) + '.csv'
        file_path = os.path.join(os.path.abspath(app.config['SAVED_DIR']), file_name)

        n_words = Counter(self.word_counts).most_common()
        with open(file_path, 'w', encoding='utf-8-sig') as f:
            writer = csv.writer(f, )
            writer.writerow(['高频词', '词频'])
            for words in n_words:
                writer.writerow(words)

        return file_path

    def save_clouds(self):
        """
        生成词云图
        """
        print('hello', os.path.abspath(app.config['IMAGE_FILE']))
        coloring = imread(os.path.abspath(app.config['IMAGE_FILE']))
        wc = WordCloud(background_color="black",  # 背景颜色
                       mask=coloring,  # 设置背景图片
                       font_path=app.config['FONT_FILE'],  # 兼容中文字体
                       width=400,
                       height=200,
                       margin=2,
                       max_font_size=120,  # 字体最大值
                       max_words=60,  # 词云中最多显示的词量
                       prefer_horizontal=1)  # 水平方向的词的数量与垂直方向的词的数量的比例

        # 计算好词频后使用generate_from_frequencies函数生成词云
        wc.generate_from_frequencies(self.word_counts)
        # 生成图片
        plt.imshow(wc)
        plt.axis("off")
        # 绘制词云
        plt.figure()
        # 保存词云
        file_name = str(int(time.time()))+'.png'
        file_path = os.path.join(os.path.abspath(app.config['SAVED_DIR']), file_name)
        wc.to_file(file_path)

        return file_path

    def save(self):
        csv_path = self.save_counts()
        cloud_path = self.save_clouds()
        zip_path = zip_files([csv_path, cloud_path])

        return zip_path
