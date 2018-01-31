import multiprocessing
import json
import math
import re

def find_term_in_result(result, term, args):
    projects = result['projects']
    for project in projects:
        text = json.dumps(project, indent=2)
        name = project['name']
        uuid = project['uuid']

        if not (term in text):
            continue

        print("\033[92m -> uuid=%s: %s\033[00m" % (uuid, name))
        if ('project_name_only' in args) and args.project_name_only:
            continue

        lines = json.dumps(project, indent=2).split('\n')
        for i, line in enumerate(lines):
            count = line.count(term)
            if count > 0:
                print("%s: %s" % (i, line.replace(term, '\x1b[6;30;42m' + term + '\x1b[0m')))
        print "\n"

def async_find_term_in_result(api, page, term, args):
    result = api.list_projects(page=page)
    return multiprocessing.Process(target=find_term_in_result, args=(result, term, args))

def command(api=None, args=None, term=None):
    jobs = []
    result = api.list_projects()

    p = multiprocessing.Process(target=find_term_in_result, args=(result, term, args))
    jobs.append(p)
    p.start()

    total=result["total"]
    current_page=result["page"]
    per_page=result["per_page"]
    num_pages = int(math.ceil(float(total)/float(per_page)))

    for i in range(num_pages - 1):
        page = (i + 2)
        p = async_find_term_in_result(api, page, term, args)
        jobs.append(p)
        p.start()

    for job in jobs:
        job.join()
