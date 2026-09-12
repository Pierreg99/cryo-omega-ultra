"""omega-hello — example gateway plugin.

Signals the register(api) contract:
  def register(api):
      api.add_route(method, path, handler)

handler(request_handler, method, path, query, body) writes the response via
request_handler._json(...).
"""


def hello(h, method, path, query, body):
    h._json({
        "plugin": "omega-hello",
        "message": "hello from the omega gateway plugin system",
        "engine": "python-gateway",
    })


def register(api):
    api.add_route("GET", "/api/hello", hello)