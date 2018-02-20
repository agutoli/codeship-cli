import yaml
import json

def command(api=None):
    result = api.list_projects()
    print "Page: %s" % result['page']
    print "Total: %s" % result['total']
    #
    # with open('data.yaml', 'w') as yml:
    #     environment_variables = result['projects'][0]['environment_variables']
    #     setup_commands =
    #     yaml.safe_dump(result['projects'][0], yml, default_flow_style=False, indent=4)
