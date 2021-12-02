from os.path import basename, splitext


def get_filename_ext(filepath):
    base_name = basename(filepath)
    name, ext = splitext(base_name)
    return name, ext


def upload_file_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.id}-{instance.title}{ext}"
    return f"blogs/{final_name}"
