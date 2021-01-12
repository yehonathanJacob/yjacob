from tqdm import tqdm
import json
import requests
from scrapy.http import HtmlResponse
import pandas as pd

JSON_PARAMS_PATTERN = """{"NewNameMade":"30213","Referral":"button","FromRec":"","SiteName":"LIB_givat-shmuel","CNumber":"10534140","SearchType":"Card1","BuyerID":"397186064","Clubtmp1":"","comefrom":"https://givat-shmuel.libraries.co.il/BuildaGate5library/general2/company_search_tree.php","DataCardTemplate":"","framemode":"","framesource":"","CardPrice":"","BANNER":"","goToSearchWithItm":"","goToSearchWithCrd":"","chosenItem":"","cndLikeOrEq":"","lgFlag":"","userDataTxt":" ","userMailTxt":"","userSbjTxt":"","userContTxtarea":"","adv_open":"none","ThisCard":"Card1","SearchFildType_1":"DataCardName~DataCardField_1","FreeText_1":"אבא עשיר,","Bool_1":" and ","SearchFildType_2":"DataCardName~DataCardField_1","FreeText_2":"","Bool_2":" and ","SearchFildType_3":"DataCardName~DataCardField_1","FreeText_3":"","SubCats0_numOfCheck":"46","SubCats1_numOfCheck":"47","SubCats2_numOfCheck":"5","SearchTime":"","PublYearEnFrom":"","PublYearEnTo":"","PublYearHeFrom":"","PublYearHeTo":"","catalogingYearFrom":"","catalogingYearTo":"","ourChoiceSel_Card1":"-1","ourChoiceSel_Card8":"-1","ourChoiceSel_Card2":"-1","ourChoiceSel_Card34":"-1","ourChoiceSel_Card35":"-1","ourChoiceSel_Card4":"-1","ourChoiceSel_Card3":"-1","ourChoiceSel_Card5":"-1","z1":"10","Category":"","OrderByField":"","OrderBy":"","itemsIdsArray":"9743,36634,4078,28540,","FF":"","z":"","ItemID":"","ValuePage":""}"""
DEFUALT_SENDING_PATTERN = json.loads(JSON_PARAMS_PATTERN)
URL_TO_SEARCH_API = 'https://givat-shmuel.libraries.co.il/BuildaGate5library/general2/company_search_tree.php'

if __name__ == '__main__':
    print("############### START ###################")
    with open('source.json', 'r') as f:
        source_data = json.load(f)

    output_data = []
    errors = []
    sending_pattern = DEFUALT_SENDING_PATTERN.copy()
    for book in tqdm(source_data):
        txt_to_search = book['name']
        link_to_book = book['link']
        description = book['pargraph']
        sending_pattern['FreeText_1'] = txt_to_search
        try:
            r = requests.post(URL_TO_SEARCH_API, params=sending_pattern)
            response = HtmlResponse(url=URL_TO_SEARCH_API, body=r.text, encoding='utf-8')
            founded_books = response.selector.css('td[width="222"]')
            if len(founded_books) >0:
                founded_books_title = []
                for book_html in founded_books:
                    book_title = ''.join(book_html.css('*::text').extract()).replace('\n','')
                    founded_books_title.append(book_title)
                founded_books_title_str = '|'.join(founded_books_title)
                output_data.append({**book, 'founded_books_title': founded_books_title_str})
        except Exception as e:
            print(f'ERROR: {e}')
            errors.append({'data':book, 'error':e})
    df = pd.DataFrame(output_data)
    df.to_excel('output.xlsx')
    print("############### DONE ###################")




