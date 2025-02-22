import os


class GCloudSync:

    """
    Parameters : 
    (a) gcp_bucket_url: bucket name in the gcp (bucket cloud)
    (b) filename: name of the file present in the above gcp bucket, filename should match exactly
    (c) destination: name given to the file being downloaded from the gcp bucket to our project directory.
    
    """

    def sync_folder_to_gcloud(self, gcp_bucket_url, filepath, filename):

        command = f"gsutil cp {filepath}/{filename} gs://{gcp_bucket_url}/"
        # command = f"gcloud storage cp {filepath}/{filename} gs://{gcp_bucket_url}/"
        os.system(command)

    def sync_folder_from_gcloud(self, gcp_bucket_url, filename, destination):

        command = f"gsutil cp gs://{gcp_bucket_url}/{filename} {destination}/{filename}"
        # command = f"gcloud storage cp gs://{gcp_bucket_url}/{filename} {destination}/{filename}"
        os.system(command)


