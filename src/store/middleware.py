class StoreTemplateMiddleware:
    """ Simply print out the template directory of a store"""
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        print("---------------- fetching ---------------- \n \
STORE : %s \n TEMPLATES_DIR : %s \n \
            ----------------------------------------------" % (request, request.GET))
        response = self.get_response(request)
        return response
    

class CartFetchMiddleware:
    "Get the cart of the logged in user and adds it to context variables"
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # print('REQUEST: %s  | SELF: %s' % (request, self))
        # for i in request.META:
            # print(i, request.META[i], sep=' : ')
        response = self.get_response(request)
        print(response)
        return response