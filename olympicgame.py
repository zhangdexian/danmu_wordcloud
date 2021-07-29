from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import jieba
from wordcloud import WordCloud, STOPWORDS
from bilibili_api import video
import asyncio


async def fetch_data():
    v = video.Video(bvid='BV1AN411Z7wf')
    dms = await v.get_danmakus(0)
    with open("OlympicGames_dm.txt", "w+") as f:
        for dm in dms:
            f.write(dm.text + "\n")


def draw():
    ###当前文件路径
    d = path.dirname(__file__)

    # Read the whole text.
    file = open(path.join(d, 'OlympicGames_dm.txt'), encoding='utf-8').read()
    ##进行分词
    # 刚开始是分完词放进txt再打开却总是显示不出中文很奇怪
    default_mode = jieba.cut(file)
    text = "\r".join(default_mode)
    alice_mask = np.array(Image.open(path.join(d, "panda.png")))
    stopwords = set(STOPWORDS)
    wc = WordCloud(
        # 设置字体，不指定就会出现乱码,这个字体文件需要下载
        font_path=r'msyh.ttf',
        background_color="white",
        max_words=2000,
        mask=alice_mask,
        stopwords=stopwords)
    # generate word cloud
    wc.generate(text)

    # store to file
    wc.to_file(path.join(d, "panda_result.jpg"))

    # show
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.figure()
    plt.imshow(alice_mask, cmap=plt.cm.gray, interpolation='bilinear')
    plt.axis("off")
    plt.show()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(fetch_data())
    draw()
