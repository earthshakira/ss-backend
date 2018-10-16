import falcon

from models import Cart
from util import ResponseUtil

class CartResource(object):

    def on_get(self, req, resp,userId):
        try:
            carts = Cart.objects(userId = userId)
            if len(carts) == 0 :
                ResponseUtil.makeResponse(404,resp);
                return;
            else :
                ResponseUtil.makeBody(resp,carts[0].to_json())
        except Exception as e:
            ResponseUtil.error(e,resp)


    def on_post(self, req, resp,userId):
        try:
            cart = Cart(userId = userId)
            carts = Cart.objects(userId = userId)
            if len(carts) == 0 :
                cartResp = cart.save()
                ResponseUtil.makeBody(resp, cartResp.to_json())
            else :
                ResponseUtil.makeBody(resp,carts[0].to_json())
        except Exception as e:
            ResponseUtil.error(e,resp);

    def on_options(self,req,resp,userId):
        ResponseUtil.makeBody(resp,"");
