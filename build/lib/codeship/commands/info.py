import json
import yaml

def command(api=None, project_uuid=None):
    result = api.get_project(project_uuid)
    print yaml.safe_dump(result['project'], default_flow_style=False, indent=2)
