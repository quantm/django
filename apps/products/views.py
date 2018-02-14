
import os, urllib, time, hashlib, cStringIO, PIL.Image as Image, string
from datetime import datetime
from settings import MEDIA_ROOT, OSCAR_IMAGE_FOLDER
from django.shortcuts import render_to_response, HttpResponse
from django.views.generic import ListView
from django.utils.translation import ugettext_lazy as _
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from oscar.core.utils import slugify
from oscar.apps.catalogue.models import ProductClass
from oscar.apps.customer.mixins import PageTitleMixin

import settings
from .forms import ProductForm
from apps.collection.models import *
from apps.catalogue.models import ProductImage
from oscar.apps.catalogue.views import ProductListView as CoreProductListView

def save_product(request):
    product_form = ProductForm(request.POST or None)
    if product_form.is_valid():
        #Get information for Product
        title = request.POST['title']
        slug = slugify(title)
        description = request.POST['description']
        image_url_from_web = urllib.unquote(request.POST['image']).decode('utf8')
        is_trending = int(request.POST['product_is_trending'])
        #Product class
        products = ProductClass.objects.all()
        if len(products) > 0:
            product_class = products[0]
        else:
            pro_cls_name = u'Default'
            pro_cls_slug = slugify(pro_cls_name)
            product_class = ProductClass(name=pro_cls_name, slug=pro_cls_slug)
            product_class.save()

        #Get image info
        io_file = cStringIO.StringIO(urllib.urlopen(image_url_from_web).read())
        img_file = Image.open(io_file)
        image_extension = '.' + string.lower(img_file.format)

        image_name = hashlib.md5(b'%s' % time.time()).hexdigest() + image_extension
        #built image path to save host
        url_product_image = datetime.now().strftime(OSCAR_IMAGE_FOLDER) + image_name
        #check file exists on host dir, need recheck MEDIA_ROOT was configured in settings file
        path_product_image = MEDIA_ROOT + '/' + url_product_image
        exists = os.path.exists(path_product_image)
        if(exists):
            url_product_image = datetime.now().strftime(OSCAR_IMAGE_FOLDER) + hashlib.md5(b'%s' % time.time()).hexdigest() + image_extension

        #save file
        img_saved = download_photo(image_url_from_web, url_product_image)

        #Save product object
        product = Product(title=title, slug=slug, description=description, product_class=product_class, user_id=request.user.pk, is_trending=is_trending)
        product.save()

        #Check image saved to save Product Image object
        if img_saved:
            product_image = ProductImage(product=product, original=url_product_image, caption=title, display_order=0)
            product_image.save()

        #built product link to return front end
        pro_link = '/catalogue/%s_%d/' % (slug, product.id)

        return {
            'code': 1,
            'pro_link': u'<a href="%s" class="f-button close" target="_blank">%s</a>' % (pro_link, u'See the product'),
            'back_text': u'Add more Products',
            'mes_box': u'<h1>Image has been saved!</h1>',
        }


def download_photo(image_url_from_web, url_product_image):
    #need recheck MEDIA_ROOT was configured in settings file
    try:
        image_on_web = urllib.urlopen(image_url_from_web)
        if image_on_web.headers.maintype == 'image':
            buf = image_on_web.read()
            file_path = "%s/%s" % (MEDIA_ROOT, url_product_image)
            arr_path = os.path.split(file_path)
            if not os.path.exists(arr_path[0]):
                os.makedirs(arr_path[0])
            downloaded_image = file(file_path, "wb")
            downloaded_image.write(buf)
            downloaded_image.close()
            image_on_web.close()
        else:
            return False
    except:
        return False
    return True


def ajax_product(request):
    page = request.GET.get('page')
    my_product = request.GET.get('my_product')

    if request.is_ajax():
        #product_list = Product.objects.all()
        product_list = Product.browsable.base_queryset().filter(stockrecords__isnull=False).distinct()

        if my_product:
            product_list = Product.objects.filter(user=request.user)

        paginator = Paginator(product_list, settings.PRODUCT_ITEM_PER_PAGE)

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        return render_to_response('catalogue/products/ajax_response.html', {"products": products, "user": request.user})

    return HttpResponse('')

class MyProductView(PageTitleMixin, ListView):
    context_object_name = active_tab = "my-products"
    template_name = 'catalogue/products/my_products.html'
    page_title = _('My Products')
    model = Product

    def get_context_data(self, **kwargs):
        context = super(MyProductView, self).get_context_data(**kwargs)
        product_list = Product.objects.filter(user=self.request.user)
        paginator = Paginator(product_list, settings.PRODUCT_ITEM_PER_PAGE)
        page = self.request.GET.get('page')

        try:
            context['products'] = paginator.page(page)
        except PageNotAnInteger:
            context['products'] = paginator.page(1)
        except EmptyPage:
            context['products'] = paginator.page(paginator.num_pages)

        return context

    def get_queryset(self):
        return super(MyProductView, self).get_queryset()



class ProductListAjaxView(CoreProductListView):

    template_name = 'catalogue/products/ajax_response.html'
    paginate_by = settings.PRODUCT_ITEM_PER_PAGE

    def get_context_data(self, **kwargs):
        context = super(ProductListAjaxView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        q = self.get_search_query()
        qs = Product.browsable.base_queryset()
        if q:
            # Send signal to record the view of this product
            self.search_signal.send(sender=self, query=q, user=self.request.user)
            return qs.filter(title__icontains=q)
        else:
            return qs.filter(stockrecords__isnull=False).distinct()

class MyProductListAjaxView(CoreProductListView):

    template_name = 'catalogue/products/ajax_response.html'
    paginate_by = settings.PRODUCT_ITEM_PER_PAGE

    def get_context_data(self, **kwargs):
        context = super(MyProductListAjaxView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        q = self.get_search_query()
        qs = Product.browsable.base_queryset().filter(user=self.request.user)
        if q:
            # Send signal to record the view of this product
            self.search_signal.send(sender=self, query=q, user=self.request.user)
            return qs.filter(title__icontains=q)
        else:
            return qs.distinct()