

def test(function):
    def f(*args):
        rv = function(args, kwargs)
        print("RV: {}".format(rv))
        postAction = kwargs["postAction"]
        if rv and postAction is not None:
            postAction()
        return rv
    return f   

@test
def build(unit):
    print("Wanna build {}".format(unit))
    return True


if __name__ == "__main__":
    build("sto cazzo", postAction=lambda: print("Executing post action"))
    print("End")
