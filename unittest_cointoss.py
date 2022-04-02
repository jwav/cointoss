#!/usr/bin/env python3

import unittest
import cointoss as ct

class TestCointoss(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = ct.Game()

    @property
    def gameparams(self):
        return self.game.params

    def test_handle_arguments(self):
        # get all available arguments, t
        args = self.gameparams.all_arg_tuples()
        argnames = [x[0] for x in args]
        values = [x[1] for x in args]
        types = [type(x[1]) for x in args]
        print("argname:",argnames)
        print("values:",values)
        print("types:",types)
        print("args:",args)

        # defines which default value is used for a given value type
        def default_value_for_type(typ) -> str:
            if typ is bool: return ""
            else: return "1337"

        # for each argument, set values
        strargvalues = [default_value_for_type(typ) for typ in types]
        print("strargvalues:",strargvalues)

        argline = " ".join([f"{argname} {strargvalue}" for argname,strargvalue in zip(argnames,strargvalues)])
        argv = ["argv0"] + [x for x in argline.split(" ") if x]
        print("argline:",argline)
        print("argv",argv)

        self.gameparams.handle_arguments(argv)
        print(self.gameparams)





if __name__ == '__main__':
    unittest.main()
