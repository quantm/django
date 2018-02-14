import json
import settings
from io import StringIO
from .models import *
import datetime
from django.shortcuts import redirect
from django.utils.timezone import utc
from apps.collection.models import *
from django.views.generic import ListView, FormView, DetailView, DeleteView
from django.template import RequestContext
from django.shortcuts import render_to_response, HttpResponse
from .forms import CollectionForm
from django.contrib.auth.models import User
from django.contrib import messages
from oscar.apps.customer.mixins import PageTitleMixin
from apps.catalogue.models import Product, ProductImage, Category
from apps.customer.models import Notification
from apps.common.functions import send_message
from apps.common.models import Message_Type
from itertools import chain
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.db.models import Count


class ViewCollectionComment(ListView):
    context_object_name = 'list_comment'
    template_name = 'collection/collection_comment.html'

    def get_context_data(self, **kwargs):
        context = super(ViewCollectionComment, self).get_context_data(**kwargs)
        context['name'] = self.request.user.get_full_name()
        context['comment_list'] = CollectionComment.objects.filter(set_id=self.request.GET['set_id'])
        context['avatar_dir'] = settings.UPLOAD_DIR+'avatar'
        save_comment(self.request)
        return context

    def get_queryset(self):
        return


class ViewCollection(ListView):
    context_object_name = 'collection'
    template_name = 'collection/load_designed.html'

    def get_context_data(self, **kwargs):
        context = super(ViewCollection, self).get_context_data(**kwargs)
        collection_id = self.request.GET.get('set_id', '')
        mode = self.request.GET.get('mode', '')
        collection_user = CollectionSet.objects.get(id=collection_id)

        if mode == "delete":
            collection_user.delete()
            messages.error(self.request, "Collection Deleted")
            return context

        context['collection_name'] = CollectionSet.objects.filter(id=collection_id)
        context['comment_list'] = CollectionComment.objects.filter(set_id=collection_id)
        context['user_name'] = User.objects.filter(id=collection_user.user_id)
        context['user_array'] = User.objects.exclude(id=collection_user.user_id)
        context['id_user_comment'] = self.request.user.id
        context['set_id'] = collection_id
        context['avatar'] = settings.UPLOAD_DIR+'avatar/'+str(collection_user.user_id)+'_avatar.png'
        return context

    def get_queryset(self):
        collection_id = self.request.GET.get('set_id', '')
        qs = CollectionSetElement.objects.filter(set_id=collection_id).exclude(style='').order_by('id')
        return qs


class ProductListCollection(ListView):
    context_object_name = 'collection'
    template_name = 'collection/product.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductListCollection, self).get_context_data(**kwargs)
        query_search = self.request.GET.get('q', '')
        context['id_u'] = self.request.user.id
        context['count'] = self.get_queryset().count()
        if query_search == '':
            context['search'] = ''
            context['display'] = 'none'
        else:
            context['search'] = query_search
            context['display'] = ''

        collection_id = self.request.GET.get('set_id', '')
        right_items = None
        if 'right_items' in self.request.GET:
            right_items = self.request.GET.get('right_items', '')

        context['collection_status'] = None
        context['collection_items'] = None
        context['c_pk'] = "0"
        if collection_id is not None and collection_id != "":
            if collection_id.isnumeric():
                collection = CollectionSet.objects.get(pk=collection_id)
                context['current_collection'] = collection
                if right_items is None or right_items == 0 or right_items == '0':
                    context['collection_items'] = CollectionSetElement.objects.filter(set=collection).exclude(style='')
                    right_panel_items = CollectionSetElement.objects.filter(set=collection, style='').values('product')
                    context['collection'] = Product.objects.filter(pk__in=right_panel_items)
                else:
                    context['is_new'] = "1"
                    context['pk_co_edited'] = collection_id
                    context['collection_items'] = CollectionSetElement.objects.filter(set=collection).exclude(style='')

        return context

    def get_queryset(self):
        filter_query = self.request.GET.get('q', '')
        qs = Product.objects.filter(title__contains=filter_query)
        return qs


class Search(ListView):
    context_object_name = 'result'
    template_name = 'collection/fetch_ajax.html'
    model = Product

    def get_queryset(self):
        filter_query = self.request.GET.get('q', '')
        qs = Product.objects.filter(title__contains=filter_query)
        return qs

    def get_context_data(self, **kwargs):
        context = super(Search, self).get_context_data(**kwargs)
        query_search = self.request.GET.get('q', '')

        if query_search == '':
            context['search'] = ''
            context['display'] = 'none'
        else:
            qs = self.get_queryset().count()
            if qs == 0:
                context['display'] = 'none'
                context['re'] = 'No product found'
            else:
                context['search'] = query_search
                context['display'] = ''

        return context


class CategoryListView(ListView):
    context_object_name = 'category'
    template_name = 'collection/category.html'
    model = Category

    def get_queryset(self):
        filter_query = self.request.GET.get('q', '')
        qs = Category.objects.all()
        return qs

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        query_search = self.request.GET.get('q', '')
        if query_search == '':
            context['search'] = ''
            context['display'] = 'none'
        else:
            context['search'] = query_search
            context['display'] = ''
        return context


#the content show in open list collection
class CollectionListView(ListView):
    template_name = 'collection/design/list_collections_on_popup.html'
    model = CollectionSet
    context_object_name = 'collections'

    def get_context_data(self, **kwargs):
        context = super(CollectionListView, self).get_context_data(**kwargs)
        context['collections'] = CollectionSet.objects.filter(user=self.request.user, status__in=['p', 'd']).order_by('id')
        return context

    def get_queryset(self):
        return super(CollectionListView, self).get_queryset().order_by('id')


class MyCollectionView(PageTitleMixin, ListView):
    context_object_name = active_tab = "my-collections"
    template_name = 'collection/my_collections.html'
    page_title = "MyCollection"
    model = CollectionSet

    def get_context_data(self, **kwargs):
        context = super(MyCollectionView, self).get_context_data(**kwargs)
        id_u = User.objects.get(pk=self.request.user.id)
        creator = CollectionSet.objects.filter(user=id_u, status__in=['c', 'd', 'p'])
        co_editor = CollectionSetEdit.objects.filter(editor=id_u, is_edited=1).select_related("set")
        if creator and not co_editor:
            context['my_collection'] = creator
            context['is_co_edit'] = "0"
        if co_editor and creator:
            context['my_collection'] = list(chain(creator, co_editor))
            context['is_co_edit'] = "1"
        if co_editor and not creator:
            context['my_collection'] = co_editor
            context['is_co_edit'] = "1"
        return context

    def get_queryset(self):
        return super(MyCollectionView, self).get_queryset().order_by('-create')


def collection_open_item(request, set_id=None):
    collection_items = CollectionSetElement.objects.filter(set_id=set_id).exclude(style='').order_by('id')
    return render_to_response('collection/design/collection_item_need_style.html',
                              {'collection_items': collection_items}, context_instance=RequestContext(request))


def save_share_collection(request):
    if request.method == "POST" and request.is_ajax():
        selected_user_array = request.POST.getlist('post_selected_user_array[]', '')
        set_id = request.POST.get('set_id', '')
        share_from_user_id = request.user.id
        fullname = request.user.get_full_name()
        subject = fullname + ' ' + 'has share collection with you'
        for share_u in selected_user_array:
            query_share = Notification(sender_id=share_from_user_id, recipient_id=share_u, location="Inbox",
                                       subject=subject, object_id=set_id, type=Message_Type._SHARE_COLLECTION)
            query_share.save()
    return HttpResponse(json.dumps(selected_user_array))


def save_invite_edit_collection(request):
    if request.method == "POST" and request.is_ajax():
        selected_user_array = request.POST.getlist('post_selected_user_array[]', '')
        set_id = request.POST.get('set_id', '')
        share_from_user_id = request.POST.get('user_invite', '')
        username = User.objects.filter(id=share_from_user_id)
        mail_subject = request.user.email + "`s invitation"
        site_url = request.get_host()
        mail_body = "<a href=http://"+site_url+"/collection/product/?set_id="+set_id+">"+"Click to edit collection</a>"
        for name in username:
            name_ = name.first_name + " " + name.last_name
        subject = name_+' '+'has invite you to edit collection'

        for share_u in selected_user_array:
            send_message(sender_id=share_from_user_id, recipient_id=share_u,subject=subject, body_html=mail_body,
                         object_id=set_id, type=Message_Type._INVITE_COLLECTION, sendmail=True)
            qs_co_edit = CollectionSet.objects.filter(id=set_id, user_id=share_u)
            if not qs_co_edit:
                CollectionSetEdit(editor=User.objects.get(pk=share_u),
                                  set=CollectionSet.objects.get(pk=set_id),
                                  date_create=datetime.datetime.utcnow().replace(tzinfo=utc),
                                  creator_id=share_from_user_id, is_edited=0).save()

        return HttpResponse(json.dumps(selected_user_array))


def collection_save(request):
    """
    Saves the note content and position within the table.
    """
    collection_form = CollectionForm(request.POST or None)
    if request.method == "POST" and request.is_ajax():
        if collection_form.is_valid():
            #Update Collection
            str_name = request.POST['name']
            status = request.POST['status']

            update_fields = []
            if 'pk' not in request.POST or request.POST['pk'] == 0 or request.POST['pk'] == '0':
                collection = CollectionSet(name=str_name, user=request.user, status=status, view=0)
                collection.save()
            else:
                collection = CollectionSet.objects.get(pk=request.POST['pk'])
                if str_name != '':
                    collection.name = str_name
                collection.status = status
                update_fields = ['name', 'status']
                collection.save(update_fields=update_fields)
            #Delete all item of Collection
            CollectionSetElement.objects.filter(set=collection).delete()

            #Re-Store items of Collection
            thumb = None
            for item in request.POST.getlist('items[]'):
                io_item = StringIO(item)
                item_value = json.load(io_item)

                product = Product.objects.get(pk=item_value['pid'])
                str_type = item_value['type']
                str_style = item_value['style']
                str_class = item_value['class']

                collection_item = CollectionSetElement(product=product, set=collection, type=str_type, style=str_style, class_name=str_class)
                collection_item.save()

                if thumb is None:
                    product_image = ProductImage.objects.filter(product=product)[0]
                    thumb = product_image.none_watermark

            if thumb is not None:
                collection.thumb = thumb
                collection.save(update_fields=['thumb'])

            open_collection_link = '/collection/list/?set_id=%d' % collection.pk

            msg = {
                'code': '1',
                'id': collection.pk,
                'message': '<p>Collection <b>%s</b> has been saved, please click <a href="%s" class="" target="_blank"> here </a> '
                           'to open your collection.</p>' % (request.POST['name'], open_collection_link)
            }
        else:
            msg = {
                'code': '0',
                'message': "AJAX post invalid",
            }
    else:
        msg = "GET petitions are not allowed for this view."
    return HttpResponse(json.dumps(msg))


def save_comment(request):
    if request.method == "GET" and request.is_ajax():
        set_id = CollectionSet.objects.get(pk=request.GET['set_id'])
        content = request.GET['text_comment']
        user_comment = request.user.get_full_name()
        comment = CollectionComment(set=set_id, content=content, user=request.user, user_comment=user_comment)
        comment.save()
    
    return HttpResponse()


def add_product_to_collection(request):
    if request.is_ajax():
        collection_pk = collection_name = product_id = None
        collection_status = 'l'
        if 'collection_pk' in request.POST:
            collection_pk = int(request.POST['collection_pk'])
        if 'collection_name' in request.POST:
            collection_name = request.POST['collection_name']
        if 'status' in request.POST:
            collection_status = request.POST['status']
        if 'product_id' in request.POST:
            product_id = int(request.POST['product_id'])

        if collection_pk is None or collection_pk == 0 or collection_pk == '0':
            thumb_string = u''
            if product_id is not None and product_id > 0:
                thumb = ProductImage.objects.filter(product_id=product_id)[0]
                thumb_string = thumb.none_watermark
            collection = CollectionSet(name=collection_name, user=request.user, thumb=thumb_string, status=collection_status)
            collection.save()
        else:
            collection = CollectionSet.objects.get(pk=collection_pk)


        if product_id is not None and product_id > 0:
            product = Product.objects.get(pk=product_id)
            product_in_collection = CollectionSetElement.objects.filter(product=product, set=collection).values('product')

            if {'product': product_id} not in product_in_collection:
                str_class = u'product not-clone'
                collection_items = CollectionSetElement.objects.filter(set=collection)
                str_style = u'position: relative; float: left; z-index: %d;' % (len(collection_items)+1)
                if collection.status == u'p' or collection.status == 'p':
                    str_style = u''
                collection_item = CollectionSetElement(product=product, set=collection, type='div', style=str_style, class_name=str_class)
                collection_item.save()
                msg = 'Product <b>%s</b> has been added to %s ' % (product.get_title(), collection.name)
            else:
                msg = 'Product <b>%s</b> already exist in %s ' % (product.get_title(), collection.name)

            if collection_status == u'l':
                str_url = '<a href="/collection/my-list/%d/" class="close-modal btn-link" target="_blank"> here </a>' % collection.pk
            else:
                str_url = '<a href="/collection/preview/%d/" class="close-modal btn-link" target="_blank"> here </a>' % collection.pk

            message = {'code': '1', 'collection_id': collection.pk, 'message': '<p>%s. You can click %s to view.</p>' % (msg, str_url)}
        else:
            message = {'code': '0', 'message': "AJAX post invalid"}
    else:
        message = {'code': '0', 'mes_box':"GET petitions are not allowed for this view."}
    return HttpResponse(json.dumps(message))

def update_edit(request):
    if request.is_ajax():
        update_fields = ['is_edited', 'editor_id']
        collection = CollectionSetEdit.objects.get(set_id=request.POST['set_id'], editor_id=request.user.id)
        collection.is_edited = "1"
        collection.save(update_fields=update_fields)
        return HttpResponse()


def gallery_save_into_collection(request):
    collection_id = request.POST.get('collection_id')
    new_name = request.POST.get('new_name')
    collection_obj = CollectionSet.objects.get(pk=collection_id)
    collection_obj.name = new_name
    collection_obj.save(update_fields=['name'])

    return redirect('/collection/product/?set_id=%d' % collection_obj.pk)


class MyCollectionForm(FormView):
    template_name = 'collection/forms/my_list_collection_form_of_add_product_modal.html'
    form_class = CollectionForm
    success_url = ''

    def get_context_data(self, **kwargs):

        collections = CollectionSet.objects.filter(user=self.request.user).exclude(status='e').order_by('-create')

        form_name = u'List'
        collections_from_session = None
        #get type option : is list or collection, is List if type==0, else is Collection
        if 'type' in self.request.GET:
            type = self.request.GET['type']
            if type == 'l' or type == u'l':
                collections = collections.filter(status='l')
                if 'ss_list' in self.request.session:
                    collections_from_session = self.request.session.get('ss_list')
            else:
                form_name = u'Collection'
                collections = collections.filter(status__in=['c', 'd', 'p'])
                if 'ss_collection' in self.request.session:
                    collections_from_session = self.request.session.get('ss_collection')

        #Get product id to assign to template
        product_id = None
        if 'product_id' in self.request.GET:
            product_id = self.request.GET['product_id']

        context = super(MyCollectionForm, self).get_context_data(**kwargs)
        context['product_id'] = product_id
        context['form_name'] = form_name
        context['collections'] = collections
        context['collections_from_session'] = collections_from_session

        return context

    def form_valid(self, form):
        return super(MyCollectionForm, self).form_valid(form)

class MyCollectionPreview(ListView):
    model = Product
    context_object_name = 'collection_preview'
    template_name = 'collection/preview_collection_before_go_design_page.html'

    def get_context_data(self, **kwargs):
        context = super(MyCollectionPreview, self).get_context_data(**kwargs)

        collection_id = int(self.kwargs['collection_id'])
        collection = CollectionSet.objects.get(pk=collection_id)
        context['pk'] = collection_id
        context['name'] = collection.name
        context['products'] = Product.objects.filter(pk__in=kwargs['object_list'])

        return context

    def get_queryset(self):
        return CollectionSetElement.objects.filter(set_id=int(self.kwargs['collection_id'])).values('product')


class MyListProfile(PageTitleMixin, ListView):
    model = CollectionSet
    context_object_name = active_tab = "my-list"
    template_name = 'collection/my_list/profile.html'
    page_title = _('My List')

    def get_context_data(self, **kwargs):
        context = super(MyListProfile, self).get_context_data(**kwargs)
        if 'object_list' in kwargs:
            context['my_list'] = kwargs['object_list']
        else:
            context['my_list'] = None
        return context

    def get_queryset(self):
        return CollectionSet.objects.annotate(num_product=Count('collectionsetelement')).filter(user=self.request.user, status='l')


class MyListDetail(PageTitleMixin, DetailView):
    context_object_name = active_tab = "my-list"
    page_title = ''
    model = CollectionSet
    template_name = 'collection/my_list/detail.html'

    def get_context_data(self, **kwargs):
        context = super(MyListDetail, self).get_context_data(**kwargs)

        context['items'] = CollectionSetElement.objects.filter(set_id=self.kwargs['pk']).select_related('product').extra(
            select={'thumb': 'none_watermark'},
            tables=['"catalogue_productimage" AS "image"'],
            where=["catalogue_product.id=image.product_id AND image.display_order=0"]
        )

        return context


class MyListDelete(PageTitleMixin, DeleteView):
    model = CollectionSet
    success_url = reverse_lazy('my-list-profile')
    template_name='collection/my_list/confirm_delete.html'
    page_title = _('Delete List')
    context_object_name = active_tab = "my-list"


def my_list_remove_item(request, list_pk=None, item_id=None):
    if request.is_ajax():
        CollectionSetElement.objects.filter(set_id=list_pk, pk=item_id).delete()
        message = {'code': '1', 'message': '<p class="success">Successful</p>'}
    else:
        message = {'message': "GET petitions are not allowed for this view."}
    return HttpResponse(json.dumps(message))


def delete_comment(request):
    if request.is_ajax():
        CollectionComment.objects.get(pk=request.POST.get('id_comment', ''))
    else:
        message = {'message': "GET petitions are not allowed for this view."}
    return HttpResponse(json.dumps(request))