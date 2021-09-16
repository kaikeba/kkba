# KKBA
![](https://img.shields.io/badge/python-3.6-brightgreen)
## Intruoduction
A low-code tool that generates python crawler code based on curl or url

## Requirement
```shell
Python >= 3.6
```

## Install
```Shell
pip install kkba
```
## Usage

Copy the curl command or url from the browser, without pasting, execute the command directly:  kkba [options]

```shell
kkba [options]

# After the command execution, the crawler directory will be generated in the current directory (including the crawler articles and readme files).

```

## Example
[开课吧传送门](https://www.kaikeba.com/open/)
<br/>
```shell
# 1. Copy curl or url
# 2. excute commands
kkba -F
```

![sample graph](https://everpic.oss-cn-beijing.aliyuncs.com/kkba-s4-ezgif.com-gif-maker.gif "sample graph")

## Help Document
```Shell
kkba -h
```

```text
爬虫生成器

usage: kkba [options]

optional arguments:
  -F,               推荐: 将粘贴板curl或者url，生成feapder异步爬虫代码，相当于scrapy的用法
  -s                将粘贴板curl或者url，生成scrapy单文件项目
  -f,               将粘贴板curl或者url，生成feapder同步爬虫代码，相当于requests的用法
  -r,               将粘贴板curl或者url，生成requests爬虫代码
  -h, --help        帮助文档
  -v, --version     查看版本

```
### Genrates feapder spider code
```shell
# install fepader
pip install feapder

# generates feapder spiders code
kkba -F
```

### Generates scrapy single file code
```shell
# install scrapy
pip install scrapy

# generates scrapy single spiders code
kkba -F
```

## Thanks
[curl2pyreqs](https://github.com/knightz1224/curl2pyreqs) 令狐 向娜
