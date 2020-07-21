import sys
import requests
import json
from datetime import datetime
from collections import defaultdict
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC

appsec_base = "https://api.veracode.com/appsec/v1"
findings_base = "https://api.veracode.com/appsec/v2"
headers = {"User-Agent": "Python HMAC Example"}


def main():
    done = False
    while not done:
        app = get_app()
        if not app:
            print("No apps found")
            sys.exit(1)
        print("Selected app: "+app[0]+", guid: "+app[1])
        findings = get_findings(app)
        findings_dict = group_findings(findings)
        output = format_output_for_jira_input(findings_dict)
        filename = app[0]+'_jira_export_'+datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
        save_to_file(filename, output)
        done = check_if_done()


def get_app():
    print("Locating apps...")
    result = ()
    response = make_api_call(appsec_base+"/applications")
    if response.ok:
        data = response.json()
        apps = [(e["profile"]["name"], e["guid"]) for e in data["_embedded"]["applications"]]
        print("Select app from list:")
        i = 1
        for app in apps:
            print("    "+str(i)+". "+app[0])
            i += 1
        s = input("select app number: ")
        result = apps[s-1]
    return result


def get_findings(app):
    findings = []
    response = make_api_call(findings_base+"/applications/"+app[1]+"/findings?scan_type=STATIC")
    if response.ok:
        data = response.json()
        findings = data["_embedded"]["findings"]
    return findings

def group_findings(findings):
    # change this to whatever grouping logic required

    # example group by module:
    # result = defaultdict(list)
    # for finding in findings:
    #     if finding["scan_type"] == "STATIC":
    #         module = finding["finding_details"]["module"]
    #         result[module].append(finding)
    # return result

    # example group by filepath:
    result = defaultdict(list)
    for finding in findings:
        if finding["scan_type"] == "STATIC":
            file_path = finding["finding_details"]["file_path"]
            result[file_path].append(finding)
    return result


def format_output_for_jira_input(output):
    # TODO complete
    # output is a python dictionary of findings grouped via logic above
    # follow Jira recommendations
    # easiest way appears to be JSON or csv:
    # https://confluence.atlassian.com/adminjiraserver/importing-data-from-json-938847609.html
    # https://confluence.atlassian.com/adminjiraserver/importing-data-from-csv-938847533.html
    output_string = ""
    for key, value in output.items():
        output_string += "{0}: {1}\n".format(key, value) 
    return output_string


def save_to_file(filename, output):
    with open(filename, 'w') as file:
        file.write(output)


def check_if_done():
    answer = True
    while True:
        reply = raw_input("Would you like to group findings for another app? (y/n) ").lower().strip()
        if reply.startswith('y'):
            answer = False
            break
        elif reply.startswith('n'):
            answer = True
            break 
    return answer


def make_api_call(url):
    try:
        return requests.get(url, auth=RequestsAuthPluginVeracodeHMAC(), headers=headers)
    except requests.RequestException as e:
        print("Whoops!")
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
