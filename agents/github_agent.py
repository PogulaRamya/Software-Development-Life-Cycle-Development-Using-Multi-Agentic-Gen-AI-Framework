import os
os.environ["GIT_PYTHON_REFRESH"] = "quiet"
import git

def push_to_github(repo_path, commit_message, branch_name="main"):
    """
    Pushes the code to the GitHub repository.
    """
    repo = git.Repo(repo_path)
    repo.git.add(all=True)
    repo.index.commit(commit_message)
    origin = repo.remote(name='origin')
    origin.push(branch_name)
