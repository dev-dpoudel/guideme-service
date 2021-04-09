from config.config import get_settings
from fastapi import Response
from fastapi.responses import FileResponse
from dependencies import ModelException
import os
import aiofiles
import io
import zipfile


class FileManager:
    ''' File Manager Class for handling file operation.
    Users aiofiles modules
    '''

    def __init__(self, context: str, content: str = "image/*"):
        self._context = context
        self._content = content

    def set_context(self, context):
        ''' Set Context for Class '''
        self._context = context

    def set_content(self, content):
        ''' Set Context for Class '''
        self._content = content

    def get_path(self, name):
        # Get Setgigns for base Dirctory
        settings = get_settings()
        # Get ABslute path for file directory
        path = os.path.join(settings.base_path, self._context)
        # Check if path exists
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

        filename = os.path.join(path, name)

        return filename

    def get_file(self, name: str):
        filename = self.get_path(name)
        # Remove file if it exists
        if os.path.exists(filename):
            return FileResponse(filename, media_type=self._content)

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

    def get_zip(self, files):
        # Aggisn fillename for zip file
        zip_filename = "content.zip"
        # Create In-Memory zip file
        s = io.BytesIO()
        zip = zipfile.ZipFile(s, "w")
        settings = get_settings()
        dir = os.path.join(settings.base_path, self._context)

        # Write to Zip FIle
        for file in files:
            # Add file at correct path
            path = os.path.join(dir, file)
            zip.write(path, file)

        # Pack Zip
        zip.close()

        headers = {'Content-Disposition': f'attachment; filename={zip_filename}'}  # noqa
        return Response(s.getvalue(),
                        media_type="application/x-zip-compressed",
                        headers=headers
                        )
