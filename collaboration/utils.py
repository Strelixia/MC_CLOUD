from django.core.mail import EmailMessage
from django.template.loader import render_to_string

def send_email(owner, collaborator, subject, template_name, reset_url):               
    email_html_content = render_to_string(template_name, {
        'owner': owner.username,
        'reset_url': reset_url
    })

    email = EmailMessage(
        subject = subject,
        body = email_html_content,
        from_email = owner,
        to =  [collaborator.email],
    )

    email.content_subtype = "html"
    email.send()