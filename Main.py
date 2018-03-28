import requests
from bs4 import BeautifulSoup

# LoanCategoryId
TYPE_KPT = '4'  # 平衡型
TYPE_BLC = '8'  # 保守型


def html_to_soup(url):
    r = requests.get(url)
    html = r.content
    return BeautifulSoup(html, 'xml')


# url构造器 获得爬取链接
def url_constructor(page_index, type):
    base_url = 'https://invest.ppdai.com/loan/' \
               'listnew?LoanCategoryId=' + type + \
               '&PageIndex=' + str(page_index) + \
               '&SortType=0&MinAmount=0&MaxAmount=0'
    # 处理逻辑
    aim_url = base_url
    return aim_url


# 获取链接页面所包含的详情页链接并封装到List
def details_url_list_getter(url):
    soup = html_to_soup(url)
    # 整个信息列表所在的div
    div_outer_borrow_list = soup.find('div', attrs={'class': 'outerBorrowList'})
    if '很抱歉，热门列表已经被抢空啦' in div_outer_borrow_list:
        return []
    else:
        # 详情信息所在的a标签
        a_s = div_outer_borrow_list.find_all('a', attrs={'class': 'title ell'})
        details_urls = []
        for a in a_s:
            details_urls.append(a['href'])
        return details_urls


# 详情页信息提取
def details_info_getter(details_url):
    soup = html_to_soup(details_url)
    # 整个信息列表所在的div
    wrap_new_lend_detail = soup.find('div', attrs={'class': 'wrapNewLendDetailInfoLeft'})
    #print(wrap_new_lend_detail_list)
    # 包含信用等级的a [信用等级详细值在其中span标签的class属性中]
    level = wrap_new_lend_detail.find('a', attrs={'class': 'altQust'}).find('span')['class']
    print(level)


# Main method
if __name__ == '__main__':
    details_url_list = details_url_list_getter(url_constructor(1, TYPE_KPT))
    if len(details_url_list) > 0:
        details_info_getter('https:' + details_url_list[0])
        # for it in details_url_list:
        # print(it)
    else:
        print('Error:未找到数据!')
