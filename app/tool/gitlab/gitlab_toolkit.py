from langchain_community.agent_toolkits.gitlab.toolkit import GitLabToolkit
from langchain_community.utilities.gitlab import GitLabAPIWrapper


def get_gitlab_tools():
    """
    Retorna todas as tools prontas do GitLab:
    - create_merge_request
    - list_merge_requests
    - get_merge_request
    - etc
    """
    gitlab = GitLabAPIWrapper()
    toolkit = GitLabToolkit(api_wrapper=gitlab)
    return toolkit.get_tools()