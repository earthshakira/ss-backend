import falcon

from models import Coupon
from models import Cart
from models import Product
from util import ResponseUtil

class ApplyEndpoint(object):

    def on_get(self, req, resp,userId,couponId):
        try:
            couponResult = Coupon.objects(id = couponId)
            cartResult = Cart.objects(userId = userId)
            if len(couponResult) == 0 :
                ResponseUtil.makeJson(resp,{'status': False,'reason':'Coupon not found'});
                return;
            if len(cartResult) == 0 :
                ResponseUtil.makeJson(resp,{'status': False,'reason':'Cart does not exist for userId'});
                return;

            coupon = couponResult[0]
            cart = cartResult[0]
            cartItems = {};
            pids = [];
            for item in cart.items.keys():
                if cart.items[item]['quantity']>0:
                    cartItems[int(item)] = cart.items[item];
                    pids.append(item);

            if len(pids) == 0 :
                ResponseUtil.makeJson(resp,{'status': False,'reason':'Cart is Empty'})
                return;

            products = Product.objects(productId__in=pids)
            filteredList = products;
            if coupon.artist:
                filteredList = list( filter((lambda x: x.artist == coupon.artist), filteredList))

            if coupon.product:
                filteredList = list( filter((lambda x: x.product == coupon.product), filteredList))

            if coupon.category:
                filteredList = list( filter((lambda x: x.category == coupon.category), filteredList))

            if len(filteredList) == 0:
                ResponseUtil.makeJson(resp,{'status': False,'reason':'Supplied Products do not have required category,artist or product'})
                return;

            totalQuantity = 0;
            totalCost = 0.00;

            for product in filteredList:
                totalCost += cartItems[product.productId]['quantity']*float(product.price);
                totalQuantity += cartItems[product.productId]['quantity'];
            print(coupon.to_json())
            if (coupon.constraint['type'] == 'cartTotal'):
                if(totalCost <= float(coupon.constraint['value'])):
                    ResponseUtil.makeJson(resp,{'status': False,'reason':'cartValue less than required','totalCost':totalCost,'totalQuantity':totalQuantity})
                    return
            elif (coupon.constraint['type'] == 'buy'):
                if(totalQuantity < int(coupon.constraint['value'])):
                    ResponseUtil.makeJson(resp,{'status': False,'reason':'number of items less than required','totalCost':totalCost,'totalQuantity':totalQuantity})
                    return
                elif coupon.discount['type'] == 'get' :
                    offItems = totalQuantity - int(coupon.constraint['value']);
                    maxDiscounted = int(coupon.discount['value']);
                    if maxDiscounted > offItems :
                        coupon.discount['value'] =  offItems
                    else :
                        coupon.discount['value'] = maxDiscounted

            newPrice = {}
            coupon.discount['value'] = int(coupon.discount['value']);
            if coupon.discount['type'] == 'get':
                sortedProducts = sorted(filteredList, key=(lambda x: float(x.price)))
                for item in sortedProducts:
                    if(coupon.discount['value'] == 0):
                        break
                    itemQuantity = int(cartItems[item.productId]['quantity']);
                    if(coupon.discount['value'] >= itemQuantity):
                        coupon.discount['value'] -= itemQuantity
                        print('decreasingQuantity');
                        newPrice[str(int(item.productId))] = 0
                    else :
                        newPrice[str(int(item.productId))] = (itemQuantity - coupon.discount['value'])*int(float(item.price))
                        coupon.discount['value'] = 0;
            elif coupon.discount['type'] == 'getPercentage':
                percent = 1 - (float(coupon.discount['value'])/100);
                for item in filteredList:
                    if(coupon.discount['value'] == 0):
                        break
                    itemQuantity = int(cartItems[item.productId]['quantity'])
                    itemPrice = float(item.price)
                    itemTotal = itemPrice * itemQuantity
                    itemTotal*= percent
                    newPrice[str(int(item.productId))] = int(itemTotal)


            ResponseUtil.makeJson(resp,{'status': True, 'newPrice':newPrice});
        except Exception as e:
            print(e)
            ResponseUtil.error(e,resp)
