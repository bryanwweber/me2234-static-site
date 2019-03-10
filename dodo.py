import pysftp
from pathlib import Path
from getpass import getpass
from hashlib import sha256
import json
import tempfile

this_dir = Path(__file__).parent
cache_path = this_dir / "output" / "filecache.json"

DOIT_CONFIG = {"dep_file": ".build.db"}


def hash_files():
    cache = {}
    for f in (this_dir / "output").glob("**/*.*"):
        if f.name == "filecache.json":
            continue
        file_hash = sha256(f.read_bytes()).hexdigest()
        cache[str(f.relative_to(this_dir / "output"))] = file_hash
    with cache_path.open("w") as cache_file:
        json.dump(cache, cache_file)


def deploy_site():
    password = getpass()
    with cache_path.open("r") as cache_file:
        local_cache = json.load(cache_file)

    temp_dir = tempfile.TemporaryDirectory()
    temp_path = Path(temp_dir.name)
    remote_cache_path = temp_path / "remotecache.json"
    remote_path = Path("edu.uconn.engr.weberb/public_html/me2234")
    with pysftp.Connection(
        "weberb.engr.uconn.edu", username="bww09001", password=password
    ) as sftp:
        if sftp.exists(str(remote_path / "filecache.json")):
            sftp.get(str(remote_path / "filecache.json"), str(remote_cache_path))
            with remote_cache_path.open("r") as cache_file:
                remote_cache = json.load(cache_file)
            for f in (this_dir / "output").glob("**/*.*"):
                if f.name == "filecache.json":
                    continue
                file_name = str(f.relative_to(this_dir / "output"))
                local_hash = local_cache[file_name]
                remote_hash = remote_cache[file_name]
                if local_hash != remote_hash:
                    sftp.put(str(f), str(remote_path / file_name))
            sftp.put(str(cache_path), str(remote_path / "filecache.json"))
        else:
            sftp.put_r(str(this_dir / "output"), str(remote_path))


def task_git_pull():
    """Pull changes from upstream before building."""
    return {"actions": ["git pull"]}


def task_build_site():
    """Build the site using Nikola."""
    return {
        "actions": ["nikola build"],
        "targets": [this_dir / "output"],
        "task_dep": ["git_pull"],
    }


def task_hash_files():
    return {
        "actions": [hash_files],
        "task_dep": ["build_site"],
        "targets": [cache_path],
    }


def task_deploy_site():
    """Deploy the site using Nikola."""
    return {"actions": [deploy_site], "task_dep": ["hash_files"], "verbosity": 2}
