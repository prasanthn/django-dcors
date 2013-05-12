Django CORS
===========

The package ``dcors`` is a Django middleware for enabling Cross-Origin Resource
Sharing (CORS).

Install  the module using::

  pip install django-dcors

Code is available at https://github.com/prasanthn/django-dcors .

Values specified in the Django settings module are used to set appropriate
headers in HTTP responses. These headers are added to all responses.

Pre-flight requests, i.e., OPTIONS requests that have the
Access-Control-Request-Method header, are returned with an empty response
containing all the headers mentioned below.

Take this behaviour into account when adding this middleware to the
MIDDLEWARE_CLASSES list in the settings module.

Adding headers to all responses is useful since not all requests are
"pre-flighted". For example a "simple" credentialed GET request is not
"pre-flighted", but the response must have Access-Control-Allow-Credentials set
to "true" for the response to be available to the client script.

::

       Setting              Value                  Respone header

    CORS_ALLOW_ORIGIN       string            Access-Control-Allow-Origin
    CORS_ALLOW_METHODS      list              Access-Control-Allow-Methods
    CORS_ALLOW_HEADERS      list              Access-Control-Allow-Headers
    CORS_ALLOW_CREDENTIALS  "true" or "false" Access-Control-Allow-Credentials
    CORS_EXPOSE_HEADERS     list              Access-Control-Expose-Headers
    CORS_MAX_AGE            seconds           Access-Control-Max-Age
    CORS_ALLOW_ALL_ORIGIN   <any-value>       <see explanation below>
    CORS_ALLOW_ALL_HEADERS  <any-value>       <see explanation below>

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

Tests are present in dcors/tests.py, and have been tested with Django 1.4.5 and
1.5.1 in Python 2.7.3 .
