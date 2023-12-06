class Group:
    def __init__(self, user_list):
        self.user_list = user_list

    def add_user(self, usr):
        self.user_list.append(usr)
        return self.user_list

    def del_user(self, usr):
        self.user_list.pop(usr.index())
