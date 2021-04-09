from config.config import get_settings
import os
import aiofiles
from fastapi.responses import FileResponse
from dependencies import ModelException


class FileManager:
    ''' File Manager Class for handling file operation.
    Users aiofiles modules
    '''

    def __init__(self, context: str):
        self.context = context

    def get_file(self, name: str):
        filename = self.get_path(name)
        # Remove file if it exists
        if os.path.exists(filename):
            return FileResponse(filename)

        raise ModelException.not_found("file {}".format(filename))

    async def save_file(self, name, file):
        # Get Filename and Path
        filename = self.get_path(name)
        # save file if dir exists
        async with aiofiles.open(filename, mode='wb+') as file_out:
            content = file.read()  # async read
            await file_out.write(content)  # async write

    def delete_file(self, name):
        filename = self.get_path(name)
        # Remove file if it exists
        if os.path.exists(filename):
            os.remove(filename)
        else:
            raise ModelException.not_found("Requested File")

    def get_path(self, name):
        # Get Setgigns for base Dirctory
        settings = get_settings()
        # Get ABslute path for file directory
        path = os.path.join(settings.base_path, self.context)
        # Check if path exists
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

        filename = os.path.join(path, name)

        return filename
