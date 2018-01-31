import multiprocessing
import json
import math

def find_term_in_result(result, term, callback):
    projects = result['projects']
    for project in projects:
        count = json.dumps(project).count(term)
        if count > 0:
            callback(project['name'], project['uuid'], count)

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
