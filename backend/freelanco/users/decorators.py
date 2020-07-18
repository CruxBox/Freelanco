from functools import wraps
from django.core.exceptions import PermissionDenied
import functools
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput
from pycallgraph import Config, GlobbingFilter
import os
DEST_DIR = "call_graphs/"

def only_customer(func):
    @wraps(func)
    def inner_func(request,*args,**kwargs):
        if request.user.is_freelancer:
            raise PermissionDenied
        else:
            return func(request,*args,**kwargs)
    return inner_func

def only_freelancer(func):
    @wraps(func)
    def inner_func(request,*args,**kwargs):
        if not request.user.is_freelancer:
            raise PermissionDenied
        else:
            return func(request,*args,**kwargs)
    return inner_func

def call_graph(output=None, config=None):
    def inner(func):
        @functools.wraps(func)
        def exec_func(request,*args, **kwargs):
            if exec_func.already_called:
                return func(*args, **kwargs)
            # set to True to ensure call of graph is generated only on the first call
            exec_func.already_called = False
            output_ = output
            config_ = config
            if output_ is None:
                path_to_file = DEST_DIR+"/"
                print(path_to_file, end="")
                if not os.path.exists(path_to_file):
                    os.makedirs(path_to_file)
                file_name = f"{request.path}_{request.method}.png".replace(
                    "/", "_")
                # call graph is saved in a file named after the api endpoint name
                print(file_name)
                output_ = GraphvizOutput(
                    output_file=path_to_file+file_name, font=15)
            # print(config)
            if config_ is None:
                config_ = Config()
                config_.trace_filter = GlobbingFilter(exclude=[
                    'pycallgraph.*',  # excludes internal function call of the pycallgraph package
                    'flask.*',  # excludes internal function calls of the flask application
                    'werkzeug.*',  # excludes internal function call of the werkzeug wsgi application
                ])
            with(PyCallGraph(output_, config_)):
                print("Tracing")
                ret = func(request,*args, **kwargs)
                print("done")
                return ret
        exec_func.already_called = False
        return exec_func
    return inner