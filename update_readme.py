import os
from github import Github
from datetime import datetime, timezone

# Initialize GitHub client
g = Github(os.environ["GITHUB_TOKEN"])

user = g.get_user("moha-abdi")

repo_names_branches = {
    "Sarifle": "fariid-rebrand",
    "SIPUserRegistrar": "main",
    "TronWatch": "main",
    "baileys-api": "main",
}

repo_info = []
for name, branch in repo_names_branches.items():
    try:
        repo = user.get_repo(name)
        branch_info = repo.get_branch(branch)
        last_updated_dt = branch_info.commit.last_modified_datetime or repo.updated_at
        last_updated = last_updated_dt.astimezone(timezone.utc)

        time_diff = datetime.now(timezone.utc) - last_updated

        if time_diff.days == 0:
            if time_diff.seconds < 3600:
                update_text = "within the last hour"
            elif time_diff.seconds < 86400:
                update_text = f"{time_diff.seconds // 3600} hours ago"
            else:
                update_text = "today"
        elif time_diff.days == 1:
            update_text = "yesterday"
        elif time_diff.days < 7:
            update_text = f"{time_diff.days} days ago"
        elif time_diff.days < 30:
            update_text = f"{time_diff.days // 7} weeks ago"
        else:
            update_text = f"{time_diff.days // 30} months ago"

        repo_name = "Fariid" if repo.name == "sarifle" else repo.name
        repo_info.append(
            {
                "name": repo_name,
                "description": repo.description or "*No description provided*",
                "language": repo.language,
                "private": repo.private,
                "fork": repo.fork,
                "updated": update_text,
                "license": repo.license.name if repo.license else "No license",
                "topics": repo.get_topics(),
            }
        )
    except Exception as e:
        print(f"Error fetching repository {name}: {str(e)}")

# Read the README template
with open("README_template.md", "r") as file:
    readme_template = file.read()

# Generate the repository list
repo_list = ""
for repo in repo_info:
    repo_url = (
        f"https://github.com/moha-abdi/{repo['name']}"
        if repo["name"] != "Fariid"
        else "#"
    )
    privacy = "🔒 Private" if repo["private"] else "🌐 Public"
    fork_text = " (Fork)" if repo["fork"] else ""
    repo_list += f"### [{repo['name']}]({repo_url}) ({privacy}{fork_text})\n"
    repo_list += f"- **Description**: {repo['description']}\n"
    repo_list += f"- **Language**: {repo['language']}\n"
    if repo["topics"]:
        repo_list += (
            f"- **Tags**: {', '.join([f'`{topic}`' for topic in repo['topics']])}\n"
        )
    repo_list += f"- **License**: {repo['license']}\n"
    repo_list += f"- **Last Updated**: {repo['updated']}\n\n"

# Update the README
updated_readme = readme_template.replace("{{REPO_LIST}}", repo_list)

# Write the updated README
with open("profile/README.md", "w") as file:
    file.write(updated_readme)
