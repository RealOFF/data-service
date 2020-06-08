
from natasha import MoneyExtractor, MoneyRateExtractor
from yargy import Parser
from yargy.pipelines import morph_pipeline
import pymorphy2
import re

def getSalary(text):
    if text == None:
        return {}

    salary = searchSalary4(text)
    if salary != None:
        return salary

    extractorRate = MoneyRateExtractor()
    matchesRate = extractorRate(text) #todo check why matchesRate[0] can be None
    if len(matchesRate) != 0 and matchesRate[0] != None and 'fact' in matchesRate[0] and matchesRate[0].fact != None:
        return {
            "value": matchesRate[0].fact.money.integer,
            "currency": matchesRate[0].fact.money.currency,
            "period": matchesRate[0].fact.period
        }
    salary = searchSalary2(text)
    if salary != None:
        return salary
    salary = searchSalary5(text)
    if salary != None:
        return salary
    salary = searchSalary3(text)
    if salary != None:
        return salary

    extractor = MoneyExtractor()
    matches = extractor(text)

    if len(matches) != 0:
        return {
            "value": matches[0].fact.integer,
            "currency": matches[0].fact.currency
        }

    salary = searchSalary1(text)


def searchSalary4(text):
    salary = ''
    result = re.search(r'\d{1,3} \$/ч', text)
    currency = 'USD'
    if result == None:
        result = re.search(r'\d{1,3}\$ за час', text)
        currency = 'USD'
        if result == None:
            result = re.search(r'\d{1,3}\$/ч', text)
            currency = 'USD'
            if result == None:
                result = re.search(r'\d{1,3} \$/час', text)
                currency = 'USD'
                if result == None:
                    result = re.search(r'\d{1,3}\$/час', text)
                    currency = 'USD'
                    if result == None:
                        result = re.search(r'\d{1,3} руб/час', text)
                        currency = 'RUB'
                        if result == None:
                            result = re.search(r'\d{1,3}руб/час', text)
                            currency = 'RUB'
                            if result == None:
                                result = re.search(r'\d{1,3} руб/ч', text)
                                currency = 'RUB'
                                if result == None:
                                    result = re.search(r'\d{1,3}руб/ч', text)
                                    currency = 'RUB'
                                    if result == None:
                                        result = re.search(r'\d{1,3} р/ч', text)
                                        currency = 'RUB'
                                        if result == None:
                                            result = re.search(r'\d{1,3}р/ч', text)
                                            currency = 'RUB'
                                            if result == None:
                                                result = re.search(r'\d{1,3}руб за час', text)
                                                currency = 'RUB'
                                                if result == None:
                                                    result = re.search(r'\d{1,3} руб за час', text)
                                                    currency = 'RUB'
                                                    if result == None:
                                                        result = re.search(r'\d{1,3}\$/hr', text)
                                                        currency = 'USD'
                                                        if result == None:
                                                            return None
                                                        salary = result.group(0)[:-4]
                                                    else:
                                                        salary = result.group(0)[:-11]
                                                else:
                                                    salary = result.group(0)[:-10]
                                            else:
                                                salary = result.group(0)[:-3]
                                        else:
                                            salary = result.group(0)[:-4]
                                    else:
                                        salary = result.group(0)[:-5]
                                else:
                                    salary = result.group(0)[:-6]
                            else:
                                salary = result.group(0)[:-7]
                        else:
                            salary = result.group(0)[:-8]
                    else:
                        salary = result.group(0)[:-5]
                else:
                    salary = result.group(0)[:-6]
            else:
                salary = result.group(0)[:-3]
        else:
            salary = result.group(0)[:-8]
    else:
        salary = result.group(0)[:-4]

    return {"value": salary, "currency": currency, "period": "HOUR"}

def searchSalary5(text):
    result = re.search(r'\$\d{1,4}', text)
    salary = ''
    if result == None:
        return None
    salary = result.group(0)[1:]
    return {"value": salary, "currency": "USD"}

def searchSalary1(text):
    result = re.search(r'Зарплата: \d{3,7}', text)
    if result == None:
        return {}
    salary_text = result.group(0)
    useless_length = 10

    all_length = len(salary_text)
    return {"value": salary_text[slice(useless_length, all_length)]}

def searchSalary3(text):
    result = re.search(r'\d{1,3} т.р.', text)
    salary = ''
    if result == None:
        result = re.search(r'\d{1,3}т.р.', text)
        if result == None:
            result = re.search(r'\d{1,3}К', text)
            if result == None:
                result = re.search(r'\d{1,3}тр', text)
                if result == None:
                    result = re.search(r'\d{1,3}K', text)
                    if result == None:
                        result = re.search(r'\d{1,3}K', text)
                        if result == None:
                            result = re.search(r'\d{1,3}к', text)
                            if result == None:
                                result = re.search(r'\d{1,3}k', text)
                                if result == None:
                                    result = re.search(r'\d{1,3} 000', text)
                                    if result == None:
                                        result = re.search(r'\d{1,3}\.000', text)
                                        # if result == None:
                                        #     result = re.search(r'\d{1,3}000', text)
                                        if result == None:
                                            return None
                                            # salary = result.group(0)[:-3]
                                        else:
                                            salary = result.group(0)[:-4]
                                    else:
                                        salary = result.group(0)[:-4]
                                else:
                                    salary = result.group(0)[:-1]
                            else:
                                salary = result.group(0)[:-1]
                        else:
                            salary = result.group(0)[:-1]
                    else:
                        salary = result.group(0)[:-1]
                else:
                    salary = result.group(0)[:-2]
            else:
                salary = result.group(0)[:-1]
        else:
            salary = result.group(0)[:-4]
    else:
        salary = result.group(0)[:-5]

    return {"value": salary + '000', "currency": "RUB"}

def searchSalary2(text): # this function need because parser does not can parse
# "тыс." and "тысяч"
    result = re.search(r'\d{1,3} тыс.', text)
    if result == None:
        result = re.search(r'\d{1,3} тысяч', text)
        if result == None:
            return None
        else:
            return {"value": result.group(0)[:-6] + '000', "currency": "RUB"}
    
    return {"value": result.group(0)[:-5] + '000', "currency": "RUB"}

def getTags(text, tag_list):
    if text == None:
        return {}
    RULE = morph_pipeline(tag_list)
    mentioned_tags = []
    parser = Parser(RULE)
    morph = pymorphy2.MorphAnalyzer()
    for match in parser.findall(text):
        try:
            value = match.tokens[0].value
            normalized_value =  morph.parse(value)[0].normal_form
            if normalized_value in mentioned_tags:
                continue
            mentioned_tags.append(normalized_value)
        except:
            print('Salary parser error')
    return mentioned_tags
    


