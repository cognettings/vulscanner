from enum import (
    Enum,
)


class SingerStreams(Enum):
    issue_assignees = "issue_assignees"
    issue_labels = "issue_labels"
    issue = "issue"
    jobs = "jobs"
    job_tags = "job_tags"
    members = "members"
    merge_requests = "merge_requests"
