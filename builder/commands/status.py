from core.project import get_project_info

def run():

    info = get_project_info()

    print("=" * 50)
    print(info["name"])
    print("=" * 50)

    print(f"Version : {info['version']}")
    print(f"Sprint : {info['sprint']}")

    print("=" * 50)
    