import falcon

from models import Cart
from util import ResponseUtil

class CartUpdater(object):

    def on_post(self,req,resp,userId,task):
        try:
            cartEntry = req.json
            cart = Cart.objects(userId = userId)
            key = 'items.' + str(cartEntry['productId']);
            if len(cart) == 0:
                ResponseUtil.makeResponse(400,resp)
                return
            cartUpdate = None
            if task == 'add' :
                cartUpdate = cart.update_one(__raw__={'$set':{key:cartEntry}})
            elif task == 'remove' :
                cartUpdate = cart.update_one(__raw__={'$unset':{key:1}})
            else :
                ResponseUtil.makeResponse(400,resp);
                return
            ResponseUtil.makeJson(resp,{"update":cartUpdate})
        except Exception as e:
            ResponseUtil.error(e,resp)

    def on_options(self,req,resp,userId,task):
        ResponseUtil.makeBody(resp,"");
