STATUS_NOT_STARTED = 1
STATUS_IN_PROGRESS = 2
STATUS_DONE = 3

STATUS_CHOICES = (
    (STATUS_NOT_STARTED, 'Not Started'),
    (STATUS_IN_PROGRESS, 'In Progress'),
    (STATUS_DONE, 'Done'),
)

STATUS_CHOICES_DICT = dict((x, y) for x, y in STATUS_CHOICES)