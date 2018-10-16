import falcon

from models import Product
from models import Coupon
from models import Cart
from util import ResponseUtil

class ListingResource(object):
    def on_get(self, req, resp,type):
        if type == 'products' :
            ResponseUtil.makeBody(resp,Product.objects.to_json())
        elif type == 'coupons' :
            ResponseUtil.makeBody(resp,Coupon.objects.to_json())
        elif type == 'carts' :
            ResponseUtil.makeBody(resp,Cart.objects.to_json())
