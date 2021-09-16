import getopt
import os
import shutil
import sys
from urllib.parse import urlencode

import pyperclip

from .parse_curl import *


def key2hump(key):
    """
    try to capitalize the underscore
    :param key:
    :type key:
    :return:
    :rtype:
    """
    return key.title().replace("_", "")


def parse_curlstring(filestring):
    """
    curl to requests code
    :param filestring:
    :type filestring:
    :return:
    :rtype:
    """
    curl_cmd = parse_curl_command(filestring)
    output = """# -*- coding: utf-8 -*-
\"\"\"
kkba generates this file
kkba doucment: https://github.com/kaikeba/kkba
\"\"\"
import requests\n
"""
    req = ['response = requests.{}("{}"'.format(curl_cmd.method, curl_cmd.url)]
    if curl_cmd.params:
        output += "params = {}\n\n".format(prettier_tuple(curl_cmd.params))
        req.append('params=params')
    if curl_cmd.data:
        if isinstance(curl_cmd.data, dict):
            output += "data = {}\n\n".format(prettier_dict(curl_cmd.data))
        elif isinstance(curl_cmd.data, str):
            output += "data = '{}'\n\n".format(curl_cmd.data)
        else:
            output = 'from requests_toolbelt import MultipartEncoder\n' + output
            output += "data = {}\n\n".format(format_multi(curl_cmd.data))
        req.append('data=data')
    if curl_cmd.headers:
        output += "headers = {}\n\n".format(prettier_dict(curl_cmd.headers))
        req.append('headers=headers')
    if curl_cmd.cookies:
        output += "cookies = {}\n\n".format(prettier_dict(curl_cmd.cookies))
        req.append('cookies=cookies')
    if curl_cmd.insecure:
        req.append('verify=False')
    output += ', '.join(req) + ')\n\n'
    output += 'print(response.text)\n\n'
    url = curl_cmd.url
    filename = re.findall('://(www\.)?(.*?)\.', url)
    filename = filename[0]
    if filename:
        filename = filename[1].replace('.', '_').replace('www_', '')
    else:
        filename = 'test.py'

    filename = filename + '.py'
    return output, filename


def parse_curl_string_feapder(filestring):
    """
    curl to feapder synchronize code
    :param filestring:
    :type filestring:
    :return:
    :rtype:
    """
    curl_cmd = parse_curl_command(filestring)
    output = """# -*- coding: utf-8 -*-
\"\"\"
kkba generates this file
feapder document： http://boris.org.cn/feapder/#/README
kkba doucment: https://github.com/kaikeba/kkba
\"\"\"

from feapder import Request
import feapder.setting as setting

setting.LOG_LEVEL = 'ERROR'


def start():
"""
    req = ['    request = Request(url="{}"'.format(curl_cmd.url)]

    if curl_cmd.params:
        params_str = '(\n' + " " * 8 + ("," + "\n" + " " * 8).join(
            str(i) for i in curl_cmd.params) + ',\n    )'
        output += "    params = {}\n\n".format(params_str)
        req.append('params=params')
    if curl_cmd.data:
        if isinstance(curl_cmd.data, dict):
            output += "    data = {}\n\n".format(prettier_dict(curl_cmd.data))
        elif isinstance(curl_cmd.data, str):
            output += "    data = '{}'\n\n".format(curl_cmd.data)
        else:
            output = 'from requests_toolbelt import MultipartEncoder\n' + output
            output += "    data = {}\n\n".format(format_multi(curl_cmd.data))
        req.append('data=data')
    if curl_cmd.headers:
        output += "    headers = {}\n\n".format(prettier_dict(curl_cmd.headers))
        req.append('headers=headers')
    if curl_cmd.cookies:
        output += "    cookies = {}\n\n".format(prettier_dict(curl_cmd.cookies))
        req.append('cookies=cookies')
    if curl_cmd.insecure:
        req.append('verify=False')
    output += ', '.join(req) + ')\n'
    output += """
    response = request.get_response()
    if response.ok:
        return response
    else:
        return 'error'


if __name__ == '__main__':
    res = start()
    print(res.text)
"""
    url = curl_cmd.url
    filename = re.findall('://(www\.)?(.*?)\.', url)
    filename = filename[0]
    if filename:
        filename = filename[1].replace('.', '_').replace('www_', '')
    else:
        filename = 'test.py'
    filename = filename + '.py'
    return output, filename


def fetch_curl(curl_args):
    """
    parse and fetch curl request
    :param curl_args:
    [url, '-H', 'xxx', '-H', 'xxx', '--data-binary', '{"xxx":"xxx"}', '--compressed']
    :return:
    """
    url = curl_args[0]
    curl_args.pop(0)

    headers = {}
    data = {}
    for i in range(0, len(curl_args), 2):
        if curl_args[i] == "-H":
            regex = "([^:\s]*)[:|\s]*(.*)"
            result = re.search(regex, curl_args[i + 1], re.S).groups()
            if result[0] in headers:
                headers[result[0]] = headers[result[0]] + "&" + result[1]
            else:
                headers[result[0]] = result[1].strip()

        elif curl_args[i] == "--data-binary":
            data = json.loads(curl_args[i + 1])

    return url, data, headers


def generate_feapder_air_spider(clip_curl):
    """
    curl to feapder AirSpider code
    :param clip_curl:
    :type clip_curl:
    :return:
    :rtype:
    """
    curl_cmd = parse_curl_command(clip_curl)
    template_path = os.path.abspath(
        os.path.join(__file__, "../", 'feapder_air_spider_template.tmpl')
    )
    with open(template_path, 'r', encoding='utf-8') as file:
        file_str = file.read()
    req = ['        yield feapder.Request(url="{}"'.format(curl_cmd.url)]
    output = ''
    output_p = ''
    if curl_cmd.params:
        params_str = '(\n' + " " * 12 + ("," + "\n" + " " * 12).join(
            str(i) for i in curl_cmd.params) + ',\n        )'
        output += "        params = {}\n\n".format(params_str)
        req.append('params=params')
    if curl_cmd.data:
        if isinstance(curl_cmd.data, dict):
            output += "        data = {}\n\n".format(prettier_dict(curl_cmd.data, indent=8))
        elif isinstance(curl_cmd.data, str):
            output += "        data = '{}'\n\n".format(curl_cmd.data)
        else:
            output = 'from requests_toolbelt import MultipartEncoder\n' + output
            output += "    data = {}\n\n".format(format_multi(curl_cmd.data, indent=8))
        req.append('data=data')
    if curl_cmd.headers:
        output_p += "        request.headers = {}\n\n".format(prettier_dict(curl_cmd.headers, indent=8))
    if curl_cmd.cookies:
        output_p += "        request.cookies = {}\n".format(prettier_dict(curl_cmd.cookies, indent=8))
    if curl_cmd.insecure:
        req.append('verify=False')
    output += ', '.join(req) + ')\n'
    file_str = file_str.replace('${params}', output)
    file_str = file_str.replace('${request}', output_p)
    url = curl_cmd.url
    filename = re.findall('://(www\.)?(.*?)\.', url)
    filename = filename[0]
    if filename:
        filename = filename[1].replace('.', '_').replace('www_', '')
    else:
        filename = 'kaikeba'
    if filename.islower():
        spider_name = key2hump(filename)
    file_str = file_str.replace("${spider_name}", spider_name).replace("${spider_name_l}", filename)
    filename = filename + '.py'
    return file_str, filename


def generate_single_scrapy(clip_curl):
    """
    curl to scrapy single file code
    :param clip_curl:
    :type clip_curl:
    :return:
    :rtype:
    """
    curl_cmd = parse_curl_command(clip_curl)
    template_path = os.path.abspath(
        os.path.join(__file__, "../", 'scrapy_template.tmpl')
    )
    with open(template_path, 'r', encoding='utf-8') as file:
        file_str = file.read()
    req = ['        yield scrapy.Request(url="{}"'.format(curl_cmd.url)]
    output = ''
    if curl_cmd.params:
        url_ = urlencode(curl_cmd.params)
        url__ = curl_cmd.url + '?' + url_
        req = ['        yield scrapy.Request(url="{}"'.format(url__)]
    if curl_cmd.data:
        if isinstance(curl_cmd.data, dict):
            output += "        data = {}\n\n".format(prettier_dict(curl_cmd.data, indent=8))
            req[0] = req[0].replace('Request', 'FormRequest')
            req.append('formdata=data')
        elif isinstance(curl_cmd.data, str):
            output += "        data = '{}'\n\n".format(curl_cmd.data)
            req.append('method="POST", body=data')
        else:
            output = 'from requests_toolbelt import MultipartEncoder\n' + output
            output += "    data = {}\n\n".format(format_multi(curl_cmd.data, indent=8))
            req[0] = req[0].replace('Request', 'FormRequest')
            req.append('formdata=data')
    if curl_cmd.headers:
        output += "        headers = {}\n\n".format(prettier_dict(curl_cmd.headers, indent=8))
        req.append('headers=headers')
    if curl_cmd.cookies:
        output += "        cookies = {}\n".format(prettier_dict(curl_cmd.cookies, indent=8))
        req.append('cookies=cookies')
    if curl_cmd.insecure:
        req.append('verify=False')
    output += ', '.join(req) + ', callback=self.parse)\n'
    file_str = file_str.replace('${params}', output)
    url = curl_cmd.url

    filename = re.findall('://(www\.)?(.*?)\.', url)
    filename = filename[0]
    if filename:
        filename = filename[1].replace('.', '_').replace('www_', '')
    else:
        filename = 'kaikeba'
    if filename.islower():
        spider_name = key2hump(filename)
    file_str = file_str.replace("${spider_name}", spider_name).replace("${spider_name_l}", filename)
    return file_str, filename


def create_readme():
    """
    create readme.md
    :return:
    :rtype:
    """
    old_path = os.path.abspath(
        os.path.join(__file__, '../', 'README.md.tmpl')
    )
    new_filename = 'README.md'
    while os.path.exists(new_filename):
        filename_md_ = input("There is'README.md' in the current directory. If you overwrite this file, please press "
                             "Enter or enter a new file name:")
        if not filename_md_:
            print("输入的空字符，生成文件覆盖源文件")
            break
        else:
            new_filename = filename_md_ + '.md'
    return old_path, new_filename


def usage():
    """
爬虫生成器

usage: kkba [options]

optional arguments:
  -F,               推荐: 将粘贴板curl或者url，生成feapder异步爬虫代码，相当于scrapy的用法
  -s                将粘贴板curl或者url，生成scrapy单文件项目
  -f,               将粘贴板curl或者url，生成feapder同步爬虫代码，相当于requests的用法
  -r,               将粘贴板curl或者url，生成requests爬虫代码
  -h, --help        帮助文档
  -v, --version     查看版本
    """
    print(usage.__doc__)
    sys.exit()


def main_cmd():
    args = sys.argv

    try:  # no params
        if args[1] in ("-h", "--help"):
            usage()

        elif args[1] in ("-v", "-V", "--version"):
            version_path = os.path.abspath(
                os.path.join(__file__, '../', 'VERSION')
            )
            with open(version_path, 'r') as f:
                version_str = f.read()
                print(version_str)
            sys.exit()
    except IndexError:
        usage()


def create_chr(dirname):
    """
    create directory path
    :param dirname:
    :type dirname:
    :return:
    :rtype:
    """
    dirname = dirname.replace('.py', '')
    while os.path.exists(dirname):
        dirname_ = input(
            f"Pathname {dirname} conflict, if you overwrite this directory, please enter Enter or enter a new path "
            "name:")
        if not dirname_:
            print("Input enter to generate a file to overwrite the source file")
            shutil.rmtree(dirname)
            break
        else:
            dirname = dirname_
    os.makedirs(dirname)
    os.chdir(dirname)
    return dirname


def get_chr(filename, output):
    """
    get directory path and spiders file
    :param filename:
    :type filename:
    :param output:
    :type output:
    :return:
    :rtype:
    """
    dirname = create_chr(filename)
    while os.path.exists(filename):
        filename_ = input(
            f"Pathname {filename} conflict, if you want overwrite this directory, please enter Enter or "
            f"enter a new path name:")
        if not filename_:
            print("Input enter to generate a file to overwrite the source file")
            break
        else:
            filename = filename_ + '.py'

    # check if exists readme.md
    old_path, new_filename = create_readme()
    shutil.copyfile(old_path, new_filename)
    open('./' + filename, 'w', encoding='utf-8').write(output)
    return 'green', f'Convertion Finished.\nPlease open {dirname} to check the code.'


def convert_main(opt):
    """
    According to the command parameter convert code
    :param opt:
    :type opt:
    :return:
    :rtype:
    """
    main_cmd()
    result_type = {
        0: 'Convertion Finished.\nNow requests code is copyed in your clipboard.',
        1: 'Please copy the curl or url before run.',
        2: 'Usage:\n\tCurl File Convert -- kkba -F requests.curl\n\tClipboard Convert -- kkba',
    }
    if opt:
        if ('-f' in opt[0]) or ('-F' in opt[0]):
            clip = str(pyperclip.paste())
            if clip.find('curl ') == 0:
                if '-f' in opt[0]:
                    output, filename = parse_curl_string_feapder(clip)
                elif '-F' in opt[0]:
                    output, filename = generate_feapder_air_spider(clip)
                return get_chr(filename, output)
            elif clip.find('http') == 0:
                clip = 'curl ' + clip
                if '-f' in opt[0]:
                    output, filename = parse_curl_string_feapder(clip)
                elif '-F' in opt[0]:
                    output, filename = generate_feapder_air_spider(clip)
                return get_chr(filename, output)
            else:
                return 'yellow', result_type[1]
            return 'red', result_type[2]
        elif '-s' in opt[0]:
            clip = str(pyperclip.paste())
            if clip.find('curl ') == 0:
                output, filename = generate_single_scrapy(clip)
                return get_chr(filename, output)
            elif clip.find('http') == 0:
                clip = 'curl ' + clip
                output, filename = generate_single_scrapy(clip)
                return get_chr(filename, output)
            else:
                return 'yellow', result_type[1]
            return 'red', result_type[2]

        elif '-r' in opt[0]:
            clip = str(pyperclip.paste())
            if clip.find('curl ') == 0:
                output, filename = parse_curlstring(clip)
                return get_chr(filename, output)
            elif clip.find('http') == 0:
                clip = 'curl ' + clip
                output, filename = parse_curlstring(clip)
                return get_chr(filename, output)
            else:
                return 'yellow', result_type[1]
            return 'red', result_type[2]

        else:
            usage()
    else:
        usage()


def main():
    """
    main function
    :return:
    :rtype:
    """
    _opts = ['version', 'help']
    _s_opts = 'rfFsSvVh'
    opt, arg = getopt.getopt(sys.argv[1:], _s_opts, _opts)
    color, feed_back = convert_main(opt)
    console = Console()
    console.print(f'=' * os.get_terminal_size()[0], justify='center')
    console.print(f'[bold {color}]{feed_back}[/]', justify='center')
    console.print(f'=' * os.get_terminal_size()[0], justify='center')
