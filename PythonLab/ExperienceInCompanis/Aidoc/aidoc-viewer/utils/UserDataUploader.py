import os
import shutil
from werkzeug.utils import secure_filename


class UserDataUploader:
    def __init__(self, upload_folder, max_content_length=5):

        self.upload_folder = upload_folder

        # assume input in GB
        self.max_content_length = max_content_length * 1024 * 1024 * 1024

    def upload_files(self, files_to_upload, to_dir, overwrite=False):
        new_files = 0
        total_files = 0

        if not files_to_upload:
            return self.create_upload_summary(new_files, total_files)

        for file in files_to_upload:
            if file.filename == '':
                continue

            total_files = total_files + 1
            if self.upload_file(file, to_dir, overwrite):
                new_files = new_files + 1

        return self.create_upload_summary(new_files, total_files)

    #TODO: IB - Ask Anna if we want this version of upload_file in postg too
    def upload_file(self, file, to_dir, overwrite=False):
        if file:
            up_dir = os.path.join(self.upload_folder, "")
            if not os.path.exists(up_dir):
                os.makedirs(up_dir)

            filename = secure_filename(file.filename)
            file_path = os.path.join(up_dir, filename)
            file.save(file_path)
            file.close()

            dst_file = os.path.join(to_dir, filename)
            return self.copy_file(file_path, dst_file, overwrite)
        else:
            return False

    def copy_file(self, src, dest, overwrite=False):
        if not overwrite and os.path.exists(dest):
            return False
        else:
            shutil.copyfile(src, dest)
            return True

    def clean(self):
        if os.path.exists(self.upload_folder):
            shutil.rmtree(self.upload_folder)

    def create_upload_summary(self, new, total):
        if new == total:
            return str(total) + ' files uploaded.'
        else:
            return str(new) + ' out of ' + str(total - new) + ' files uploaded. Duplicate files were ignored.'
