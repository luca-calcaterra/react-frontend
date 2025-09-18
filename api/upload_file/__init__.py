import logging
import azure.functions as func
from azure.storage.blob import BlobServiceClient
import os

connect_str = os.environ["AzureWebJobsStorage"]
container_name = "files"

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        file = req.files.get('file')
        if not file:
            return func.HttpResponse("No file uploaded", status_code=400)

        filename = file.filename
        blob_service = BlobServiceClient.from_connection_string(connect_str)
        blob_client = blob_service.get_blob_client(container=container_name,
                                                   blob=f"{filename}.txt")
        # Create empty blob
        blob_client.upload_blob(b"", overwrite=True)
        return func.HttpResponse(f"Created empty file {filename}.txt")
    except Exception as e:
        logging.error(e)
        return func.HttpResponse("Error occurred", status_code=500)
