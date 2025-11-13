import os

# Define the entire backend structure as a dictionary
structure = {
    "backend": {
        "api": {
            "v1": {
                "auth": {
                    "router.py": "# Authentication routes\n",
                    "schemas.py": "# Authentication schemas\n",
                    "service.py": "# Authentication service logic\n"
                },
                "user": {
                    "router.py": "# User routes\n",
                    "schemas.py": "# User schemas\n",
                    "service.py": "# User service logic\n"
                },
                "__init__.py": ""
            },
            "__init__.py": ""
        },
        "core": {
            "config.py": "# Environment and settings management\n",
            "database.py": "# Database connection and Base model\n",
            "dependencies.py": "# Common dependencies for routes\n",
            "exceptions.py": "# Custom exception handlers\n",
            "logging.py": "# Logging configuration\n",
            "security.py": "# Token generation and password hashing\n"
        },
        "models": {
            "user.py": "# User model definition\n",
            "__init__.py": "# Expose all models\n"
        },
        "services": {
            "user_service.py": "# User-related business logic\n",
            "auth_service.py": "# Authentication-related business logic\n",
            "__init__.py": ""
        },
        "tests": {
            "test_auth.py": "# Tests for authentication module\n",
            "test_user.py": "# Tests for user module\n",
            "__init__.py": ""
        },
        "alembic": {},  # optional folder for migrations
        "main.py": "# Entry point for the FastAPI app\n",
        "requirements.txt": "# List of Python dependencies\n",
        ".env": "# Environment variables\n",
        ".gitignore": "# Ignore Python cache, venv, etc.\n",
        "README.md": "# Backend project documentation\n"
    }
}


def create_structure(base_path, structure_dict):
    """Recursively create directory and file structure."""
    for name, content in structure_dict.items():
        path = os.path.join(base_path, name)

        if isinstance(content, dict):
            # It's a folder
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            # It's a file
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)


if __name__ == "__main__":
    base_directory = os.getcwd()  # Create structure in the current working directory
    create_structure(base_directory, structure)
    print("✅ Backend project structure initialized successfully!")
