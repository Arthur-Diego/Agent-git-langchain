from langchain_community.tools import tool
import subprocess
import tempfile
import os


def run_git(cmd: list[str]) -> str:
    result = subprocess.run(
        ["git"] + cmd,
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr)
    return result.stdout


@tool
def sync_branch_changes(
    source_branch: str,
    target_branch: str,
    commit_message: str
) -> str:
    """
    Sincroniza alterações de uma branch para outra usando diff/apply,
    evitando cherry-pick.
    """

    # checkout target
    run_git(["checkout", target_branch])

    # cria patch temporário
    with tempfile.NamedTemporaryFile(delete=False) as patch:
        patch_path = patch.name
        diff = run_git(["diff", f"{target_branch}..{source_branch}"])
        patch.write(diff.encode())

    # aplica patch
    run_git(["apply", patch_path])

    os.remove(patch_path)

    # commit e push
    run_git(["add", "."])
    run_git(["commit", "-m", commit_message])
    run_git(["push", "origin", target_branch])

    return f"Alterações de {source_branch} aplicadas em {target_branch} com sucesso."
