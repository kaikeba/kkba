import argparse
import json
import re
import shlex
from collections import OrderedDict
from os import get_terminal_size
from urllib.parse import urlparse, unquote

from rich.console import Console
from rich.syntax import Syntax


def prettier_print(code: str):
    """
    pretter print
    :param code:
    :type code:
    :return:
    :rtype:
    """
    syntax = Syntax(code, "python", theme="monokai", line_numbers=True)
    console = Console()
    console_width = int((get_terminal_size()[0] - 36) / 2)
    console.print("=" * console_width +
                  "[bold magenta] Python Requests Code Preview Start [/]" +
                  "=" * console_width,
                  justify='center')
    console.print(syntax)
    console.print("=" * console_width +
                  "[bold magenta]  Python Requests Code Preview End  [/]" +
                  "=" * console_width,
                  justify='center')


def parse_content_type(content_type: str):
    """
    parse content type
    :param content_type:
    :type content_type:
    :return:
    :rtype:
    """
    parts = content_type.split(';', 1)
    tuparts = parts[0].split('/', 1)
    if len(tuparts) != 2:
        return None
    dparts = OrderedDict()
    if len(parts) == 2:
        for i in parts[1].split(";"):
            c = i.split("=", 1)
            if len(c) == 2:
                dparts[c[0].strip()] = c[1].strip()
    return tuparts[0].lower(), tuparts[1].lower(), dparts


def format_multi(the_multi_list, indent=4):
    """
    format multi data
    :param the_multi_list:
    :type the_multi_list:
    :param indent:
    :type indent:
    :return:
    :rtype:
    """
    return 'MultipartEncoder(\n' + " " * indent + 'fields=[\n' + " " * indent * 2 + (
            ",\n" + " " * indent * 2).join(map(str, the_multi_list)) + '\n])'


def parse_multi(content_type, the_data):
    """
    parse multi data
    :param content_type:
    :type content_type:
    :param the_data:
    :type the_data:
    :return:
    :rtype:
    """
    boundary = b''
    if content_type:
        ct = parse_content_type(content_type)
        if not ct:
            print('nocontent-type')
            return ['no content-type']
        try:
            boundary = ct[2]["boundary"].encode("ascii")
        except (KeyError, UnicodeError):
            print('no boundary')
            return ['no boundary']
    if boundary:
        result = []
        for i in the_data.split(b"--" + boundary):
            p = i.replace(b'\\x0d', b'\r')
            p = p.replace(b'\\x0a', b'\n')
            p = p.replace(b'\\n', b'\n')
            p = p.replace(b'\\r', b'\r')
            parts = p.splitlines()
            print(parts)
            if len(parts) > 1 and parts[0][0:2] != b"--":
                if len(parts) > 4:
                    tmp_value = {}
                    key, tmp_value['filename'] = re.findall(
                        br'\bname="([^"]+)"[^"]*filename="([^"]*)"',
                        parts[1])[0]
                    tmp_value['content'] = b"".join(
                        parts[3 + parts[2:].index(b""):])
                    tmp_value['content_type'] = parts[2]
                    value = (tmp_value['filename'].decode(),
                             tmp_value['content'].decode(),
                             tmp_value['content_type'].decode())
                else:
                    key = re.findall(br'\bname="([^"]+)"', parts[1])[0]
                    value = (b"".join(parts[3 +
                                            parts[2:].index(b""):])).decode()
                result.append((key.decode(), value))
        return result


def parse_args(curl_cmd):
    """
    argparse parse curl params
    :param curl_cmd:
    :type curl_cmd:
    :return:
    :rtype:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('command')
    parser.add_argument('url')
    parser.add_argument('-d', '--data')
    parser.add_argument('-b', '--cookie', default=None)
    parser.add_argument('--data-binary',
                        '--data-raw',
                        '--data-ascii',
                        default=None)
    parser.add_argument('-X', default='')
    parser.add_argument('-F', '--form', default=None)
    parser.add_argument('-H', '--header', action='append', default=[])
    parser.add_argument('-A', '--user-agent', default='')
    parser.add_argument('--compressed', action='store_true')
    parser.add_argument('-k', '--insecure', action='store_true')
    parser.add_argument('-I', '--head', action='store_true')
    parser.add_argument('-G', '--get', action='store_true')
    parser.add_argument('--user', '-u', default=())
    parser.add_argument('-i', '--include', action='store_true')
    parser.add_argument('-s', '--silent', action='store_true')
    cmd_set = shlex.split(curl_cmd)
    arguments = parser.parse_args(cmd_set)
    return arguments


def prettier_dict(the_dict, indent=4):
    """
    pretter dict
    :param the_dict:
    :type the_dict:
    :param indent:
    :type indent:
    :return:
    :rtype:
    """
    if not the_dict:
        return "{}"
    return ("\n" + " " * indent).join(
        json.dumps(the_dict,
                   sort_keys=True,
                   indent=indent,
                   separators=(',', ': ')).splitlines())


def prettier_tuple(the_tuple, indent=4):
    """
    pretter tuple
    :param the_tuple:
    :type the_tuple:
    :param indent:
    :type indent:
    :return:
    :rtype:
    """
    if not the_tuple:
        return "()"
    return '(\n' + " " * indent + ("," + "\n" + " " * indent).join(
        str(i) for i in the_tuple) + ',\n)'


def curl_replace(curl_cmd):
    """
    replace curl part string
    :param curl_cmd:
    :type curl_cmd:
    :return:
    :rtype:
    """
    curl_str_replace = [(r'\\\r|\\\n|\r|\n', ''), (' -XPOST', ' -X POST'),
                        (' -XGET', ' -X GET'), (' -XPUT', ' -X PUT'),
                        (' -XPATCH', ' -X PATCH'), (' -XDELETE', ' -X DELETE'),
                        (' -Xnull', '')]
    tmp_curl_cmd = curl_cmd
    for pattern in curl_str_replace:
        tmp_curl_cmd = re.sub(pattern[0], pattern[1], tmp_curl_cmd)
    return tmp_curl_cmd.strip()


class parse_curl_command:
    def __init__(self, curl_cmd):
        """
        parse curl command
        :param curl_cmd: curl command
        :type curl_cmd: str
        """
        self.curl_cmd = curl_replace(curl_cmd)
        self.arguments = parse_args(self.curl_cmd)
        self.method = 'get'
        post_data = self.arguments.data or self.arguments.data_binary
        self.urlparse = urlparse(self.arguments.url)
        self.url = "{}://{}{}".format(self.urlparse.scheme,
                                      self.urlparse.netloc, self.urlparse.path)
        self.cookies = None
        if self.urlparse.query:
            self.params = tuple(
                re.findall(r'([^=&]*)=([^&]*)', unquote(self.urlparse.query)))
        else:
            self.params = ()
        headers = self.arguments.header
        cookie_string = ''
        content_type = ''
        if headers:
            self.headers = dict(
                [tuple(header.split(': ', 1)) for header in headers])
            cookie_string = self.headers.get('cookie') or self.headers.get(
                'Cookie')
            if 'cookie' in self.headers:
                self.headers.pop('cookie')
            if 'Cookie' in self.headers:
                self.headers.pop('Cookie')
            content_type = self.headers.get(
                'Content-Type') or self.headers.get('content-type')
        else:
            self.headers = {}
        if self.arguments.cookie:
            cookie_string = self.arguments.cookie
        if post_data and not self.arguments.get:
            self.method = 'post'
            if "multipart/form-data" in content_type.lower():
                self.data = parse_multi(
                    content_type,
                    unquote(post_data.strip('$')).encode('raw_unicode_escape'))
            elif '{"' in post_data:
                self.data = post_data
            else:
                self.data = dict(
                    re.findall(r'([^=&]*)=([^&]*)', unquote(post_data)))
        elif post_data:
            self.params = tuple(
                re.findall(r'([^=&]*)=([^&]*)', unquote(post_data)))
            self.data = {}
        else:
            self.data = {}
        if self.arguments.X:
            self.method = self.arguments.X.lower()
        if cookie_string:
            self.cookies = dict(
                re.findall(r' ([^=\s]*)=([^;]*)', cookie_string))
        if self.arguments.insecure:
            self.insecure = True
        else:
            self.insecure = False
