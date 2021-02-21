from django.core.mail import send_mass_mail

import watchlist.watchlist.settings as settings
from watchlist.strainer.models import User


def format_email(email):
    user = User.objects.filter(email__exact=email).values('email','radar')[0]
    return("Alteração no Radar financeiro", 
           f"As suas novas recomendações de compra são \n {user['radar']}",
           settings.EMAIL_HOST_USER, 
           [user['email']])


def send_email_to(users):
    send_mass_mail(
                   tuple(list(map(format_email, users))),
                   fail_silently=False
    )
    pass
