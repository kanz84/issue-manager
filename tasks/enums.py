from issuetracker.utils.util_enum import StringEnum


class TaskStatusEnum(StringEnum):
    NOT_STARTED = "NS", "Not Started"
    IN_PROGRESS = "IP", "In Progress"
    DONE = "D", "Done"

    @classmethod
    def to_dict(cls):
        return {i.value: i.description for i in cls}
