# OpenID consumer demo.
# Refer to: https://github.com/openid/python-openid

import openid
import webapp2
from openid.consumer import consumer
from openid.extensions import sreg

# my OpenID: https://myprovider.com/openid/myname
OPENID_PROVIDER_URL = 'https://myprovider.com/openid/'

class RootHandler(webapp2.RequestHandler):
    def get(self):
        print self.request.path
        if self.request.path == '/':
            self.response.content_type = 'text/plain'
            self.response.body = 'Please visit /login\n'
        elif self.request.path == '/login':
            self.doLogin()
        elif self.request.path == '/verify':
            self.doVerify()
        else:
            self.response.status_int = 404

    def doLogin(self):
        oidconsumer = consumer.Consumer(dict(), None)

        try:
            request = oidconsumer.begin(OPENID_PROVIDER_URL)
            if request is None:
                msg = 'No OpenID services found for ' + OPENID_PROVIDER_URL
                raise consumer.DiscoveryFailure(msg, None)
        except consumer.DiscoveryFailure, exc:
            self.response.status_int = 500
            self.response.content_type = 'text/plain'
            self.response.body = 'Error in discovery: %s' % exc[0]
            return

        sreg_request = sreg.SRegRequest(['nickname', 'fullname', 'email'])
        request.addExtension(sreg_request)

        realm = 'http://localhost:9000/'
        return_to = realm + 'verify'
        redirect_url = request.redirectURL(realm, return_to)

        self.response.status_int = 302
        self.response.location = redirect_url

    def doVerify(self):
        oidconsumer = consumer.Consumer(dict(), None)

        query = self.request.params
        current_url = self.request.path_url
        info = oidconsumer.complete(query, current_url)
        identifier = info.getDisplayIdentifier() or ''

        if info.status == consumer.SUCCESS and \
           identifier.startswith(OPENID_PROVIDER_URL):
            sreg_resp = dict(sreg.SRegResponse.fromSuccessResponse(info))
            self.response.body = 'Identity: %s\nRegistration: %s\n' % \
                (identifier,sreg_resp)
        else:
            self.response.status_int = 403
            self.response.content_type = 'text/plain'
            self.response.body = 'OpenID verification failed.'
            return


application = webapp2.WSGIApplication([('/.*', RootHandler)])

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    host, port = 'localhost', 9000
    server = make_server(host, port, application)
    print 'Serving on port %s:%s...' % (host, port)
    server.serve_forever()
