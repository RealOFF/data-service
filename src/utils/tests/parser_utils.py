from src.utils.parser_utils import searchSalary3, searchSalary4, searchSalary5, getSalary

def searchSalaryTest():
    assert searchSalary3('Текст 300 т.р.') == {"value": '300000', "currency": "RUB"}, '"300 т.р." searchSalary3 test filed'

    text1 = '8$ за час'
    text2 = '8$/ч'
    text3 = '8$/час'
    text4 = '8 $/час'
    text5 = '8 руб/час'
    text6 = '8 руб/ч'
    text7 = '8руб/ч'
    text8 = '8р/ч'
    text9 = '8 р/ч'
    text10 = '8 руб за час'
    result1 = searchSalary4(text1)
    result2 = searchSalary4(text2)
    result3 = searchSalary4(text3)
    result4 = searchSalary4(text4)
    result5 = searchSalary4(text5)
    result6 = searchSalary4(text6)
    result7 = searchSalary4(text7)
    result8 = searchSalary4(text8)
    result9 = searchSalary4(text9)
    result10 = searchSalary4(text10)

    assert result1 == {"value": '8', "currency": "USD", "period": "HOUR"}, 'searchSalary4 test failed'
    assert result2 == {"value": '8', "currency": "USD", "period": "HOUR"}, 'searchSalary4 test failed'
    assert result3 == {"value": '8', "currency": "USD", "period": "HOUR"}, 'searchSalary4 test failed'
    assert result4 == {"value": '8', "currency": "USD", "period": "HOUR"}, 'searchSalary4 test failed'
    assert result5 == {"value": '8', "currency": "RUB", "period": "HOUR"}, 'searchSalary4 test failed'
    assert result6 == {"value": '8', "currency": "RUB", "period": "HOUR"}, 'searchSalary4 test failed'
    assert result7 == {"value": '8', "currency": "RUB", "period": "HOUR"}, 'searchSalary4 test failed'
    assert result8 == {"value": '8', "currency": "RUB", "period": "HOUR"}, 'searchSalary4 test failed'
    assert result9 == {"value": '8', "currency": "RUB", "period": "HOUR"}, 'searchSalary4 test failed'
    assert result10 == {"value": '8', "currency": "RUB", "period": "HOUR"}, 'searchSalary4 test failed'

    text11 = 'SENIOR MOBILE ADOBE AIR DEVELOPERФормат: #удаленкаЗанятость: ПолнаяОпыт: от 5 летЯзык: #английскийЗарплата: от $3000Компания:'
    result11 = searchSalary5(text11)
    assert result11 == {"value": '3000', "currency": "USD"}, 'searchSalary5 test failed'

    text12 = '''
        Город: Москва (Сокольники или Павелецкая), есть релокационный пакет

Формат работы: офис, возможна удаленка через полгода работы 

Занятость: полная

Вилка: 180-250 т.р. на руки

Ищем коллегу для создания и развития современного сервиса дистанционных банковских услуг.

• SPA приложение на Angular 8

• Пишем на TypeScript, ES6 Modules, SASS

• Собираем в Webpack

• Храним в Git

Также готовы рассматривать кандидатов, которые пишут на React, но хотели бы перейти на Angular.
'''

    result12 = getSalary(text12)

    assert result12 == {"value": '250000', "currency": "RUB"}, 'getSalary test failed'

    text13 = 'Менеджер по продажам на вводном уроке в Кодиум от 30000 до 45000 рублей'

    result13 = getSalary(text13)

    assert result13 == {"value": 45000, "currency": "RUB"}, 'getSalary test failed'