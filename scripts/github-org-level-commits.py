import requests
from datetime import datetime

# Configuration
token = "YOUR_ACCESS_TOKEN"  # Replace with your token
headers = {"Authorization": f"Bearer {token}"}
since = "2023-01-01T00:00:00Z"
until = "2023-01-31T23:59:59Z"
output_file = "github_org_commit_report.md"

# Function to get all organizations
def get_organizations(headers):
    orgs_url = "https://api.github.com/user/orgs"
    all_orgs = []
    page = 1
    
    while True:
        params = {"per_page": 100, "page": page}
        response = requests.get(orgs_url, headers=headers, params=params)
        orgs = response.json()
        
        if not orgs or response.status_code != 200:
            break

        all_orgs.extend([org['login'] for org in orgs if org['login'].startswith("TFE-")])
        page += 1
    
    return all_orgs

# Function to get all repositories for an organization
def get_all_repositories(org, headers):
    repos_url = f"https://api.github.com/orgs/{org}/repos"
    all_repos = []
    page = 1
    
    while True:
        params = {"per_page": 100, "page": page}
        response = requests.get(repos_url, headers=headers, params=params)
        repos = response.json()
        
        if not repos or response.status_code != 200:
            break

        all_repos.extend(repos)
        page += 1
    
    return all_repos

# Function to get all branches for a repository
def get_all_branches(org, repo_name, headers):
    branches_url = f"https://api.github.com/repos/{org}/{repo_name}/branches"
    response = requests.get(branches_url, headers=headers)
    return response.json() if response.status_code == 200 else []

# Function to count commits for a branch within a date range
def get_commit_count(org, repo_name, branch_name, since, until, headers):
    commits_url = f"https://api.github.com/repos/{org}/{repo_name}/commits"
    params = {"sha": branch_name, "since": since, "until": until, "per_page": 100}
    page = 1
    total_commits = 0

    while True:
        params["page"] = page
        response = requests.get(commits_url, headers=headers, params=params)
        commits = response.json()
        
        if not commits or response.status_code != 200:
            break
        
        total_commits += len(commits)
        page += 1

    return total_commits

# Main script to generate a table-format report
def generate_consolidated_report(since, until):
    with open(output_file, "w") as file:
        file.write(f"# GitHub Commits Consolidated Report\n")
        file.write(f"**Date Range:** {since} to {until}\n\n")

        organizations = get_organizations(headers)
        for org in organizations:
            file.write(f"## Organization: {org}\n")
            file.write("| Repository | Branch | Commit Count |\n")
            file.write("|------------|--------|--------------|\n")
            
            total_commit_count = 0
            repositories = get_all_repositories(org, headers)
            for repo in repositories:
                repo_name = repo['name']
                branches = get_all_branches(org, repo_name, headers)
                
                for branch in branches:
                    branch_name = branch['name']
                    commit_count = get_commit_count(org, repo_name, branch_name, since, until, headers)
                    total_commit_count += commit_count
                    file.write(f"| {repo_name} | {branch_name} | {commit_count} |\n")
            
            file.write(f"\n**Total Commits for {org}: {total_commit_count}**\n\n")
        
        print(f"Consolidated report generated: {output_file}")

# Run the script
generate_consolidated_report(since, until)
