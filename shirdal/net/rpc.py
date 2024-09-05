from typing import Type

import zmq


def get_methods(obj):
    """
    Retrieve all methods of an object excluding built-in special methods.

    Args:
    obj: The object whose methods are to be listed.

    Returns:
    list: A list of method names as strings.
    """
    # Get all attributes of the object
    attributes = dir(obj)

    # Filter out callable attributes (methods) and special methods
    return [
        attr for attr in attributes
        if callable(getattr(obj, attr)) and not attr.startswith('__')
    ]


class ServerRPC:
    def __init__(self, endpoint):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind(endpoint)

    def start(self):
        while True:
            message = self.socket.recv_json()
            # Process the request (this is where you'd put your actual RPC logic)
            response = self._process_request(message)

            # Send the message back to the client
            self.socket.send_json(response)

    def _process_request(self, request):
        # Placeholder for actual RPC logic
        if 'method' in request and 'params' in request:
            method = request['method']
            params = request['params']

            args = params.get('args', [])
            kwargs = params.get('kwargs', {})

            func = getattr(self, method)

            return func(*args, **kwargs)

        return {'error': 'Unknown method'}


class ClientRPC:
    def __init__(self, endpoint):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect(endpoint)

    def _call(self, method, *args, **kwargs):
        # Prepare the request
        request = {
            'method': method,
            'params': {
                'args': list(args),
                'kwargs': kwargs
            }
        }

        # Send request
        self.socket.send_json(request)

        # Wait for response
        response = self.socket.recv_json()
        return response
