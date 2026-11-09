"""Upload one staged image from the GitHub repository to the Hugging Face dataset.

Called by `.github/workflows/upload-image.yml` with these environment variables:

    HF_TOKEN               repository secret (never printed)
    INPUT_IMAGE_PATH       path of the image inside the checked-out repository
    INPUT_DESTINATION_NAME destination path inside the dataset, e.g. profiles/x.jpg
"""

import os
import sys
from pathlib import Path, PurePosixPath

from huggingface_hub import HfApi

REPO_ID = "mrhudlle/mr-huddle-images"
REPO_TYPE = "dataset"

ALLOWED_PREFIXES = ("profiles/", "gallery/", "teams/")
ALLOWED_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp"}
MAX_SIZE_BYTES = 8 * 1024 * 1024


def fail(message: str, code: int = 1):
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(code)


def main() -> None:
    token = os.environ.get("HF_TOKEN", "").strip()
    if not token:
        fail("HF_TOKEN is missing. Add it as a GitHub repository secret.")

    image_path = os.environ.get("INPUT_IMAGE_PATH", "").strip()
    destination_name = os.environ.get("INPUT_DESTINATION_NAME", "").strip()

    if not image_path or not destination_name:
        fail("Both image_path and destination_name are required.")

    workspace = Path.cwd().resolve()
    source = (workspace / image_path).resolve()

    # Never allow reading outside the checked-out repository.
    if not source.is_relative_to(workspace):
        fail("Image path is outside the repository.")
    if not source.is_file():
        fail(f"Image not found: {image_path}")

    destination = PurePosixPath(destination_name)
    if destination.is_absolute() or ".." in destination.parts:
        fail("Invalid destination path.")
    if not any(destination_name.startswith(prefix) for prefix in ALLOWED_PREFIXES):
        fail("Destination must be inside an allowed image folder.")
    if destination.suffix.lower() not in ALLOWED_SUFFIXES:
        fail("Unsupported image extension.")

    size = source.stat().st_size
    if size <= 0:
        fail("Image is empty.")
    if size > MAX_SIZE_BYTES:
        fail("Image exceeds the 8 MiB limit.")

    api = HfApi(token=token)

    # Verify repository access before uploading (fails fast on a bad token).
    api.repo_info(repo_id=REPO_ID, repo_type=REPO_TYPE)

    result = api.upload_file(
        path_or_fileobj=str(source),
        path_in_repo=destination_name,
        repo_id=REPO_ID,
        repo_type=REPO_TYPE,
        commit_message=f"Upload image: {destination_name}",
    )

    print("Upload successful.")
    print(f"Dataset: {REPO_ID}")
    print(f"Dataset path: {destination_name}")
    print(f"Commit result: {result}")


if __name__ == "__main__":
    main()
