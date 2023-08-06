class Result:
    def __init__(self, success, value, error):
        self.success = success
        self.error = error
        self.value = value

    @property
    def failure(self):
        return not self.success

    @classmethod
    def fail(cls, error):
        return cls(False, value=None, error=error)

    @classmethod
    def ok(cls, value=None):
        return cls(True, value=value, error=None)
