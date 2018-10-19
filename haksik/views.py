# Import #
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from time import localtime
from datetime import datetime
import json

# var list #
wArr = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

# Create your views here.

def keyboard(request) :
    return JsonResponse(
    {
        'type': 'buttons',
        'buttons': ['오늘','내일', '요일지정', '상시메뉴', '기타문의']
    }
)

@csrf_exempt
def message(request) :
    message = ((request.body).decode('utf-8'))
    returnJsonStr = json.loads(message)
    returnStr = returnJsonStr['content']
    
    todayW = localtime().tm_wday
    todayD = datetime.now()

    inFp = open("/home/ubuntu/myproject/haksik/weekMeal.txt", "r", encoding = "utf-8")
    # open에는 경로 설정 필수#
    oldList = []
    for inline in inFp.readlines() :
        oldList.append(inline)
    
    tempStr = ''
    for line in oldList :
        tempStr += line

    tempStr = tempStr.strip('\n')
    newList = []
    newList = tempStr.split('\n\n')

    inFp.close()

    weekMeal = newList
    
    for i in range(8, 15) :
        if weekMeal[i]=='\xa0' or weekMeal[i]=='\r\r' or len(weekMeal[i])<12 :
            weekMeal[i]+='\n학식이 없는 날이거나 홈페이지에 등록되지 않았습니다.'

    nstr=''

    for j in range(8, 13) :
        for k in range(len(weekMeal[j])) :
            if weekMeal[j][k]=='*' :
                if k==0 :
                    nstr+='학식 제공시간: 11:00~18:30\n:: 4000원 ::\n'
                else :
                    nstr+='<택1>\n\n학식 제공시간: 11:00~14:00\n:: 5000원 ::\n'
                nstr+=weekMeal[j][k]
            else :
                nstr+=weekMeal[j][k]
        weekMeal[j]=nstr
        nstr=''

    day = {'mon': weekMeal[8], 'tue': weekMeal[9], 'wed': weekMeal[10], 'thu': weekMeal[11], 'fri': weekMeal[12], 'every': weekMeal[14]}

    # 분기문 #

    if returnStr == "오늘" :
        if wArr[todayW] == 'sat' or wArr[todayW] == 'sun' :
            return JsonResponse (
            {
                'message': {
                    'text': '오늘은 주말입니다! :D'
                },
                'keyboard': {
                    'type': 'buttons',
                    'buttons': ['초기화면']
                }
            }
        )
        else :
            return JsonResponse (
            {
                'message': {
                    'text': ''+todayD.strftime('%Y년 %m월 %d')+'일\n오늘의 학식입니다.\n\n'+day[wArr[todayW]]+''
                },
                'keyboard': {
                    'type': 'buttons',
                    'buttons': ['초기화면']
                }
            }
        )

    elif returnStr == "내일" :
        if wArr[todayW] == 'fri' or wArr[todayW] == 'sat' :
            return JsonResponse (
            {
                'message': {
                    'text': '내일은 주말입니다. :)'
                },
                'keyboard': {
                    'type': 'buttons',
                    'buttons': ['초기화면']
                }
            }
        )
        else :
            return JsonResponse (
            {
                'message': {
                    'text': '내일 학식입니다.\n\n'+day[wArr[(todayW+1)%7]]+''
                },
                'keyboard': {
                    'type': 'buttons',
                    'buttons': ['초기화면']
                }
            }
        )

    elif returnStr == "요일지정" :
        return JsonResponse (
        {
            'message': {
                'text': '요일을 선택하세요.'
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['월', '화', '수', '목', '금']
            }
        }
    )

    elif returnStr == "상시메뉴" :
        return JsonResponse (
        {
            'message': {
                'text': '상시메뉴입니다.\n\n학식 제공시간: 10:00~18:30\n:: 4000원 ::\n'+day['every']+'\n<택1>'
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['초기화면']
            }
        }
    )

    elif returnStr == "기타문의" :
        return JsonResponse (
        {
            'message': {
                'text': '안녕하세요?\n덕성여대 학식알리미를 사용해주셔서 감사합니다.\n\n문의 및 건의사항이나 피드백은 dev.jaimie@gmail.com으로 제목에 [덕성학식]을 붙여 메일을 보내주시기 바랍니다.\n좋은 하루 되세요. ^^',
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['초기화면']
            }
        }
    )

    elif returnStr == "초기화면" :
        return JsonResponse (
        {
            'message': {
                'text': '초기화면입니다. 날짜를 선택해주세요.'
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['오늘', '내일', '요일지정', '상시메뉴',  '기타문의']
            }
        }
    )

    elif returnStr == '월' :
        return JsonResponse (
        {
            'message': {
                'text': '월요일 학식입니다.\n\n'+day['mon']+''
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['초기화면']
            }
        }
    )

    elif returnStr == '화' :
        return JsonResponse (
        {
            'message': {
                'text': '화요일 학식입니다.\n\n'+day['tue']+''
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['초기화면']
            }
        }
    )

    elif returnStr == '수': 
        return JsonResponse (
        {
            'message': {
                'text': '수요일 학식입니다.\n\n'+day['wed']+''
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['초기화면']
            }
        }
    )

    elif returnStr == '목':
        return JsonResponse (
        {
            'message': {
                'text': '목요일 학식입니다.\n\n'+day['thu']+''
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['초기화면']
            }
        }
    )

    elif returnStr == '금' :
        return JsonResponse (
        {
            'message': {
                'text': '금요일 학식입니다.\n\n'+day['fri']+''
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['초기화면']
            }
        }
    )

    else :
        return JsonResponse (
        {
            'message': {
                'text': '개발 중이거나 오류입니다. 관리자에게 문의해주세요.'
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['초기화면']
            }
        }
    )

