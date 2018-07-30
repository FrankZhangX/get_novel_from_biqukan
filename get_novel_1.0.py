import requests
from bs4 import BeautifulSoup
import sys

class get_novel(object):
	'''获取小说类'''
	def __init__(self):
		self.server = 'http://www.biqukan.com/'
		self.target = 'http://www.biqukan.com/50_50096/'
		self.titles = []		#章节标题
		self.urls = []			#章节链接
		self.nums = 0			#章节数
		

	def get_chapter(self, target):
		#获取章节内容
		#target = 'http://www.biqukan.com/50_50096/18520412.html'
		req = requests.get(url = target)	#get方式获取html
		#print(req.text)
		html = req.text
		bs = BeautifulSoup(html, 'lxml')
		texts = bs.find_all('div', class_='showtxt')	#返回列表，长度为1
		#print(texts)
		chapter = texts[0].text.replace('&amp;1t;/p&gt;<br/> <br/>', '\n\n').replace('&1t;/p>','\n\n').replace('&amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;1t;/p&amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;gt;', '\n')	#返回字符串
		#print(chapter)
		'''
		with open('novel.txt', 'w', encoding='utf-8') as f:
			f.writelines(str(chapter))
		'''
		return str(chapter)


	def get_catalogue(self):
		#获取目录
		#target = 'http://www.biqukan.com/50_50096/'
		req = requests.get(url = self.target)
		html = req.text
		div_bs = BeautifulSoup(html, 'lxml')
		texts = div_bs.find_all('div', class_='listmain')
		a_bs = BeautifulSoup(''.join(str(texts[0]).split('\n')[15:-1]), 'lxml')	#去除前面最新章节
		catalogue = a_bs.find_all('a')
		'''
		#显示目录
		for i in catalogue:
			print(i.string)
		'''
		'''
		with open('catalogue.txt', 'w', encoding='utf-8') as f:
			f.writelines(str(i.string)+'\n' for i in catalogue)
		'''
		self.nums = len(catalogue)
		#统计目录及对应链接
		for title in catalogue:
			self.titles.append(title.string)
			self.urls.append(self.server[:-1] + title.attrs['href'])


	def writer(self, title, text, path):	#title：章节标题，text：章节内容，path：保存路径
		with open(path, 'a', encoding='utf-8') as f:
			f.write(title + '\n\n')
			f.writelines(text)
			f.write('\n\n\n')


if __name__ == '__main__':
	novel = get_novel()
	novel.get_catalogue()
	print('正在下载《三国演义》：')
	for i in range(novel.nums):
		novel.writer(novel.titles[i], novel.get_chapter(novel.urls[i]), '《三国演义》.txt')
		sys.stdout.write('	已下载：%.2f%%'	%	float(i/novel.nums*100) + '\r')
		sys.stdout.flush()
	print('	已下载：100%	')
	print('		下载完成！')
