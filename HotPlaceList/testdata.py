from hotplist.models import HotPlaces
from django.utils import timezone


for i in range(300):
    HP = HotPlaces(name="테스트데이터입니다:[%03d]" %i, address='테스트데이터', phone_num = None, original_rating = 5.0, rating = 5.0, image = '4xcl35J.jpeg', author = None)


    HP.save()