class Item:
    def __init__(self, use_function=None, targeting=False, targeting_message=None,
                 treasure_value=None, **kwargs):
        self.use_function = use_function
        self.targeting = targeting
        self.targeting_message = targeting_message
        self.treasure_value = treasure_value
        self.function_kwargs = kwargs
