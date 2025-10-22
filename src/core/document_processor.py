import os
from pathlib import Path
from fastapi import UploadFile
from markitdown import MarkItDown

class DocumentProcessor:
    """
    Processes uploaded documents by saving them temporarily, converting to
    Markdown, and then cleaning up the temporary file.
    """
    def __init__(self):
        self.upload_dir = Path("data/uploads")
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    def process(self, file: UploadFile) -> str:
        """
        Saves an uploaded file, converts it to Markdown, and deletes the temp file.
        """
        # Ensure filename is secure
        if not file.filename:
            raise ValueError("File has no name.")
        
        temp_file_path = self.upload_dir / Path(file.filename).name

        try:
            # Save the uploaded file to a temporary location
            with open(temp_file_path, "wb") as buffer:
                buffer.write(file.file.read())

            # Process the file from its path
            md = MarkItDown()
            result = md.convert(str(temp_file_path))
            return result.text_content

        finally:
            # Clean up the temporary file
            if temp_file_path.exists():
                os.remove(temp_file_path)
