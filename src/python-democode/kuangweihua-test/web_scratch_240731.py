"""
通过 "关键词" 提取网页链接，爬取网页内容
参考网址: https://python.langchain.com/v0.2/docs/integrations/tools/
注意需要找的工具是 Return Data 中包含 "Snippet" 的项

1. 最好不要 URL + BeatuifulSoup  
    ->  Google Serper 有 WebSearch 的选项爬取网页内容，具体看代码部分的注释网址
2. 直接得到 content 然后加入生成文本中，
    ->  文本路径: web_down_file_path = f"src/exa/exa_txt/{input_keyword}.txt"
"""

import os
import pprint

import json
import re

import requests
from bs4 import BeautifulSoup
from langchain_community.tools import DuckDuckGoSearchResults

### 关键词输入
keyword = "ProjectManager"

# Tool 1 : EXA
# def EXA_search(input_keyword):
#     # 0. EXA (Agent tool) 工具爬取使用
#     exa_api_url = "https://api.exa.ai/search"
#     exa_payload = {"query": input_keyword}
#     exa_headers = {
#         "accept": "application/json",
#         "content-type": "application/json",
#         "x-api-key": "8388973f-cd9c-4452-bfea-c860c263fbba",
#     }
#     exa_response = requests.post(exa_api_url, json=exa_payload, headers=exa_headers)
#     exa_response_json = exa_response.json()

#     # 1. 将获取的信息保存为json文件
#     exa_json_file_path = f"src/exa/exa_json/{input_keyword}.json"
#     with open(exa_json_file_path, "w", encoding="utf-8") as json_file:
#         json.dump(exa_response_json, json_file, ensure_ascii=False, indent=4)
#     print(f"1. exa json 文件保存到 {exa_json_file_path}")

#     # 2. 读取并提取 json 文件中的 url
#     with open(exa_json_file_path, "r", encoding="utf-8") as json_file:
#         exa_data = json.load(json_file)
#     urls = [result["url"] for result in exa_data["results"]]
#     print("2. URL 爬取到 (urls[0]) :",urls[0])

#     # 3. 从URL抓取网页内容并保存到文件
#     web_down_file_path = f"src/exa/exa_txt/{input_keyword}.txt"
#     with open(web_down_file_path, "a", encoding="utf-8") as file: # 'a' 模型, 追写模式
#         for url in urls:
#             try:
#                 response = requests.get(url)
#                 response.raise_for_status()
#                 soup = BeautifulSoup(response.content, "html.parser")
#                 text = soup.get_text().replace("\n", " ").replace("\r", "")
#                 file.write(f"web 内容来自 URL: {url}\n\n")
#                 file.write(text)
#                 file.write("\n\n" + "=" * 80 + "\n\n")
#             except requests.RequestException as e:
#                 print(f"获取时出错: {url}, error: {e}")
#             except Exception as e:
#                 print(f"处理内容时出错: {url}, error: {e}")
#     print(f"URL 内容全部写入到: {web_down_file_path}")
# EXA_search(keyword)


# Tool 2 : DuckDuckGo (false)
base_json_dir = "src/exa/exa_json/"
base_txt_dir = f"src/exa/exa_txt/"
# 在 base_txt_dir下建一个文件夹'{keyword}'，文件夹包含《duckduckgo_snippet》《serper_snippet》《urls》《main_txt》
# 在 base_json_dir下建一个'{keyword}'的json文件
# 根据DuckduckGo获取keyword相关内容，分别存放《duckduckgo-snippet》与《urls》文件中
# 根据GoogleSerper获取keyword相关内容，存放《duckduckgo-snippet》与《urls》文件中
# 使用GoogleSerper遍历urls，获取主要内容，存放在《main_txt》

# 创建目录
# 定义关键词目录路径和JSON文件路径
keyword_dir = os.path.join(base_txt_dir, keyword)
json_file_path = os.path.join(base_json_dir, f"{keyword}.json")

# 定义需要创建的文件列表
files_to_create = ["serper_snippet", "main_txt"]

# 定义各个文件的路径
file_paths = {file_name: os.path.join(keyword_dir, file_name) for file_name in files_to_create}


def create_files_and_json():
    # 如果目录不存在则创建
    os.makedirs(keyword_dir, exist_ok=True)
    os.makedirs(base_json_dir, exist_ok=True)

    # 在目录中创建每个文件
    for file_path in file_paths.values():
        open(file_path, 'w').close()

    # 创建一个空的JSON文件
    with open(json_file_path, 'w') as json_file:
        json.dump({}, json_file)


create_files_and_json()

# 定义各个文件路径变量
GoogleSerper_path = file_paths["serper_snippet"]

main_txt_path = file_paths["main_txt"]


#
# def DuckDuckGo_search(input_keyword):
#     DuckDuckGo_search = DuckDuckGoSearchResults()
#     results = DuckDuckGo_search._run(input_keyword)
#     return results
#
#
# # 执行DuckDuckGo搜索
# DuckDuckGo_results = DuckDuckGo_search(keyword)
#
# # 打印DuckDuckGo搜索结果
# print(DuckDuckGo_results)
# print(type(DuckDuckGo_results))
#
# # 用正则表达式将原始字符串转换为 JSON 格式
# json_str = re.sub(r'\[snippet: ', '{"snippet": ', DuckDuckGo_results)
# json_str = re.sub(r', title: ', ', "title": ', json_str)
# json_str = re.sub(r', link: ', ', "link": ', json_str)
# json_str = re.sub(r'\]', '}', json_str)
# json_str = '[' + json_str + ']'
#
# # 解析 JSON 字符串
# try:
#     json_data = json.loads(json_str)
#     print(json_data)
# except json.JSONDecodeError as e:
#     print(f"JSON 解码错误: {e}")
#

# Tool 3 : Google Serper
# 官网: https://serper.dev/
# LangChain: https://python.langchain.com/v0.2/docs/integrations/tools/google_serper/
# 可以获取原始数据，也可以进行 Google 图片搜索 / Google 新闻 / Google 地理位置
# !!! 这个也有 URL 的爬取，可以结合 EXA 得到的 URL？
def GoogleSerper_search(input_keyword):
    from langchain_community.utilities import GoogleSerperAPIWrapper
    # 进 GoogleSerperAPIWrapper 中，有直接拼接 Snippet 的函数
    os.environ["SERPER_API_KEY"] = "0b33d1ee4053a32b93f6d029f66aa149599d7c91"
    GoogleSerper_search = GoogleSerperAPIWrapper(k=10, type="search")
    response = GoogleSerper_search.results(input_keyword)
    print("GoogleSerper response:", response)
    print(type(response))
    # 将响应结果保存为 JSON 文件
    file_path = json_file_path
    with open(file_path, 'w') as file:
        json.dump(response, file, indent=4)

    print(f"响应结果已保存到 {file_path}")

    # 将snippet保存
    # Extract snippets and links
    snippets = [item['snippet'] for item in response['organic']]

    file_path = GoogleSerper_path
    with open(file_path, 'w') as file:
        file.write('Snippets:\n')
        file.write('\n'.join(snippets))
    print(f"snippet结果已保存到 {file_path}")


GoogleSerper_search(keyword)


# 通过json里的urls获取主要txt，存放到main_txt中
#     # 2. 读取并提取 json 文件中的 url
def extract_links_from_json(json_file_path):
    # 读取 JSON 文件
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # 提取链接
    links = [item['link'] for item in data.get('organic', [])]
    return links


urls = extract_links_from_json(json_file_path)

print(urls)


def scrape_urls(api_key, urls, output_file):
    # 设置请求的URL
    url = "https://scrape.serper.dev"

    # 打开输出文件
    with open(output_file, 'w', encoding='utf-8') as file:
        # 遍历所有的URL
        for target_url in urls:
            # 构建请求的payload
            payload = json.dumps({
                "url": target_url
            })

            # 设置请求头
            headers = {
                'X-API-KEY': api_key,
                'Content-Type': 'application/json'
            }

            # 发送POST请求
            response = requests.request("POST", url, headers=headers, data=payload)
            print(type(response))
            print(response)
            # 写入响应结果
            # file.write(f"URL: {target_url}\n")
            file.write(response.text + "\n")

    print(f"所有响应结果已保存到 {output_file}")


# 示例用法
api_key = 'ed86bb07558520108083d454996e405afa715db1'

output_file = main_txt_path
scrape_urls(api_key, urls, output_file)
