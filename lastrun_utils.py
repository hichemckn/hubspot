from azure.storage.blob import BlobServiceClient


def get_last_written_entry_timestamp(blob_connection_string: str) -> str:
    blob_service_client = BlobServiceClient.  \
            from_connection_string(blob_connection_string)
    container_client = blob_service_client.   \
            get_container_client("producerlogs")

    # Retrieve the last successful run time from the blob
    blob_client = container_client.get_blob_client("lastruntime.txt")
    blob_data = blob_client.download_blob()
    last_written_entry_timestamp = blob_data.readall().decode("utf-8")

    return last_written_entry_timestamp

def update_last_written_entry_timestamp(last_entry_timestamp: str,     
                            blob_connection_string: str) -> None:
    blob_service_client = BlobServiceClient.   \
                    from_connection_string(blob_connection_string)
    container_client = blob_service_client.    \
                    get_container_client("producerlogs")

    # Update the blob with the new last successful run time
    blob_client = container_client.get_blob_client("lastruntime.txt")
    blob_client.upload_blob(last_entry_timestamp, overwrite=True)
