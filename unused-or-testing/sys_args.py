
def sys_args(*check):
    """System Arg Handler Function.

    Check if arg(s) were given or return all.

    *check - Args to compare to those give to sys | Strings
            / If none are give, argv given to system are returned.
            / If args are give, it will check if they were given to sys.
                Returning a list of Trues/False or signle if single arg is given.

    """
    if not check:
        return sys.argv[1:]
    else:
        re = [i in sys.argv[1:] for i in check]
        if len(re) == 1: re = re[0]
        return re
