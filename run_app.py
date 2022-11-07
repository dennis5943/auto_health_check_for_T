import requests
from bs4 import BeautifulSoup
import logging
from requests_toolbelt.multipart.encoder import MultipartEncoder
from fake_useragent import UserAgent
import re

proxies = {
   'http': 'http://localhost:8090',
   'https': 'http://localhost:8090',
}


logging.basicConfig(filename='/app/actionlog.log', encoding='utf-8', level=logging.DEBUG)

url4home = 'https://zh.surveymonkey.com/r/EmployeeHealthCheck'
url4post = 'https://zh.surveymonkey.com/r/EmployeeHealthCheck'

def getSurveyData(s:requests.session):
    res = s.get(url4home, verify = False)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text)
        input = soup.find('input',attrs={'id':'survey_data'})

        searchBeaconUrl = soup.find('script',attrs={'type':'text/javascript'},text=re.compile("rumAuth", flags=re.DOTALL))
        if not searchBeaconUrl:
            raise "Cannot find rumAuth"

        logging.debug('searchBeaconUrl:'+searchBeaconUrl.text)
        beaconUrl = '{}?auth={}'.format( \
            re.search("beaconUrl:\s*'([^']+)'",searchBeaconUrl.text).group(1),\
            re.search("rumAuth:\s*'([^']+)'",searchBeaconUrl.text).group(1))
        logging.info('beaconUrl:'+beaconUrl)
        print(beaconUrl)
        
        return input.attrs['value'],beaconUrl
    
    raise "Fail"

def postMyAnswer(s:requests.session, survey_data:str):
    mp_encoder = MultipartEncoder(
        fields={
            '87960815': '688357155',
            '87960813': '[Type your Employee ID]',
            '87960820': '688357202',
            '87960821': '688357189',
            '87960822_688357192_DMY': '',
            '87960814':'688357154',
            'survey_data': survey_data,
            'response_quality_data':'{"question_info":{"qid_87960816":{"number":-1,"type":"presentation_text","option_count":null,"has_other":false,"other_selected":null,"relative_position":null,"dimensions":null,"input_method":null,"is_hybrid":false},"qid_87960815":{"number":1,"type":"single_choice_vertical","option_count":1,"has_other":false,"other_selected":null,"relative_position":[[0,0]],"dimensions":[1,1],"input_method":null,"is_hybrid":false},"qid_87960813":{"number":2,"type":"open_ended","option_count":null,"has_other":false,"other_selected":null,"relative_position":null,"dimensions":null,"input_method":"text_typed","is_hybrid":true},"qid_87960820":{"number":3,"type":"single_choice_vertical","option_count":4,"has_other":false,"other_selected":null,"relative_position":[[3,0]],"dimensions":[4,1],"input_method":null,"is_hybrid":false},"qid_87960821":{"number":4,"type":"single_choice_vertical","option_count":4,"has_other":false,"other_selected":null,"relative_position":[[3,0]],"dimensions":[4,1],"input_method":null,"is_hybrid":false},"qid_87960822":{"number":5,"type":"datetime","option_count":null,"has_other":false,"other_selected":null,"relative_position":null,"dimensions":null,"input_method":null,"is_hybrid":false},"qid_87960823":{"number":-1,"type":"presentation_text","option_count":null,"has_other":false,"other_selected":null,"relative_position":null,"dimensions":null,"input_method":null,"is_hybrid":false},"qid_87960814":{"number":6,"type":"single_choice_vertical","option_count":1,"has_other":false,"other_selected":null,"relative_position":[[0,0]],"dimensions":[1,1],"input_method":null,"is_hybrid":false}},"tooltip_open_count":0,"opened_tooltip":false,"start_time":1667491590362,"end_time":1667491618689,"time_spent":28327,"previous_clicked":false,"has_backtracked":false,"bi_voice":{}}',
            'is_previous': 'false',
            'disable_survey_buttons_on_submit': ''
            # plain file object, no filename or mime type produces a
            # Content-Disposition header with just the part name
        }
    )

    headers = {
        'Host': 'zh.surveymonkey.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:106.0) Gecko/20100101 Firefox/106.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Origin': 'https://zh.surveymonkey.com',
        'Connection': 'keep-alive',
        'Referer': 'https://zh.surveymonkey.com/r/EmployeeHealthCheck',
        'Content-Type': mp_encoder.content_type,
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1'
    }
    #headers['User-Agent'] = UserAgent().random

    res = s.post(
        url4post,
        data=mp_encoder,  # The MultipartEncoder is posted as data, don't use files=...!
        # The MultipartEncoder provides the content-type header with the boundary:
        headers = headers,
        verify=False
    )

    if res.status_code == 200 and re.search('填寫完成',res.text):
        logging.info('通報完成')
    else:
        logging.error(res.text)
        raise 'Script Error, please check the version.'
        

    #print(res.text)

if __name__ == '__main__':
    s = requests.Session()

    token,searchBeaconUrl = getSurveyData(s)
    postMyAnswer(s,token)
    print('token:',token)