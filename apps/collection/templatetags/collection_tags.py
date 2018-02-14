from django import template
from django.template.loader import render_to_string, select_template
import settings

register = template.Library()


@register.simple_tag(takes_context=True)
def render_collection(context, product):
    """
    Render a product snippet as you would see in a browsing display.

    This templatetag looks for different templates depending on the UPC and
    product class of the passed product.  This allows alternative templates to
    be used for different product classes.
    """
    names = ['catalogue/partials/product/upc-%s.html' % product.upc,
             'catalogue/partials/product/class-%s.html' % product.get_product_class().slug,
             'catalogue/partials/collection.html']
    template_ = select_template(names)
    # Ensure the passed product is in the context as 'product'
    context['product'] = product
    return template_.render(context)

@register.simple_tag(takes_context=True)
def render_item_no_style(context, collection_items):
    names = ['collection/design/collection_item_no_style.html']
    template_ = select_template(names)
    context['collection_items'] = collection_items
    return template_.render(context)


@register.simple_tag(takes_context=True)
def render_item_need_style(context, collection_items):
    names = ['collection/design/collection_item_need_style.html']
    template_ = select_template(names)
    context['collection_items'] = collection_items
    return template_.render(context)


@register.simple_tag(takes_context=True)
def render_user_template(context, user, type, form_url, header_text, button_text):
    names = ['collection/user_template.html']
    template_ = select_template(names)
    context['selected_user'] = user
    context['type'] = type
    context['header_text'] = header_text
    context['form_url'] = form_url
    context['button_text'] = button_text
    context['avatar_dir'] = settings.AVATAR_DIR
    return template_.render(context)


@register.simple_tag(takes_context=True)
def render_alert(context, id, header_text, url, btn_text, type, modal):
    names = ['collection/alert.html']
    template_ = select_template(names)
    context['collection_id'] = id
    context['btn_text'] = btn_text
    context['modal'] = modal
    context['header_text'] = header_text
    context['url'] = url
    context['type'] = type
    return template_.render(context)

@register.simple_tag(takes_context=True)
def render_product_template(context, collection):
    names = ['collection/product_template.html']
    template_ = select_template(names)
    context['collection'] = collection
    return template_.render(context)