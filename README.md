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

![sample graph](https://everpic.oss-cn-beijing.aliyuncs.com/kkba_0.8.13_s4.gif "sample graph")

## Help Document
```Shell
kkba -h
```
![enter description here](https://gitee.com/margan/pictures/raw/master/小书匠/1627449398278.png)

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
