import requests
from bs4 import BeautifulSoup

TYPE_KPT = '4'  # LoanCategoryId 4:平衡型,8:保守型


# html转换
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
    # print(wrap_new_lend_detail_list)
    # 包含信用等级的a [信用等级详细值在其中span标签的class属性中]
    credit_level = wrap_new_lend_detail.find('a', attrs={'class': 'altQust'}).find('span')['class'] \
        .replace('creditRating ', '')
    # TODO 赔标信用标 [暂无网页]
    #

    # 用户名
    user_name = wrap_new_lend_detail.find('span', attrs={'class': 'username'}).get_text()
    # 借款的详细信息 [借款金额 , 协议利率 , 期限]
    new_lend_detail_money_list = soup.find('div', attrs={'class': 'newLendDetailMoneyLeft'}).find_all('dd')

    # 人员详细信息 [性别 , 年龄 , 注册时间 , 文化程度 , 毕业院校 , 学习形式 , 借款用途 , 还款来源 , 工作信息 , 收入情况]
    lender_info_list = soup.find('div', attrs={'class': 'lender-info'}).findAll('p', attrs={'class': 'ex col-1'})

    print(lender_info_list[0].find('span').get_text())  # 性别
    print(lender_info_list[1].find('span').get_text())  # 年龄
    print(lender_info_list[2].find('span').get_text())  # 注册时间
    print(lender_info_list[3].find('span').get_text())  # 文化程度
    print(lender_info_list[4].find('span').get_text())  # 毕业院校
    print(lender_info_list[5].find('span').get_text())  # 学习形式
    print(lender_info_list[6].find('span').get_text())  # 借款用途
    print(lender_info_list[7].find('span').get_text())  # 还款来源
    print(lender_info_list[8].find('span').get_text())  # 工作信息
    print(lender_info_list[9].find('span').get_text())  # 收入情况

    # 认证信息
    record_info_list = soup.find('ul', attrs={'class', 'record-info'}).findAll('li')
    verfied_info = ''
    for i in range(len(record_info_list)):
        verfied_info += (record_info_list[i].get_text()) + ' '

    # 总体div
    tab_contain_divs = soup.find("div", attrs={'class': 'lendDetailTab_tabContent w1000center'}) \
        .find_all('div', attrs={'class': 'tab-contain'})

    # 统计信息
    statistics_info_list = tab_contain_divs[2].find_all('span', attrs={'class', 'num'})
    print(statistics_info_list[0].get_text().strip())  # 成功借款次数
    print(statistics_info_list[1].get_text().strip())  # 历史记录
    print(statistics_info_list[2].get_text().strip())  # 成功还款次数
    print(statistics_info_list[3].get_text().strip())  # 正常还清次数
    print(statistics_info_list[4].get_text().strip())  # 逾期(0-15天)还清次数
    print(statistics_info_list[5].get_text().strip())  # 逾期(15天以上)还清次数
    print(statistics_info_list[6].get_text().strip().replace('¥', ''))  # 累计借款金额
    print(statistics_info_list[7].get_text().strip().replace('¥', ''))  # 待还金额
    print(statistics_info_list[8].get_text().strip().replace('¥', ''))  # 待收金额
    print(statistics_info_list[9].get_text().strip().replace('¥', ''))  # 单笔最高借款金额
    print(statistics_info_list[10].get_text().strip().replace('¥', ''))  # 历史最高负债

    print('------------')
    # 投资人情况List
    ol_list = soup.find('div', attrs={'class': 'scroll-area'}).find_all('ol')
    # 投资人单条信息
    for ol in ol_list:
        li_list = ol.find_all('li')
        print(li_list[0].find('span', attrs={'class': 'listname'}).get_text())  # 投资人id
        print(li_list[0].find('a', attrs={'target': '_blank'})['title'])  # 投资方式
        print(li_list[1].get_text())  # 利率
        print(li_list[2].get_text())  # 期限
        print(li_list[3].get_text().replace('¥', ''))  # 有效金额
        print(li_list[4].get_text())  # 投标时间
    print('------------')

    # print(verfied_info)
    #
    # print(credit_level, user_name)
    # print(new_lend_detail_money_list[0].get_text(), new_lend_detail_money_list[1].get_text()
    #       , new_lend_detail_money_list[2].get_text())


# Main method
if __name__ == '__main__':
    details_url_list = details_url_list_getter(url_constructor(1, TYPE_KPT))
    if len(details_url_list) > 0:
        details_info_getter('https:' + details_url_list[0])
        # for it in details_url_list:
        # print(it)
    else:
        print('Error:未找到数据!')
