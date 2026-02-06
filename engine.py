# foundationai/engine.py
import os
import yaml
from dotenv import load_dotenv
load_dotenv()  # Loads .env variables

class FoundationAI:
    def __init__(self, workspace="foundation_workspaces", 
                 learning_sprint_path="learning_sprints"):
        self.workspace = workspace
        self.learning_sprint_path = learning_sprint_path
        os.makedirs(workspace, exist_ok=True)
        
        # Load default sprint config if exists
        self.sprint_config = yaml.safe_load(
            open(f"{learning_sprint_path}/speaking.yaml", "r")
        ) or {
            "default": {"data_sources": ["blogposts"], "tools": ["OpenAI"]}
        }
    
    def learn(self, instruction: str):
        """Executes learning sprint for any instruction"""
        # Step 1: Find relevant sprint config
        sprint_config = self.sprint_config.get(instruction.lower(), 
                                              self.sprint_config["default"])
        
        # Step 2: Generate code snippet using GitHub Actions template
        learning_code = f"""
def learn_{instruction.replace(' ', '_').lower()}():
    \"\"\"Auto-generated for '{instruction}'\"\"\"
    print(f"Learning {instruction}...")
    data_sources = {sprint_config['data_sources']}
    tools = {sprint_config['tools']}
    return {{
        "status": "success",
        "config": "{instruction}",
        "tools_used": tools
    }}
"""
        
        # Step 3: Auto-commit to GitHub (simulated)
        commit_message = f"feat({instruction}): added learning workflow"
        os.system(f'git add engine.py && git commit -m "{commit_message}"')
        
        return {
            "instruction": instruction,
            "code_snippet": learning_code[:120] + "...",
            "commit": commit_message,
            "tools": sprint_config["tools"]
        }
    
    def deploy(self, environment="dev"):
        """Deploy model to target environment"""
        # Logic for deploying via Docker Compose
        os.system(f'docker-compose -f docker-compose.{environment}.yml up -d')
        return f"Deployed to {environment}!"
