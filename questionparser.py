import requests
from bs4 import BeautifulSoup
import logging
import re
import json

def find_all_question_options(htmlText : str):

    soup = BeautifulSoup(htmlText, 'html.parser')
    questionsSrc = [{
        'question_id': s.find('div',attrs={'data-question-id':re.compile('[0-9a-z]')})['data-question-id'],
        'question': s.find('span',attrs={'class': re.compile('user-generated notranslate')}).find('span')
    } for s in soup.find_all(name='div',attrs={ 'class': re.compile('question-container')})]

    for s in questionsSrc:
        s['options'] = [inputSoup['value'] for inputSoup in soup.find_all(name='input',attrs={'name':s['question_id']})]
        if s['question'] is not None:
            for child in s['question'].findAll():
                child.decompose()
            s['question'] = s['question'].text.strip()

    return questionsSrc

def parseQuestions_20221013(htmlText : str,EmployeeID:str):
    questions = find_all_question_options(htmlText)
    ans = [-1,0,-1,3,3,-1,-1,0]
    assert(len(questions) == len(ans))
    assert(any(x for x in questions if x["question"] == '工號'))

    #print(questions)
    soup = BeautifulSoup(htmlText)
    survey_dataInput = soup.find('input',attrs={'id':'survey_data'})
    assert(survey_dataInput)

    data = { 'survey_data' : survey_dataInput.attrs['value']}
    for idx in range(len(ans)):
        qid = questions[idx]['question_id']
        answer = questions[idx]['options'][ans[idx]] if ans[idx] >= 0 else ''
        data[qid] = answer

    id = [x for x in questions if x["question"] == '工號'].pop()['question_id']
    data[id] = EmployeeID
    return data


if __name__ == '__main__':
    s = requests.Session()

    url = 'https://zh.surveymonkey.com/r/EmployeeHealthCheck'
    res = s.get(url)

    assert(res.status_code == 200)

    data = parseQuestions_20221013(res.text,'084849')

    print(data)

    with open("questions.json", 'a') as out_file:
        out_file.write(json.dumps(data))
