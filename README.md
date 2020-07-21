# Veracode Flaw Grouping Script

A simple example of usage of the Veracode API signing library provided on the [Veracode Help Center](https://help.veracode.com/reader/LMv_dtSHyb7iIxAQznC~9w/cCoBmgWWxUM4hOY54dTqgA) and the Findings API (release imminent) to group flaws in a veracode report for Jira import by some other means that 1 flaw = 1 ticket.

## Setup

Save Veracode API credentials in your user home folder `~/.veracode/credentials`
An example of how to create the Credentials file is also provided on the [Veracode Help Center](https://help.veracode.com/reader/LMv_dtSHyb7iIxAQznC~9w/zm4hbaPkrXi02YmacwH3wQ)

Install dependencies:

    cd veracode-usage-script
    pip install -r requirements.txt

Fix missing code:
- Select flaw grouping criteria or write own logic
- Complete transformation of json findings data into Jira inputs in format_output_for_jira_input function

## Run

Run by calling in a Terminal or cmd window:

    python flaw-grouping.py
    
Program will proimpt for inputs and results will be saved to a file in the present working directory for later import into JIRA [via json](https://confluence.atlassian.com/adminjiraserver/importing-data-from-json-938847609.html) or [via csv](https://confluence.atlassian.com/adminjiraserver/importing-data-from-csv-938847533.html) depending on how you have completed the missing code in the project.
