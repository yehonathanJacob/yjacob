from io import BytesIO
from flask import after_this_request, request
import gzip
import functools


def gzipped(compression_level=9, enabled=True):
    def decorator(f):
        @functools.wraps(f)
        def view_func(*args, **kwargs):
            @after_this_request
            def zipper(response):
                if not enabled:
                    return response

                accept_encoding = request.headers.get('Accept-Encoding', '')

                if 'gzip' not in accept_encoding.lower():
                    return response

                response.direct_passthrough = False

                if response.status_code < 200 or response.status_code >= 300 or 'Content-Encoding' in response.headers:
                    return response

                gzip_buffer = BytesIO()
                gzip_file = gzip.GzipFile(mode='wb', fileobj=gzip_buffer, compresslevel=compression_level)
                gzip_file.write(response.data)
                gzip_file.close()

                response.data = gzip_buffer.getvalue()
                response.headers['Content-Encoding'] = 'gzip'
                response.headers['Vary'] = 'Accept-Encoding'
                response.headers['Content-Length'] = len(response.data)

                return response

            return f(*args, **kwargs)

        return view_func

    return decorator
