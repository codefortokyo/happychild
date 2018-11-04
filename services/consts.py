import datetime

SHINAGAWA_WARD_ID = 9
# TODO: managed by DataBase? :thinking_face:
SHINAGAWA_OPEN_DATA = {
    'modified_date': datetime.date(2018, 10, 10),
    'url': 'http://www.city.shinagawa.tokyo.jp/contentshozon/889.csv'
}

AGE_LABELS = {
    1: ['0', '0歳', '0歳児', '０歳児', '57日', '7か月'],
    2: ['1', '1歳', '1歳児', '１歳児'],
    3: ['2', '2歳', '2歳児', '２歳児'],
    4: ['3', '3歳', '3歳児', '３歳児'],
    5: ['4', '4歳', '4歳児・5歳児', '4歳児以上', '４歳児'],
    6: ['5', '5歳', '延長', '５歳児'],
    7: ['3歳児・4歳児・5歳児', '2?5歳児']
}
