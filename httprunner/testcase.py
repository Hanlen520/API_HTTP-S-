# encoding:utf-8
import ast
import csv
import io
import itertools
import json
import os
import random
import re

import yaml
from httprunner import exception, logger, utils
from httprunner.compat import OrderedDict, numeric_types

variable_regexp=r'\$([\w]+)'
function_regexp=r'\$\{([\w]+\([\$\w\.\-_=,]*\))\}'
function_regexp_compile=re.compile(r"^([\w_]+)\(([\$\w\.\-_=,]*)\)$")

test_def_overall_dit={
    "loaded":False,
    "api":{},
    "suite":{}
}
testcases_cache_mapping={}
def _load_yaml_file(yaml_file):
    """
    加载yaml文件，并检查文件格式内容
    :param yaml_file:
    :return:
    """
    with io.open(yaml_file, 'r', encoding='utf-8') as stream:
        yaml_content = yaml.load(stream)
        #check_format(yaml_file, yaml_content)
        return yaml_content

def _load_json_file(json_file):
    with io.open(json_file,'r') as data_file:
        try:
            json_content=json.load(data_file)
        except exception.JSONDecodeError:
            err_msg = u"JSONDecodeError: JSON file format error: {}".format(json_file)
            logger.log_error(err_msg)
            raise exception.FileFormatError(err_msg)
        #check_format(json_file,json_content)
        return json_content

def _load_csv_file(csv_file):
    csv_contnet_list=[]
    with io.open(csv_file) as csvfile:
        reader=csv.DictReader(csvfile)
        for row in reader:
            csv_contnet_list.append(row)
    return csv_contnet_list


def load_file(file_path):
    #文件加载
    if not os.path.isfile(file_path):
        raise exception.FileNotFoundError("{} does not exist.".format(file_path))
    file_suffix=os.path.splitext(file_path)[1].lower()
    if file_suffix=='.json':
        return _load_json_file(file_path)
    elif file_suffix in ['.yaml','yml']:
        return _load_yaml_file(file_path)
    elif file_suffix=='.csv':
        return _load_csv_file(file_path)
    else:
        #不支持的格式
        err_msg=u"Unsupported file format:{}".format(file_path)
        logger.log_warning(err_msg)
        return []

def extract_variables(content):
    """ 提取变量名：  extract all variable names from content, which is in format $variable
       @param (str) content
       @return (list) variable name list

       e.g. $variable => ["variable"]
            /blog/$postid => ["postid"]
            /$var1/$var2 => ["var1", "var2"]
         abc => []
    """
    try:
        return re.findall(variable_regexp,content)
    except TypeError:
        return []

def parse_string_value(str_value):
    """ 字符串转换成整形 parse string to number if possible
    e.g. "123" => 123
         "12.2" => 12.3
         "abc" => "abc"
         "$var" => "$var"
    """
    try:
        return ast.literal_eval(str_value)
    except ValueError:
        return str_value
    except SyntaxError:
        #e.g .$var,${func}
        return str_value

def parse_function(content):
    """ 返回函数名 参数值 parse function name and args from string content.
        @param (str) content
        @return (dict) function name and args

        e.g. func() => {'func_name': 'func', 'args': [], 'kwargs': {}}
             func(5) => {'func_name': 'func', 'args': [5], 'kwargs': {}}
             func(1, 2) => {'func_name': 'func', 'args': [1, 2], 'kwargs': {}}
             func(a=1, b=2) => {'func_name': 'func', 'args': [], 'kwargs': {'a': 1, 'b': 2}}
             func(1, 2, a=3, b=4) => {'func_name': 'func', 'args': [1, 2], 'kwargs': {'a':3, 'b':4}}
        """
    function_meta={
        "args":[],
        "kwargs":{}
    }
    matched=function_regexp_compile.match(content)
    function_meta["func_name"]=matched.group(1)

    args_str=matched.group(2).replace(" ","")
    if args_str=="":
        return function_meta

    args_list=args_str.split(',')
    for arg in args_list:
        if '=' in arg:
            key,value=arg.split('=')
            function_meta['kwargs'][key]=parse_string_value(value)
        else:
            function_meta['args'].append(parse_string_value(arg))
    return function_meta




content='func(4,k,c=2,v=5)'
matched=function_regexp_compile.match(content)
print(matched.group(2))
print(parse_function(content))




#print(parse_string_value('4311232'))
#file_path=os.path.join(os.getcwd(),'data\\account.csv')
# print(os.path.splitext(file_path)[1].lower())
# a=load_file(file_path)
# print(a)
