from bs4 import BeautifulSoup
#import urllib
import urllib.request
import re
import sys
from konlpy.tag import Twitter
from collections import Counter


# 결과 파일들: 2 = 결과 약간 필터링, 3 = 단어 분석
RESULT_FILE_NAME = "result.txt"
RESULT_FILE_NAME2 = "result2.txt"
RESULT_FILE_NAME3 = "result3.txt"
# 파싱 대상 URL: 티몬 슈퍼마트 비비고 육개장(http://www.ticketmonster.co.kr/userReview/732328290/19240042/?page=1#content_start)
URL= 'http://www.ticketmonster.co.kr/userReview/732328290/19240042/?page=1#content_start'
# URL 중간에 리뷰 페이지가 넘어가는 숫자가 있기 때문에 URL을 분리해 둠
U_head = "http://www.ticketmonster.co.kr/userReview/732328290/19240042/?page="
U_tail = "#content_start"

# 크롤링 함수
def get_text(URL):
    # URL 페이징을 위한 숫자
    URL_NUM = 1
    text =''
    for i in range(1, 5):
        # 몇 페이지를 연속적으로 크롤링 할거니까
        full_url = U_head + str(URL_NUM) + U_tail
        source_code_from_URL = urllib.request.urlopen(full_url)
        soup = BeautifulSoup(source_code_from_URL, 'lxml', from_encoding="utf-8")
        #text =  str(URL_NUM)+ text
        # 리뷰가 들어있는 div에서 crawling
        for item in soup.find_all('div', {"class": "review_ct"}):
            #text = text + str(item.find_all(text=True))
            #text += str(item.find_all('div', {"class": "sec"}))
            # # 여기까지 잘 작동함
            # tmp = item.find_all('div', {"class": "sec"})
            # for x in tmp:
            #     text += str(x.find_all('div', {"class": "review_area"}))
            tmp = item.find_all('div', {"class": "sec"})
            for x in tmp:
                text += str(x.find('div', {"class": "review_area"}).find('div', {"class": "txt_box"}).find('div', {"class": "txt"}))
        # 페이지 한 장 넘기기
        URL_NUM += 1
    return text
    # source_code_from_URL = urllib.request.urlopen(URL)
    # soup = BeautifulSoup(source_code_from_URL, 'lxml', from_encoding="utf-8")
    # text = ''
    # review_result = soup.find('div', {"class": "detail_list_review extend_premium"})
    # list = review_result.find_all('li')
    # # 프리미엄 리뷰 부분 가져오기
    # for item in soup.find_all('div', {"class": "detail_list_review extend_premium"}):
    #     text = text +str(item.find_all(text=True))

    # 쿠팡 리뷰 부분 가져오기 -> 쿠팡은 수집 막아놨나? 안되는데ㅋ
    # for item in soup.find_all('div', {"class": "review_ct"}):
    #     text = text + str(item.find_all(text=True))
    # review_result = soup.find('div', class_='list _premiumReviewListArea', display='hidden')
    # lis = review_result.find_all('li')
    #
    # count = 10
    # for li in lis:
    #     page = 1
    #     #reple = str(li.find('div',class_='item case_2 _click').find('div', class_='row').find('div', class_='col_content').find('div', class_='inner_content').find('div', class_='review_comment').find('p'))
    #     reple = str(li.find('div', class_='item case_2 _click').find('p'))
    #     text = text + reple

# 개행문자만 제거하려다가 필요 없는 잡다한 문자 제거
def remove_newline_char(newline):
    remove_newline = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]','', newline)
    remove_newline = re.sub('[a-zA-Z]','', remove_newline)
    return remove_newline

# 키워드 가져오기: http://yoonpunk.tistory.com/7 블로그 참조함
def get_keywords(text, ntags = 50):
    spliter = Twitter()
    nouns = spliter.nouns(text)
    count = Counter(nouns)
    return_list = []
    for n, c in count.most_common(ntags):
        temp = {'tag': n, 'count':c}
        return_list.append(temp)
    return return_list

# 메인 함수
def main():
    #  비비고 육개장 리뷰들 텍스트 파일에 저장
    open_result_file = open(RESULT_FILE_NAME2,'w', encoding='UTF-8', newline='')
    result_text = get_text(URL)
    result_text = remove_newline_char(result_text)
    open_result_file.write(result_text)
    open_result_file.close()
    # 저장한 텍스트 파일에서 자주쓰이는 명사 카운팅
    open_text_file = open(RESULT_FILE_NAME2, 'r', encoding='UTF-8', newline='')
    text = open_text_file.read()
    tags = get_keywords(text, 20)
    open_text_file.close()
    open_output_file = open(RESULT_FILE_NAME3, 'w', encoding='UTF-8', newline='')
    for tag in tags:
        noun = tag['tag']
        count = tag['count']
        open_output_file.write('{} {}\n'.format(noun, count))

    open_output_file.close()

if __name__ == '__main__':
    main()