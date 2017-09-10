class Item:
    def __init__(self, use_function=None, targeting=False, targeting_message=None,
                 is_treasure=False, **kwargs):
        self.use_function = use_function
        self.targeting = targeting
        self.targeting_message = targeting_message
        self.is_treasure = is_treasure
        self.function_kwargs = kwargs
