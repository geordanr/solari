# Copyright (c) 2010 Eli Stevens
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# stdlib
import functools
import os, os.path
import re
import threading
import urllib

# 3rd party packages

# in-house
import core

def browserFingerprint(app):
    def middleware_browserFingerprint(environ, start_response):
        ua_str = 'foo'
        ua_list = re.sub('[();/]+', ' ', ua_str.lower()).split()

        browser_str = None
        if 'compatible' in ua_list:
            for browser_str in ('opera', 'msie', 'konqueror'):
                if browser_str in ua_list:
                    break
            else:
                browser_str = None

        elif 'mozilla' in ua_list:
            for browser_str in ('chrome', 'firefox', 'netscape6', 'netscape', 'galeon', 'k-meleon', 'gecko'):
                if browser_str in ua_list:
                    break
            else:
                browser_str = 'mozilla'

        else:
            for browser_str in ('lynx', 'wget', 'elinks'):
                if browser_str in ua_list:
                    break
            else:
                browser_str = None

        if browser_str:
            core.context.browser = (browser_str, ua_list[ua_list.index(browser_str) + 1], ua_str)
        else:
            core.context.browser = (None, None, ua_str)

        return app(environ, start_response)

    return middleware_browserFingerprint


try:
    import couchable


    def trace(*args):
        def _trace(func):
            def wrapper(*args, **kwargs):
                print enter_string
                func(*args, **kwargs)
                print exit_string
            return wrapper

        if len(args) == 1 and callable(args[0]):
            # No arguments, this is the decorator
            # Set default values for the arguments
            enter_string = 'entering'
            exit_string = 'exiting'
            return _trace(args[0])
        else:
            # This is just returning the decorator
            enter_string, exit_string = args
            return _trace



    def addCouchableDb(cdbname='?', cdburl='http://localhost:5984'):
        def addCouchableDb_(func):
            @functools.wraps(func)
            def addCouchableDb__(*args, **kwargs):
                core.context.cdb = couchable.CouchableDb(kwargs.get('cdburl', cdbname), kwargs.get('cdbname', cdburl))
                return func(*args, **kwargs)

            return addCouchableDb__
        return addCouchableDb_

        #if len(args) == 1 and callable(args[0]):
        #    # No arguments, this is the decorator
        #    # Set default values for the arguments
        #    enter_string = 'entering'
        #    exit_string = 'exiting'
        #    return _trace(args[0])
        #else:
        #    # This is just returning the decorator
        #    enter_string, exit_string = args
        #
        #    return functools.partial(middleware_addCouchableDb, **kwargs)
        #
        #return middleware_addCouchableDb

except ImportError:
    pass




# eof
