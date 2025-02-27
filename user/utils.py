from django.core.mail import EmailMessage
from django.template.loader import render_to_string

def send_email(user, admin_email, subject, template_name, reset_url):               
    email_html_content = render_to_string(template_name, {
        'user': user.username,
        'reset_url': reset_url
    })

    email = EmailMessage(
        subject = subject,
        body = email_html_content,
        from_email = admin_email,
        to =  [user.email],
    )

    email.content_subtype = "html"
    email.send()