import os
import json

def analyze_project_structure(project_root):
    project_files = {}
    
    for root, _, files in os.walk(project_root):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, project_root)
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            project_files[relative_path] = content
    
    return project_files

def generate_script(project_root, output_script):
    project_files = analyze_project_structure(project_root)
    
    script_content = f"""import os\n\n
def create_project_files(root):\n    files = {json.dumps(project_files, indent=4)}\n    \n    for rel_path, content in files.items():\n        full_path = os.path.join(root, rel_path)\n        os.makedirs(os.path.dirname(full_path), exist_ok=True)\n        with open(full_path, \"w\", encoding=\"utf-8\") as f:\n            f.write(content)\n\nif __name__ == \"__main__\":\n    project_root = \"{os.path.basename(project_root)}\"\n    create_project_files(project_root)\n    print(\"Project files created in:\", project_root)\n"""
    
    with open(output_script, "w", encoding="utf-8") as f:
        f.write(script_content)
    
    print(f"Script {output_script} generated successfully.")

if __name__ == "__main__":
    project_root = os.path.dirname(os.path.abspath(__file__))  # Change this to your actual project path
    output_script = "PackageInstallerScript.py"
    generate_script(project_root, output_script)