import os




class GCloudSync:

    """
    Parameters : 
    (a) gcp_bucket_name: bucket name in the GCS (Google CLoud Storage)
    (b) gcs_filename: name of the file present in the above gcp bucket, gcs_filename should match exactly
    (c) destination_dir: Local directory path or GCS dir path to download the file to
    (d) source_dir : source directory path from where we want to copy item(s)
    (e) source_filename : source filename (present inside source_dir) that we want to copy.
    (f) new_filename : name given to the file being downloaded from GCS
         
    """

    def sync_folder_to_gcloud(self, source_dir, source_filename, gcp_bucket_name ):

        command = f"gsutil cp {source_dir}/{source_filename} gs://{gcp_bucket_name}/"
     
        os.system(command)



    # This method downloads a specific file from a GCS bucket [Google Cloud Storage (GCS) bucket] to a 
    # local folder using the gsutil command-line tool.
    def sync_folder_from_gcloud(self, gcp_bucket_name, gcs_filename, destination_dir, new_filename):

        # gsutil cp ... : Google’s CLI command to copy files to/from bGCS buckets
        command = f"gsutil cp gs://{gcp_bucket_name}/{gcs_filename} {destination_dir}/{new_filename}"
        
        os.system(command)


