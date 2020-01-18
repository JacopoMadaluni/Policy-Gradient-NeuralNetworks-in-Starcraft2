

def test(function):
    def f(*args, **kwargs):
        rv = function(*args, **kwargs)
        print("RV: {}".format(rv))
        postAction = kwargs["postAction"]
        if rv and postAction is not None:
            postAction()
        return rv
    return f   

agent = "hello"
def agent_method(function):
    def wrapper(*args, **kwargs):
        rv = function(*args, agent, **kwargs)
        return rv
    return wrapper    
    


@agent_method
def test2(x, agent=None):
    print(x)
    print(agent)



def pls(*args):
    print(args)

    


if __name__ == "__main__":
    test2("hello1")
