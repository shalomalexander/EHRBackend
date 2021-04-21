from background_task import background
from .models import User
from logging import getLogger

logger = getLogger(__name__)
@background(schedule=5)
def notify_user():
    # lookup user by id and send them a message
    # user = User.objects.get(pk=user_id)
    # user.email_user('Here is a notification', 'You have been notified')
    queryset = User.objects.filter(verified_field=False)
    print(queryset)
    return 
    # for q in queryset:
    #     if q.verified_field == False:
    #        User.objects.filter(username=queryset.username).delete()