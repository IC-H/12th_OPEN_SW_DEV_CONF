from user.backend.mail.mail import find_changed_url, send_mail_by_url


if ## When?:
    url = find_changed_url()

    for _id in url:
	    send_mail_by_url(_id)
