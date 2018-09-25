from django.conf import settings
from common.models import User, UserUrl, DomainUrl
from django.core.mail import send_mail
 
class YummyMailer():

    def find_changed_url(self):
    	domain_url = []
    	for changed_url in DomainUrl.objects.filter(has_change__exact = 1):
    	    domain_url.append(changed_url.id)
    	return domain_url

    def send_mail_by_url(self, url_id):
        user = UserUrl.objects.filter(url__exact = url_id)
        user_email = []
        for user_url in user:
            user_email.append(User.objects.filter(pk__exact = user_url.user_id).get().email)

        if len(user_email) > 0:
            send_mail(
                subject = 'Yummy Spam : 새로운 공지가 업데이트 되었습니다.',
                message = DomainUrl.objects.filter(pk__exact = url_id).get().url+' 에서 새로운 공지가 업데이트 되었습니다.',
                from_email = settings.EMAIL_HOST_USER,
                recipient_list = user_email,
                fail_silently = False,
            )

    def update_has_change(self, url_id):
        DomainUrl.objects.filter(pk__exact = url_id).update(has_change = False)

    def send(self):
        url = self.find_changed_url()
        for _id in url:
            self.send_mail_by_url(_id)
            self.update_has_change(_id)