
class Task():
    def __init__(self, name, description, clue, value, install_function, verify_function, parents=[]):
        self.name             = name
        self.description      = description
        self.clue             = clue
        self.value            = value
        self.install_function = install_function
        self.verify_function  = verify_function
        self.parents          = parents

        self.done             = False
        self.clue_used        = False
        self.lock             = len(parents) != 0
        self.level            = max( [t.level+1 for t in parents] + [0] )

    def verify(self):
        for parent in self.parents:
            verified, reason = parent.verify()
            if not verified:
                return False, f"{parent.name} not verified: {reason}"

        self.lock = False
        self.done, reason = self.verify_function()
        return self.done, reason

    def is_lock(self):
        self.lock = not all([t.done for t in self.parents])
        return self.lock

    def install(self):
        if self.install_function:
            return self.install_function()
        else:
            return True

    def show(self):
        return self.name, self.description

    def show_clue(self):
        if not self.clue_used:
            self.clue_used = True
            self.value = self.value // 2
        return self.clue


    def __str__(self):
        parents = ['\n'.join([' '*3 + line for line in p.__str__().split('\n')]) for p in self.parents]
        for i in range(len(parents)):
            tmp = [l for l in parents[i]]
            tmp[1] = '*'
            parents[i] = "".join(tmp)

        if parents == []:
            parents = [' Nothing']
        return f"task: '{self.name}'\ndone: {self.done}\nclue used: {self.clue_used}\ndepends on:\n"+"\n".join(parents)
