from django.core.mail import EmailMessage
from django.template.loader import render_to_string

def send_email(owner, collaborator, subject, template_name, inviting_url):               
    email_html_content = render_to_string(template_name, {
        'owner_email': owner.email,
        'owner_name': owner.username,
        'inviting_url': inviting_url,
        'collaborator': collaborator
    })

    email = EmailMessage(
        subject = subject,
        body = email_html_content,
        from_email = owner.email,
        to =  [collaborator],
    )

    email.content_subtype = "html"
    email.send()
    