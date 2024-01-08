class MyFunc():
    def __init__(self, db, args_list):
        self.args_list = args_list#[:]
        self.db = db
        print(self.args_list)

    def __call__(self, *args, **kwargs):
        if len(args) > len(self.args_list):
            raise TypeError(f'Too many arguments passed: {args} for expected {self.args_list}.')

        # At this point all positional arguments are fine.
        for arg in self.args_list[len(args):]:
            if arg not in kwargs:
                raise TypeError(f'Missing value for argument {arg}.')

        # At this point, all arguments have been passed either as
        # positional or keyword.
        if len(self.args_list) - len(args) != len(kwargs):
            raise TypeError('Too many arguments passed.')

        if self.db is not None:
            self.db.main[self.db.pkey_max] = {}

        for e, arg in enumerate(args):
            #print(e, arg)
            self.db.main[self.db.pkey_max][self.db.args[e]] = arg

        for arg in self.args_list[len(args):]:
            #print(arg, kwargs[arg])
            self.db.main[self.db.pkey_max][arg] = kwargs[arg]

        #print(self.args_list[len(args):])
        #for kw in self.args_list[len(args):]:
            #self.db.main[self.db.pkey_max][kw] = arg
        self.db.pkey_max += 1
        return self.db.pkey_max-1

class Database:
    def __init__(self, *args):
        #self.main = {primary_key: {x: None for x in args}}
        self.main = {}
        self.args = args
        self.pkey_max = 0
        self.add_entry = MyFunc(self, self.args)

    # check if the pkey is in the database
    def get_pkey(self, pkey, default=None):
        # return true or whatever the default is
        return self.main.get(pkey)

    # check if the key has the value, for the pkey
    def find_by_key(self, pkey, key, value, default=None):
        # return true or whatever the default is
        return ((got_val := self.main[pkey].get(key) is not None) and got_val == value) or default

    # finds a value in any column, by the pkey, and returns it
    def find_by_p_key(self, pkey, value, default=None):
        if (exists := self.main.get(pkey)) is not None:
            for k,v in exists.items():
                if value in v:
                    return v
            else:
                return default
        else:
            return default

db = Database("one", "two", "three", "four")
print(db.add_entry(1, 4, three=3, four=16))
print(db.add_entry("a", "b", "c", "d"))
print(db.add_entry(one=-1, two=-2, three=-3, four=-4))
for x in range(5):
    if db.get_pkey(x):
        print(db.main[x])
