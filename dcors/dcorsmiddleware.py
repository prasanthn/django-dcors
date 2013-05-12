from django import http
from django.conf import settings
from dcors.utils import logger

"""Django middleware module for handling CORS HTTP headers.

Values specified in the settings module are used to set appropriate headers
in HTTP responses. These headers are added to all responses.

Pre-flight requests, i.e., OPTIONS requests that have the
Access-Control-Request-Method header, are returned with an empty response
containing all the headers mentioned below.

Take this behaviour into account when adding this middleware to the
MIDDLEWARE_CLASSES list in the settings module.

Adding headers to all responses is useful since not all requests are
"pre-flighted". For example a "simple" credentialed GET request is not
"pre-flighted", but the response must have Access-Control-Allow-Credentials set
to "true" for the response to be available to the client script.

       Setting              Value                  Respone header

    CORS_ALLOW_ORIGIN       string            Access-Control-Allow-Origin
    CORS_ALLOW_METHODS      list              Access-Control-Allow-Methods
    CORS_ALLOW_HEADERS      list              Access-Control-Allow-Headers
    CORS_ALLOW_CREDENTIALS  "true" or "false" Access-Control-Allow-Credentials
    CORS_EXPOSE_HEADERS     list              Access-Control-Expose-Headers
    CORS_MAX_AGE            seconds           Access-Control-Max-Age

If the setting CORS_ALLOW_ALL_ORIGIN is present, containing any value, then the
Access-Control-Allow-Origin response header is set to the value of the Origin
header in the request. This is a shortcut for allowing CORS for all domains.

If the setting CORS_ALLOW_ALL_HEADERS is present, containing any value, then the
Access-Control-Allow-Headers response header is set it the value of the Access-
Control-Request-Headers header in the request. This is a shortcut for allowing
clients to send any header with a CORS request.

By default none of the above values are set, and hence the response will contain
empty values for the corresponding header. Note that the headers will be present
in the response, but the value of each will be an empty string.

This middleware only adds appropriate headers to responses, and doesn't prevent
access based on header values in the request. A web browser will not allow
JavaScript to issue requests and access responses that don't conform to the CORS
standard. The browser determines the allowed access points using the headers in
the response.

See https://developer.mozilla.org/en-US/docs/HTTP/Access_control_CORS for more
information on CORS. Web browsers that support CORS can be found at
http://caniuse.com/#search=cors .

"""


class CorsMiddleware(object):
    """Django middleware to enable CORS support.
    """
    def set_headers(self, response, request):
        CORS_ALLOW_ORIGIN = getattr(settings, "CORS_ALLOW_ORIGIN", '')
        CORS_ALLOW_METHODS = getattr(settings, "CORS_ALLOW_METHODS", [])
        CORS_ALLOW_HEADERS = getattr(settings, "CORS_ALLOW_HEADERS", [])
        CORS_ALLOW_CREDENTIALS = getattr(settings, "CORS_ALLOW_CREDENTIALS", "false")
        CORS_EXPOSE_HEADERS = getattr(settings, "CORS_EXPOSE_HEADERS", [])
        CORS_MAX_AGE = getattr(settings, "CORS_MAX_AGE", 0)

        # A shortcut to allow CORS for all domains.
        if getattr(settings, "CORS_ALLOW_ALL_ORIGIN", None):
            CORS_ALLOW_ORIGIN = request.META.get("HTTP_ORIGIN")
        # A shortcut to allow all headers in a CORS request.
        if getattr(settings, "CORS_ALLOW_ALL_HEADERS", None):
            CORS_ALLOW_HEADERS = request.META.get("HTTP_ACCESS_CONTROL_REQUEST_HEADERS")

        response['Access-Control-Allow-Origin'] = CORS_ALLOW_ORIGIN
        response['Access-Control-Allow-Methods'] = ",".join(CORS_ALLOW_METHODS)
        response['Access-Control-Allow-Headers'] = ",".join(CORS_ALLOW_HEADERS)
        response['Access-Control-Allow-Credentials'] = CORS_ALLOW_CREDENTIALS
        response['Access-Control-Expose-Headers'] = ",".join(CORS_EXPOSE_HEADERS)
        response['Access-Control-Max-Age'] = CORS_MAX_AGE

        return response

    def process_request(self, request):
        """If 'preflight' request then simple return all CORS settings."""
        if request.method == 'OPTIONS' and 'HTTP_ACCESS_CONTROL_REQUEST_METHOD' in request.META:
            response = http.HttpResponse()
            return self.set_headers(response, request)

        return None

    def process_response(self, request, response):
        """Add headers to response.

        If Access-Control-Allow-Origin is already present then no action is taken.
        """
        # Assume that these headers have been set somewhere else.
        # For example, in the response to a preflight request as above.
        if response.has_header('Access-Control-Allow-Origin'):
            return response

        # Not all requests will be preceded by a preflight request. So include
        # all headers. The credentials header is required when a credentialed
        # get request is made; get requests are usually not "preflighted".
        return self.set_headers(response, request)
