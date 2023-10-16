from django.urls import reverse


def get_menu_items():
    menu_items = [
        {"title": "Helpy", "url": reverse("index")},
        {"title": "Offer help", "url": reverse("offer_help")},
        {"title": "Articles", "url": reverse("articles")},
        {"title": "Events", "url": reverse("events")},
        {"title": "About", "url": reverse("about")},
    ]
    return menu_items
