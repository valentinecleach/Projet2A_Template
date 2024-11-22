
class Singleton(type):
    """
    A singleton metaclass that ensures a class has only one instance.

    Attributes
    ----------
    _instance : dict
        A dictionary to store instances of classes that use this metaclass
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """Creates or returns an instance of the class.
        
        Parameters
        ----------
        cls : type
            The class being instantiated.
        *args
            Positional arguments.
        **kwargs
            Keyword arguments.
        
        Returns
        -------
        Singleton
        """ 
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]