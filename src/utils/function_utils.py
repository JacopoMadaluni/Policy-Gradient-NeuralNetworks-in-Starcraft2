
__agent = None
def initialize_function_utils(agent):
    global __agent 
    __agent = agent

"""
Decorator function
"""
def agent_method(function):
    def wrapper(*args, **kwargs):
        global __agent
        rv = function(*args, __agent, **kwargs)
        return rv
    return wrapper    
    