from django import template

register = template.Library()

def uploadsleft(value, arg):
  left = value - arg.count()
  if left < 0:
    return 0
  return left

register.filter('uploadsleft', uploadsleft)
