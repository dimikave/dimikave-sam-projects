import os
import subprocess
import sys
from pathlib import Path
import yaml


def run_sam_build(service_name):
    """Run SAM build for the specified service from the service directory."""
    service_path = Path(service_name)

    # Change directory to the service path
    print(f"Changing directory to {service_path} and running 'sam build'...")
    try:
        result = subprocess.run(
            ["sam", "build"],
            cwd=service_path,
            capture_output=True,
            text=True,
            shell=True
        )
        if result.returncode != 0:
            print(f"Error during 'sam build':\n{result.stderr}")
            sys.exit(1)
        print(result.stdout)
    finally:
        print(f"Returning to root directory {Path.cwd()}")


def install_local_package(package_path, target_dir):
    """Install a local package into the specified target directory from the root directory."""
    print(f"Running pip install for {package_path} into {target_dir} from the root directory...")
    result = subprocess.run(
        ["pip", "install", "-t", target_dir, "."+package_path],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(f"Error installing {package_path}:\n{result.stderr}")
        sys.exit(1)
    print(result.stdout)


def get_function_directory_mapping(build_dir):
    """Parse template.yaml to map Lambda directories to their resource names."""
    template_path = build_dir / "template.yaml"
    print(template_path)
    function_dir_mapping = {}

    # Load template.yaml
    with open(template_path) as f:
        template = yaml.safe_load(f)

    # Map resource names to CodeUri directories
    for resource_name, resource_details in template.get("Resources", {}).items():
        if resource_details.get("Type") == "AWS::Serverless::Function":
            lambda_name = resource_details["Properties"].get("Handler", "")
            lambda_name = lambda_name.split(".")[0].replace("_", "-")
            print(lambda_name)
            print(resource_name)
            function_dir_mapping[lambda_name] = resource_name  # Map directory to resource name

    return function_dir_mapping


def process_requirements(service_name, build_dir, function_dir_mapping):
    """Process each Lambda function's requirements.txt within the service."""
    service_path = Path(service_name)

    # Iterate over Lambda function directories within the service
    for lambda_dir in service_path.iterdir():
        if lambda_dir.is_dir() and lambda_dir.name != ".aws-sam":
            req_file = lambda_dir / "src" / "requirements.txt"

            # Only process if requirements.txt exists in the src folder
            if req_file.exists():
                print(f"Processing requirements for Lambda function in {lambda_dir}...")

                # Read requirements.txt and install local packages
                with req_file.open() as f:
                    for line in f:
                        line = line.strip()

                        # Check if the line is a local package path with ../shared/
                        if line.startswith("../shared/"):
                            # Strip the initial "." from the path
                            package_path = line.lstrip(".")
                            print(lambda_dir.name)
                            target_dir_name = function_dir_mapping.get(lambda_dir.name)

                            target_dir = build_dir / target_dir_name
                            print(package_path)
                            print(target_dir)
                            install_local_package(package_path, target_dir)
            else:
                print(f"No requirements.txt found in {lambda_dir / 'src'}, skipping.")

def main():
    # Check for service name argument
    if len(sys.argv) != 2:
        print("Usage: python custom_sam_build.py <service-name>")
        sys.exit(1)

    service_name = sys.argv[1]
    build_dir = Path(service_name) / ".aws-sam" / "build"

    # Run SAM build and get function names
    run_sam_build(service_name)
    function_dir_mapping = get_function_directory_mapping(build_dir)

    # Process requirements with function directory mapping
    process_requirements(service_name, build_dir, function_dir_mapping)
    print(f"Build and installation of shared packages completed successfully for {service_name}.")


if __name__ == "__main__":
    main()
