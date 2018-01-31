import multiprocessing
import json
import math
import re

def find_term_in_result(result, term, callback):
    projects = result['projects']
    for project in projects:
        text = json.dumps(project, indent=2)
        name = project['name']
        uuid = project['uuid']

        if not (term in text):
            continue

        print("\033[92m -> uuid=%s: %s\033[00m" % (uuid, name))
        lines = json.dumps(project, indent=2).split('\n')
        for i, line in enumerate(lines):
            count = line.count(term)
            if count > 0:
                # callback(project['name'], project['uuid'], count)
                print("%s: %s" % (i, line.replace(term, '\x1b[6;30;42m' + term + '\x1b[0m')))
        print "\n"

def async_find_term_in_result(api, page, term, callback):
    result = api.list_projects(page=page)
    return multiprocessing.Process(target=find_term_in_result, args=(result, term, callback))

def command(api=None, term=None, callback=None):
    jobs = []
    result = api.list_projects()

    p = multiprocessing.Process(target=find_term_in_result, args=(result, term, callback))
    jobs.append(p)
    p.start()

    total=result["total"]
    current_page=result["page"]
    per_page=result["per_page"]
    num_pages = int(math.ceil(float(total)/float(per_page)))

    for i in range(num_pages - 1):
        page = (i + 2)
        p = async_find_term_in_result(api, page, term, callback)
        jobs.append(p)
        p.start()

    for job in jobs:
        job.join()
