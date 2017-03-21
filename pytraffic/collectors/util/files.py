import time, os


def old_or_not_exists(file, age):
    if not os.path.isfile(file):
        return True
    last_modified = os.path.getmtime(file)
    now = time.time()
    return now - last_modified > age


def file_path(source_file, file):
    return os.path.join(os.path.dirname(os.path.realpath(source_file)), file)
