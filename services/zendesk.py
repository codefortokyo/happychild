from django.conf import settings
from zenpy.lib.api_objects import Ticket, User


def create_ticket(username: str, email: str, title: str, description: str):
    settings.ZENPY_CLIENT.tickets.create(
        Ticket(title=title, description=description,
               requester=User(name=username, email=email))
    )
