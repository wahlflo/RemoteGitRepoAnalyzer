from collections import namedtuple
from datetime import datetime
from typing import List
from cli_formatter.output_formatting import error, info, Color, colorize_string


class MalformedCommitLog(Exception):
    pass


CommitLog = namedtuple("CommitLog", ['parent_commit_id', 'commit_id', 'user_name', 'user_email', 'timestamp', 'timezone', 'comment'])


def show_commit_logs(commit_logs: str) -> None:
    try:
        parsed_commit_logs = _parse_commit_logs(commit_logs=commit_logs)
    except MalformedCommitLog:
        error("error while parsing log file")
        info("show original downloaded log file")
        print(60 * '#')
        print(commit_logs)
        return

    if len(parsed_commit_logs) == 0:
        info("There are no commits")
        return

    for commit_log in parsed_commit_logs:
        print(commit_log.parent_commit_id, end=' ')
        print(commit_log.commit_id, end=' ')
        print(commit_log.user_name, end=' ')
        print(commit_log.user_email, end=' ')
        print(colorize_string(commit_log.timestamp.strftime('%d.%m.%Y %H:%M'), color=Color.YELLOW), end=' ')
        print(commit_log.timezone, end=' ')
        print(colorize_string(text=commit_log.comment, color=Color.GREEN))


def _parse_commit_logs(commit_logs: str) -> List[CommitLog]:
    parsed_commit_logs = list()
    for commit_log in commit_logs.split('\n'):
        if len(commit_log) > 3:

            # parse comment
            commit_log_parts = commit_log.split('\t', 1)
            if len(commit_log_parts) != 2:
                raise MalformedCommitLog()
            comment = commit_log_parts[1]

            # parse attributes
            attributes = commit_log_parts[0].split(' ')
            if len(attributes) < 6:
                raise MalformedCommitLog()
            parent_commit_id, commit_id = attributes[:2]

            attributes = list(reversed(attributes[2:]))
            timezone, timestamp, user_email = attributes[:3]
            user_name = ' '.join(attributes[3:])

            # parse timestamp
            try:
                parsed_timestamp: datetime = datetime.fromtimestamp(int(timestamp))
            except:
                raise MalformedCommitLog()

            parsed_commit_logs.append(CommitLog(
                parent_commit_id=parent_commit_id,
                commit_id=commit_id,
                user_name=user_name,
                user_email=user_email,
                timestamp=parsed_timestamp,
                timezone=timezone,
                comment=comment,
            ))

    return parsed_commit_logs