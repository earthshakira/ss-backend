from app import api
from backend.listing import ListingResource
from backend.cart import CartResource
from backend.coupon import CouponResource
from backend.cartUpdater import CartUpdater
from backend.validate import ValidateEndpoint
from backend.apply import ApplyEndpoint

api.add_route('/api/{type}', ListingResource())
api.add_route('/api/cart/{userId}',CartResource())
api.add_route('/api/cart/{userId}/{task}',CartUpdater())
api.add_route('/api/coupon/{id}',CouponResource())
api.add_route('/api/validate/{userId}/{couponId}',ValidateEndpoint())
api.add_route('/api/apply/{userId}/{couponId}',ApplyEndpoint())
