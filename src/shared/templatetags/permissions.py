from django import template

register = template.Library()


class CanNode(template.Node):

    def __init__(self, permission, nodelist):
        self.permission = permission
        self.nodelist = nodelist

    def render(self, context):
        request = context["request"]
        user = request.user

        if not user.is_authenticated:
            return ""

        if not user.has_perm(self.permission):
            return ""

        return self.nodelist.render(context)


@register.tag
def can(parser, token):
    bits = token.split_contents()

    if len(bits) != 2:
        raise template.TemplateSyntaxError(
            "can requires exactly one permission."
        )

    permission = bits[1].strip("\"'")

    nodelist = parser.parse(("endcan",))
    parser.delete_first_token()

    return CanNode(permission, nodelist)