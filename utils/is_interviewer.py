def is_interviewer(speaker: str, mappings: dict[str, bool] = {}) -> bool:
    if ("interviewer" in speaker.lower()):
        return True

    if ("interviewee" in speaker.lower()):
        return False

    if ("participant" in speaker.lower()):
        return False

    for name, interviewer in mappings.items():
        if (name.lower() in speaker.lower()):
            return interviewer

    return True
