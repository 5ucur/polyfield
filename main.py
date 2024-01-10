import os
import pickle

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
            raise TypeError(f'Too many arguments passed.')

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
        self.db.serialise()
        return self.db.pkey_max-1

class Database:
    def __init__(self, filename, *args):
        #self.main = {primary_key: {x: None for x in args}}
        # If the file exists
        self.filename=f"{filename}.db"
        if os.path.isfile(self.filename):
            # Try to load the file
            try:
                with open(self.filename, "rb") as file:
                    self.main = pickle.load(file)
            except Exception as e:
                print(f"An error occurred, this is all we know: {e}")
        # If the file doesn't exist, and also no pos args
        elif not args:
            raise TypeError(f"Neither filename nor positional arguments supplied.\n{filename}\n{args}")
        # So by now there should be args, and a filename for a missing file
        else:
            # Set up main dict
            self.main = {}
        # If we have an existing database
        if self.main:
            print("we have main")
            #self.pkey_max = self.main[0]
            self.pkey_max = len(self.main)+1
            self.args = list(self.main[0].keys())
        # Else, if the database is empty
        else:
            print("we have no main")
            # Set pkey_max to zero
            self.pkey_max = 0
            self.args = args
        self.add_entry = MyFunc(self, self.args)
        # If the pkey_max is zero
        if not self.pkey_max:
            # Set pkey stuff to be stored
            self.add_entry(*["0" for _ in range(len(self.args))])

    def items(self):
        return self.main.items()

    def serialise(self):
        for key in self.args:
            self.main[0][key] = f"{self.pkey_max}"
        with open(self.filename, "wb") as file:
            pickle.dump(self.main, file)

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

db = Database("quotes", "one", "two", "three", "four")
db.add_entry(1, 4, three=3, four=16)
db.add_entry("a", "b", "c", "d")
db.add_entry(one=-1, two=-2, three=-3, four=-4)
for k, v in db.items():
    print(k, v)
# print(repr(db.main))
#db.serialise()
print("done c:")
