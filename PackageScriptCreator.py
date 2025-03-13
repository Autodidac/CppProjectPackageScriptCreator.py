import os
import json
import subprocess

def analyze_project_structure(project_root, exclude_self=True):
    project_files = {}
    
    # Walk the project directory and exclude the "build" folder
    for root, dirs, files in os.walk(project_root):
        # Exclude the build directory so its files are not added
        dirs[:] = [d for d in dirs if d.lower() != "build"]
        if exclude_self:
            files = [f for f in files if f != "PackageScriptConstructor.py"]
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, project_root)
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            project_files[relative_path] = content
    
    return project_files

def generate_script(project_root, output_script):
    exclude_self = input("Exclude this script from the package? (y/n): ").strip().lower() == 'y'
    project_files = analyze_project_structure(project_root, exclude_self)
    
    # The generated script will recreate the project files in a folder named after the project,
    # then create a build folder and run CMake.
    script_content = f"""import os
import json
import subprocess

def create_project_files(root):
    files = {json.dumps(project_files, indent=4)}
    
    for rel_path, content in files.items():
        full_path = os.path.join(root, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

def run_cmake(root):
    build_dir = os.path.join(root, "build")
    os.makedirs(build_dir, exist_ok=True)
    subprocess.run(["cmake", ".."], cwd=build_dir, check=True)
    print("CMake configuration completed.")

if __name__ == "__main__":
    # Extract the project name from this script's filename (expected format: generate_<ProjectName>.py)
    script_name = os.path.basename(__file__)
    prefix = "generate_"
    suffix = ".py"
    if script_name.startswith(prefix) and script_name.endswith(suffix):
        project_name = script_name[len(prefix):-len(suffix)]
    else:
        project_name = "GeneratedProject"
    target_folder = project_name
    os.makedirs(target_folder, exist_ok=True)
    create_project_files(target_folder)
    print("Project files created in:", target_folder)
    run_cmake(target_folder)
"""
    
    with open(output_script, "w", encoding="utf-8") as f:
        f.write(script_content)
    
    print(f"Script {output_script} generated successfully.")

if __name__ == "__main__":
    # Set the project root to the directory where this constructor script resides.
    project_root = os.path.dirname(os.path.abspath(__file__))
    # The generated script's name will include the project name.
    output_script = f"generate_{os.path.basename(project_root)}.py"
    generate_script(project_root, output_script)
