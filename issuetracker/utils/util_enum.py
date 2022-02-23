import enum


class BaseEnum:
    @classmethod
    def choices(cls):
        return [(i.value, i.description) for i in cls]

    @classmethod
    def to_enum(cls, val):
        for i in cls:
            if i.value == val:
                return i

    @classmethod
    def help(cls):
        items = [f"* ({i.value}, {i.description})" for i in cls]
        if len(items) > 30:
            items = items[:30]
            items[29] = "..."
        return "\n".join(items)


class StringEnum(str, BaseEnum, enum.Enum):
    def __new__(cls, value, *args):
        if not isinstance(value, (str, enum.auto)):
            raise TypeError(f"Value must be string: {repr(value)} is a {type(value)}")
        entry = str.__new__(cls, value)
        entry._value_ = value
        return entry

    def __init__(self, value, description=""):
        super().__init__()
        self.description = description

    def __str__(self):
        return self.value
