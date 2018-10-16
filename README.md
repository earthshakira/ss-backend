## ss-backend API

This API primarily validates and applies a coupon to a cart

[link to live heroku](https://shubham-ss-api.herokuapp.com/api/)

### Routes

```python
/api/{type}
```
route to Fetch Collections of objects from DB

```python
/api/cart/{userId}
```
Cart routes

```python
/api/cart/{userId}/{task}
```
routes for operations on cart
```python
/api/coupon/{id}
```
route for a coupon

```python
/api/validate/{userId}/{couponId}
```
validates a coupon for a cart

```python
/api/apply/{userId}/{couponId}
```
gives the changes for a cart on a particular coupon
