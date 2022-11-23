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


"""
'97301341': '751278109',
'97301339': '084849',
'97301346': '751278156',
'97301347': '751278143',
#'97301348_751278146_DMY': '',
'97301340':'751278108',

{'question_id': '97301342', 'question': '如您開始填寫並送交員工體溫回報表者，視為同意個人資料蒐集聲明內容所載之蒐集、處理及利用個人資料告知事項。詳細請見。'}
----------------------------------------
{'question_id': '97301341', 'question': '如您開始填寫並送交員工體溫回報表者，視為同意本蒐集、處理及利用個人資料告知事項。本個人資料蒐集不強制適用於本公司位於台灣以外的集團公司。'}
<input aria-checked="{}" aria-labelledby="97301341_751278109_label" class="radio-button-input" id="97301341_751278109" name="97301341" role="radio" type="radio" value="751278109"/>
----------------------------------------
{'question_id': '97301339', 'question': '工號'}
----------------------------------------
{'question_id': '97301346', 'question': '2. 身體症狀 Physical Conditions'}
<input aria-checked="{}" aria-labelledby="97301346_751278153_label" class="radio-button-input" id="97301346_751278153" name="97301346" role="radio" type="radio" value="751278153"/>
<input aria-checked="{}" aria-labelledby="97301346_751278154_label" class="radio-button-input" id="97301346_751278154" name="97301346" role="radio" type="radio" value="751278154"/>
<input aria-checked="{}" aria-labelledby="97301346_751278155_label" class="radio-button-input" id="97301346_751278155" name="97301346" role="radio" type="radio" value="751278155"/>
<input aria-checked="{}" aria-labelledby="97301346_751278156_label" class="radio-button-input" id="97301346_751278156" name="97301346" role="radio" type="radio" value="751278156"/>
----------------------------------------
{'question_id': '97301347', 'question': '3. 執行快篩者其結果？Execute COVID-19 rapid test kits and result'}
<input aria-checked="{}" aria-labelledby="97301347_751278140_label" class="radio-button-input" id="97301347_751278140" name="97301347" role="radio" type="radio" value="751278140"/>
<input aria-checked="{}" aria-labelledby="97301347_751278141_label" class="radio-button-input" id="97301347_751278141" name="97301347" role="radio" type="radio" value="751278141"/>
<input aria-checked="{}" aria-labelledby="97301347_751278142_label" class="radio-button-input" id="97301347_751278142" name="97301347" role="radio" type="radio" value="751278142"/>
<input aria-checked="{}" aria-labelledby="97301347_751278143_label" class="radio-button-input" id="97301347_751278143" name="97301347" role="radio" type="radio" value="751278143"/>
----------------------------------------
{'question_id': '97301348', 'question': None}
----------------------------------------
{'question_id': '97301349', 'question': '提醒：'}
----------------------------------------
{'question_id': '97301340', 'question': '本人已詳細閱讀上述調查表所列事項，並保證填寫內容正確屬實。'}
<input aria-checked="{}" aria-labelledby="97301340_751278108_label" class="radio-button-input" id="97301340_751278108" name="97301340" role="radio" type="radio" value="751278108"/>
----------------------------------------


<div data-question-type="datetime_date_only"
     data-rq-question-type="datetime"
     class="question-container
    
        
        
    
    ">

    <div id="question-field-97301348"
        data-qnumber="6"
        data-qdispnumber="5"
        data-question-id="97301348"
        class=" question-datetime qn question date_only"
        
        
    >
        
        
            <h3 class="screenreader-only">Question Title</h3><div class=" question-fieldset question-legend"  >
                
                
                <h4 id="question-title-97301348" class=" question-title-container ">
                    <span class="required-asterisk notranslate">
                            *
                        </span>

                    
                    
                <span class="user-generated notranslate  
                ">
                檢測日期 Rapid test date</span>
                
                </h4>
                <div class="question-body clearfix notranslate ">
                    

    
    
        <div class="question-datetime-row  row-0 clearfix">
            <!-- translate to-do -->
            <label id="97301348_751278146_DMY_label" class="question-datetime-row-text question-body-font-theme row-0 user-generated">
                Date
            </label>
            <div class="question-datetime-fields">
                
                    <div class="question-datetime-date">
                        <div class="question-datetime_hint">
                          日期
                        </div>
                        
                        <div class="input-group date">
                            
                            
                            
                            
                            <input id="97301348_751278146_DMY"
                                   name="97301348_751278146_DMY"
                                   type="text"
                                   class="form-control text date--picker date-validation"
                                   data-date-question-id="97301348_751278146"
                                   placeholder="MM/DD/YYYY"
                                   
                                   maxlength="10"
                                   autocomplete="off"
                                   data-date-picker
                                   data-date-format="mm/dd/yyyy"
                                   data-date-language=zh-tw
                                   data-format-message="* 請以「月/日/年 (mm/dd/yyyy)」的格式輸入日期。"
                                   data-year-message="* 請使用 1900 – 9999 之間的數字來輸入「年」。"
                                   aria-label="選擇／修改日期：使用 Shift + 向上鍵／向下鍵可變更月份，使用 Ctrl + Shift + 向上鍵／向下鍵可變更年份"
                            />
                            <label class="input-group-addon btn" for="97301348_751278146_DMY">
                              <span class="glyphicon glyphicon-calendar"></span>
                            </label>  
                        </div>
                    </div>
                

                
            </div>
            <div class="datetime_validations">
              <label for="97301348_751278146_DMY" generated="true" class="error" role="alert"></label>
              <label for="97301348_751278146_H" generated="true" class="error" role="alert"></label>
              <label for="97301348_751278146_M" generated="true" class="error" role="alert"></label>
              <label for="97301348_751278146_AM" generated="true" class="error" role="alert"></label>
            </div>
        </div>
    

                </div>
            </div>
    </div>
</div></div>
"""