
__agent = None
def initialize_function_utils(agent):
    """
    This method is used to initialize the main agent 
    class in this file. This is done to allow the injection
    of the MainAgent(sc2.BotAI) to every decorated method (see agent_method)

    The injected object lives in the __agent variable in this file.
    """
    global __agent 
    __agent = agent


def agent_method(function):
    """
    Decorator function:
    Every method decorated with @agent_method will have
    the main agent class (which inherits sc2.BotAI class) injected.

    Example usage:
    @agent_method
    def test_method(*args, agent=None, **kwargs):
        ...

    """
    def wrapper(*args, **kwargs):
        global __agent
        rv = function(*args, __agent, **kwargs)
        return rv
    return wrapper    
    