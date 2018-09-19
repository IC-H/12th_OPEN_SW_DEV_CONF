from common.models import User, UserUrl, DomainUrl
from django.core.mail import send_mail


def find_changed_url():
	domain_url = []
	for changed_url in DomainUrl.objects.filter(has_changed = 1)
	    domain_url.append(changed_url.id)
	return domain_url

def send_mail_by_url(url_id):
	url_id = 1
    user_email = []
    for user_url in UserUrl.objects.filter(url__exact = url_id):
        user_email.append(User.objects.filter(pk__exact = user_url.user_id).get().email)

    if len(user_email) > 0
        send_mail(
            subject = 'Yummy_spam  : The Url you choiced has changed',
            message = 'The Url you choiced has changed'+DomainUrl.objects.filter(pk__exact = url_id).get().url,
            from_email = 'webmaster@yummyspam.com',
            recipient_list = [user_email],
            fail_silently = False,
        )

def send_to_user():
    url = find_changed_url()

    for _id in url:
	    send_mail_by_url(_id)
