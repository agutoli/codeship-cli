import yaml
import os.path

def command():
    try:
        config = {
            "username": raw_input('-> Codeship username: '),
            "organization": raw_input('-> Codeship organization: ')
        }
    except KeyboardInterrupt:
        print "\nCancelling...\n"
        exit()

    filename = os.path.expanduser(os.path.join("~/", ".codeship"))

    with open(filename, 'w') as yml:
        yaml.safe_dump(config, yml, default_flow_style=False, indent=4)

    print "Saved at %s " % filename
