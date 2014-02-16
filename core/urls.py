# -*- coding: utf-8 -*-
# core.urls
# 

# Following few lines is an example urlmapping with an older interface.

from kay.routing import (
  ViewGroup, Rule
)

view_groups = [
  ViewGroup(
    Rule('/', endpoint='index', view='core.views.index'),
    Rule('/post', endpoint='post', view='core.views.post'),
    Rule('/code/<int:id>', endpoint='show', view='core.views.show'),
  )
]

