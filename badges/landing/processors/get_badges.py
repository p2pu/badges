from badge.models import get_published_badges
from badge.models import get_badge
from badge.models import get_featured_badges
from badge.models import last_n_published_badges
from project.processors import get_badge_uri_by_number_of_projects, sort_badge_uris_by_attached_projects
from badge.view_helpers import fetch_badge_resources


def get_filtered_badges(option):

    if option == 'popular':
        badges = []
        items = sort_badge_uris_by_attached_projects()[:12]
        for item in items:
            badges.append(get_badge(item['badge_uri']))
    elif option == 'new':
        badges = last_n_published_badges(12)
    elif option == 'featured':
        badges = get_featured_badges()
    else:
        badges = get_published_badges()

    return map(fetch_badge_resources, badges)