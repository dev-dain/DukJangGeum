"""
이 모듈은 카카오톡 메시지 요청에 대한 응답 메시지를 출력한다.

사용 변수 목록
message
return_json_str
return_str (str)
wday_arr (list)
go_main_button (str)
today_wday (int)
today_now (datetime.datetime)
file_path (str)
in_fp (_io.TextIOWrapper)
temp_list (list)
line (str)
temp_str (str)
meal_list (list)
add_text (str)
i (int)
j (int)
day (dict)
date (dict)

"""
# Import
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from time import localtime
from datetime import datetime
import json


# Create your views here.
# Views function
def keyboard(request):
    """
    사용자가 채팅을 최초 요청했을 때 보인다.

    """
    return JsonResponse(
    {
        'type': 'buttons',
        'buttons': ['오늘','내일', '요일지정', '상시메뉴', '기타문의']
    }
)

@csrf_exempt
def message(request):
    """
    keyboard나 request 함수에서 얻은 message 요청에 대응해 응답을 전송한다.
    '오늘'-'초기화면'
    '내일'-'초기화면'
    '요일지정'-'월', '화', '수', '목', '금'-'초기화면'
    '상시메뉴'-'초기화면'
    '기타문의'-'초기화면'

    """
    message = ((request.body).decode('utf-8'))
    return_json_str = json.loads(message)
    return_str = return_json_str['content']

    wday_arr = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
    go_main_button = '초기화면'
    today_wday = localtime().tm_wday
    today_now = datetime.now()
    file_path = '/home/ubuntu/myproject/haksik/weekMeal.txt'
    # open에는 full 경로 설정 필수
    in_fp = open(file_path, 'r', encoding='utf-8')
    
    temp_list = []
    for line in in_fp.readlines():
        temp_list.append(line)
    
    temp_str = ''
    for line in temp_list:
        temp_str += line

    temp_str = temp_str.strip('\n')
    meal_list = []
    meal_list = temp_str.split('\n\n')
    in_fp.close()
    
    for i in range(8, 15):
        if meal_list[i]=='\xa0' or meal_list[i]=='\r\r' or len(meal_list[i])<12:
            meal_list[i]+='학식이 없는 날이거나 홈페이지에 등록되지 않았습니다.'
    add_text=''

    for i in range(8, 13):
        for j in range(len(meal_list[i])):
            if meal_list[i][j]=='*':
                if j==0:
                    add_text+='학식 제공시간: 11:00~18:30\n:: 4000원 ::\n'
                else:
                    add_text+='<택1>\n\n학식 제공시간: 11:00~14:00\n:: 5000원 ::\n'
                add_text+=meal_list[i][j]
            else:
                add_text+=meal_list[i][j]
        meal_list[i]=add_text
        add_text=''

    day = {'mon': meal_list[8], 'tue': meal_list[9], 'wed': meal_list[10], 
            'thu': meal_list[11], 'fri': meal_list[12], 'every': meal_list[14]}
    date = {'mon': meal_list[2], 'tue': meal_list[3], 'wed': meal_list[4],
            'thu': meal_list[5], 'fri': meal_list[6]}
    
    # 분기문
    if return_str=='오늘':
        if wday_arr[today_wday]=='sat' or wday_arr[today_wday]=='sun':
            return JsonResponse(
            {
                'message': {
                    'text': '오늘은 주말입니다! :D'
                },
                'keyboard': {
                    'type': 'buttons',
                    'buttons': [go_main_button]
                }
            }
        )
        else:
            return JsonResponse(
            {
                'message': {
                    'text': ''+today_now.strftime('%m월 %d')+'일\n'\
                            '오늘의 학식입니다.\n\n'+
                            day[wday_arr[today_wday]]
                },
                'keyboard': {
                    'type': 'buttons',
                    'buttons': [go_main_button]
                }
            }
        )

    elif return_str=='내일':
        if wday_arr[today_wday]=='fri' or wday_arr[today_wday]=='sat':
            return JsonResponse(
            {
                'message': {
                    'text': '내일은 주말입니다. :)'
                },
                'keyboard': {
                    'type': 'buttons',
                    'buttons': [go_main_button]
                }
            }
        )
        else:
            return JsonResponse(
            {
                'message': {
                    'text': today_now.strftime('%m월 ')+
                            date[wday_arr[(today_wday+1)%7]]+'\n'+
                            '내일 학식입니다.\n\n'+ 
                            day[wday_arr[(today_wday+1)%7]]
                },
                'keyboard': {
                    'type': 'buttons',
                    'buttons': [go_main_button]
                }
            }
        )

    elif return_str=='요일지정':
        return JsonResponse(
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

    elif return_str=='상시메뉴':
        return JsonResponse(
        {
            'message': {
                'text': '상시메뉴입니다.\n\n'\
                        '학식 제공시간: 10:00~18:30\n:: 4000원 ::\n'\
                        ''+day['every']+'\n<택1>'
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': [go_main_button]
            }
        }
    )

    elif return_str=='기타문의':
        return JsonResponse(
        {
            'message': {
                'text': '안녕하세요?\n'\
                        '덕성여대 학식알리미를 사용해주셔서 감사합니다.\n\n'\
                        '문의 및 건의사항이나 피드백은 '\
                        'dev.jaimie@gmail.com으로 제목에 [덕성학식]을 붙여 '\
                        '메일을 보내주시기 바랍니다.\n좋은 하루 되세요. ^^'
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': [go_main_button]
            }
        }
    )

    elif return_str=='초기화면':
        return JsonResponse(
        {
            'message': {
                'text': '초기화면입니다. 날짜를 선택해주세요.'
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['오늘', '내일', '요일지정', '상시메뉴', '기타문의']
            }
        }
    )

    elif return_str=='월':
        return JsonResponse(
        {
            'message': {
                'text': today_now.strftime('%m월 ')+date['mon']+
                        ' 학식입니다.\n\n'+day['mon']
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': [go_main_button]
            }
        }
    )

    elif return_str=='화':
        return JsonResponse(
        {
            'message': {
                'text': today_now.strftime('%m월 ')+date['tue']+
                        ' 학식입니다.\n\n'+day['tue']
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': [go_main_button]
            }
        }
    )

    elif return_str=='수': 
        return JsonResponse(
        {
            'message': {
                'text': today_now.strftime('%m월 ')+date['wed']+
                        ' 학식입니다.\n\n'+day['wed']
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': [go_main_button]
            }
        }
    )

    elif return_str=='목':
        return JsonResponse(
        {
            'message': {
                'text': today_now.strftime('%m월 ')+date['thu']+
                        ' 학식입니다.\n\n'+day['thu']
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': [go_main_button]
            }
        }
    )

    elif return_str=='금':
        return JsonResponse(
        {
            'message': {
                'text': today_now.strftime('%m월 ')+date['fri']+
                        ' 학식입니다.\n\n'+day['fri']
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': [go_main_button]
            }
        }
    )

    else:
        return JsonResponse(
        {
            'message': {
                'text': '개발 중이거나 오류입니다.'\
                        '관리자에게 문의해주세요.'
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': [go_main_button]
            }
        }
    )
