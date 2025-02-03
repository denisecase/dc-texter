# DEV NOTES

## A Note on Organization

pip requires a folder/package to install. 

Repository Name: dc-texter
  - Uses dashes (-) as allowed in GitHub repository names.
  - Cannot be used as a Python package name due to dashes.
  - Has no effect on Python package imports.
  - Nice if it matches the PyPi distribution name.
  - The PyPi distribution name is the package/project/folder name but with a dash not underscore, because Python I guess. 
  

Package (Folder) Name: dc_texter
  - Uses underscores (_) to ensure compatibility with Python imports.
  - Becomes an installable package when  __init__.py file is added.

File Name: etexter.py
  - The file name with a .py extension.
  - Can be executed as a script. 
  - We avoid using the file name in imports if we set up __init__.py correctly. 

pyproject.toml
  - [project] name = "dc_texter"`
  - Used for installation (`pip install dc_texter`).
  - The package folder should match.

```toml
[project]
name = "dc_texter" # install name

version = "0.1.0"

[tool.setuptools]
packages = ["dc_texter"] # list of package folders
```

## PyPI Publish With GitHub Actions

Log in to <https://pypi.org/> / Account Settings / Add API token.
All projects, name it same as repo. Copy the PyPi token. 

In GitHub, go to repo / settings / secrets / actions and make a new secret named PYPI_API_TOKEN (see publish.yml). Paste PyPi token.


## Versioning notes

- update pyproject.toml to new version, e.g., v0.1.1
- if didn't succeed, remove locally and remote first
```
git tag -d v0.1.1
git push origin --delete v0.1.1

git add .
git commit -m "v0.1.2"
git tag -a v0.1.1 -m "Release v0.1.2"
git push origin main
git push origin v0.1.2
```