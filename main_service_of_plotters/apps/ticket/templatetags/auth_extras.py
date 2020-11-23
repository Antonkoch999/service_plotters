"""This module adding tag to check users group."""

from django import template

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    """Checks if the user has a group.

    :param user: request user
    :param group_name: name of user group
    :return: true or false
    """
    return user.groups.filter(name=group_name).exists()
