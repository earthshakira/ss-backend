from app import api
from listing import ListingResource
from cart import CartResource
from coupon import CouponResource
from cartUpdater import CartUpdater
from validate import ValidateEndpoint
from apply import ApplyEndpoint

api.add_route('/api/{type}', ListingResource())
api.add_route('/api/cart/{userId}',CartResource())
api.add_route('/api/cart/{userId}/{task}',CartUpdater())
api.add_route('/api/coupon/{id}',CouponResource())
api.add_route('/api/validate/{userId}/{couponId}',ValidateEndpoint())
api.add_route('/api/apply/{userId}/{couponId}',ApplyEndpoint())
