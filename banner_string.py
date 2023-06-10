class BannerString:
    def __init__(self, string_list):
        self.string = string_list

    def __repr__(self):
        return "\n".join(self.string)

    def __str__(self):
        return self.__repr__()
