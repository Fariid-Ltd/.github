import os
from github import Github
from datetime import datetime, timezone

# Initialize GitHub client
g = Github(os.environ['TOKEN_GITHUB'])

# Get the user (your personal account)
user = g.get_user("moha-abdi")

# Specify the repositories we want to include
repo_names = ["Sarifle", "SIPUserRegistrar", "TronWatch", "baileys-api"]

# Prepare the repository information
repo_info = []
for name in repo_names:
    try:
        repo = user.get_repo(name)
        last_updated = repo.updated_at.astimezone(timezone.utc)
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
        
        repo_info.append({
            'name': repo.name,
            'description': repo.description or "*No description provided*",
            'language': repo.language,
            'private': repo.private,
            'fork': repo.fork,
            'updated': update_text,
            'license': repo.license.name if repo.license else "No license",
            'topics': repo.get_topics()
        })
    except Exception as e:
        print(f"Error fetching repository {name}: {str(e)}")

# Read the README template
with open('README_template.md', 'r') as file:
    readme_template = file.read()

# Generate the repository list
repo_list = ""
for repo in repo_info:
    privacy = "🔒 Private" if repo['private'] else "🌐 Public"
    fork_text = " (Fork)" if repo['fork'] else ""
    repo_list += f"### [{repo['name']}](https://github.com/moha-abdi/{repo['name']}) ({privacy}{fork_text})\n"
    repo_list += f"- **Description**: {repo['description']}\n"
    repo_list += f"- **Language**: {repo['language']}\n"
    if repo['topics']:
        repo_list += f"- **Tags**: {', '.join([f'`{topic}`' for topic in repo['topics']])}\n"
    repo_list += f"- **License**: {repo['license']}\n"
    repo_list += f"- **Last Updated**: {repo['updated']}\n\n"

# Update the README
updated_readme = readme_template.replace('{{REPO_LIST}}', repo_list)

# Write the updated README
with open('profile/README.md', 'w') as file:
    file.write(updated_readme)