#huggingface-cli login
from huggingface_hub import HfApi
api = HfApi()
# api.create_repo(repo_id="thyroid", private=True)

# api.upload_folder(
#     folder_path="/Users/wangzhuoyang/Desktop/projects/thyroid/data",
#     repo_id="joooy94/thyroid_data",
#     repo_type="dataset",
# )

api.upload_file(
    path_or_fileobj="/Users/wangzhuoyang/Desktop/projects/thyroid/data/data.zip",
    repo_id="joooy94/thyroid_data",
    path_in_repo = 'data.zip',
    repo_type="dataset",
)
