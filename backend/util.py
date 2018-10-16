import falcon
class ResponseUtil(object):
    """To be used for getting a predefined response for errors"""
    stati = {
        404:{
            "status": falcon.HTTP_404,
            "message": 'resource not found'
        },
        409:{
            "status": falcon.HTTP_409,
            "message": 'idempotent operation'
        },
        400:{
            "status": falcon.HTTP_400,
            "message": 'operation not supported'
        },
        422:{
            "status": falcon.HTTP_422,
            "message": 'Can\'t do what you want with what I\'ve got valid params'
        },
        202:{
            "status": falcon.HTTP_202,
            "message": 'Already done'
        }

    }

    @staticmethod
    def addHeaders(response):
        response.append_header('Access-Control-Allow-Headers','X-PINGOTHER, Content-Type')
        response.append_header('Access-Control-Allow-Origin','*')
        response.append_header('Allow','OPTIONS, GET, HEAD, POST, PATCH')
        response.append_header('Access-Control-Allow-Methods','OPTIONS, GET, HEAD, POST, PATCH')
        response.append_header('Content-type','application/json; charset=utf-8')

    @staticmethod
    def makeBody(response,value):
        ResponseUtil.addHeaders(response);
        response.status = falcon.HTTP_200
        response.body = value

    @staticmethod
    def makeJson(response,jsonObject):
        ResponseUtil.addHeaders(response);
        response.status = falcon.HTTP_200
        response.json = jsonObject

    @staticmethod
    def makeResponse(statusCode,response):
        ResponseUtil.addHeaders(response);
        error = ResponseUtil.stati[statusCode]
        response.status = error['status']
        response.json = error;

    @staticmethod
    def success():
        ResponseUtil.addHeaders(response);
        return falcon.HTTP_200

    @staticmethod
    def error(e,response):
        ResponseUtil.addHeaders(response);
        response.status = falcon.HTTP_500
        response.json = {'status' : falcon.HTTP_500, 'except' : str(e)}
