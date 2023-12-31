"""
This script generates a migration from `main` to a `remote` feature `branch`.
You do not need to make use of this script for development/staging purposes,
because we always reset the database to a common starting point during dev.

This script is only needed when generating a migration for production to the
csxl.unc.edu primary deployment database.

Usage: python3 -m backend.script.generate_migration [remote] [branch]
"""

import subprocess
import sys
import argparse

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


def main() -> None:
    # Create the parser
    parser = argparse.ArgumentParser(
        description="Generate a migration, from `main` to a `remote` feature `branch`."
    )

    # Add the required argument for the branch name
    parser.add_argument("remote", help="Name of the git remote", type=str)
    parser.add_argument("branch", help="Name of the git branch", type=str)

    # Parse the arguments
    args = parser.parse_args()

    # Use the branch name from the arguments
    remote_name = args.remote
    branch_name = args.branch

    if can_switch_branch():
        print("✅ No uncommitted work")
    else:
        print("❌ Uncommitted files, please ensure all changes are committed.")
        sys.exit(1)

    if git_fetch_all():
        print("✅ Fetched all git branches")
    else:
        print("❌ Failed to fetch all git branches.")
        sys.exit(1)

    if branch_exists(branch_name):
        print(f"✅ Branch `{branch_name}` exists")
    else:
        print(f"❌ Branch {branch_name} does not exist, double check spelling.")
        sys.exit(1)

    if switch_branch("main"):
        print("✅ Switched to `main` branch")
    else:
        print("❌ Failed to switch to main branch.")
        sys.exit(1)

    # if pull_remote_branch(remote_name, "main"):
    #     print(f"✅ Pulled latest changes from {remote_name}/main")
    # else:
    #     print(f"❌ Failed to pull latest changes from {remote_name}/main.")
    #     sys.exit(1)

    if run_backend_script("reset_testing"):
        print("✅ Reset database to production schema")
    else:
        print("❌ Failed to reset database to production schema.")
        sys.exit(1)

    if alembic_stamp_head():
        print("✅ alembic stamp head - migration at production")
    else:
        print("❌ Failed to alembic stamp head.")
        sys.exit(1)

    if switch_branch(branch_name):
        print(f"✅ Switched to branch `{branch_name}`")
    else:
        print(f"❌ Failed to switch to branch {branch_name}.")
        sys.exit(1)

    if pull_remote_branch(remote_name, branch_name):
        print(f"✅ Pulled latest changes from {remote_name}/{branch_name}")
    else:
        print(f"❌ Failed to pull latest changes from {remote_name}/{branch_name}.")
        sys.exit(1)

    if alembic_generate_migration(branch_name):
        print(f"✅ alembic revision generated")
    else:
        print(f"❌ Failed to generate alembic revision")
        sys.exit(1)


def can_switch_branch() -> bool:
    # Command to check the status of the repository, ignoring untracked files
    command = "git status --porcelain -uno"

    # Run the command
    result = subprocess.run(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    # Check the output
    if result.stdout.strip():
        # Changes are present, cannot switch branches safely
        return False
    else:
        # No changes, safe to switch branches
        return True


def git_fetch_all() -> bool:
    result = subprocess.run(
        ["git", "fetch", "--all"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.returncode == 0


def branch_exists(branch: str) -> bool:
    result = subprocess.run(
        ["git", "branch", "-a"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return branch in result.stdout


def switch_branch(branch: str) -> bool:
    result = subprocess.run(
        ["git", "checkout", branch],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.returncode == 0


def pull_remote_branch(remote: str, branch: str) -> bool:
    result = subprocess.run(
        ["git", "pull", "--ff-only", remote, branch],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.returncode == 0


def run_backend_script(script_name: str) -> bool:
    result = subprocess.run(
        ["python3", "-m", f"backend.script.{script_name}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.returncode == 0


def alembic_stamp_head() -> bool:
    result = subprocess.run(
        ["alembic", "stamp", "head"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.returncode == 0


def alembic_generate_migration(branch_name: str) -> bool:
    result = subprocess.run(
        ["alembic", "revision", "--autogenerate", "-m", f"Migration for {branch_name}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.returncode == 0


if __name__ == "__main__":
    main()
