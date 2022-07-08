#!/usr/bin/python3
import os
import shutil
import subprocess
import sys

srcDir = sys.argv[1]
sonarParams="/k:Ansys:SpeosSC01 ";
branch="dev";

propertiesFile = f"{srcDir}/sonar-project.properties"
if os.path.exists(propertiesFile):
	with open(propertiesFile, 'r') as file:
		data = file.read().replace('sonar.', '/d:sonar.').replace('\n',' ')
		sonarParams += f"{data} "

exclusionFile = f"{srcDir}/.sonar-exclusions"
if os.path.exists(exclusionFile):
	with open(exclusionFile, 'r') as file:
		data = file.read().replace('\n', ',')
		sonarParams += f"/d:sonar.exclusions=\"{data}\" "

isPR = "SYSTEM_PULLREQUEST_PULLREQUESTID" in os.environ
if isPR:
	srcBranch = os.getenv('SYSTEM_PULLREQUEST_SOURCEBRANCH').replace('refs/heads/', '')
	tgtBranch = os.getenv('SYSTEM_PULLREQUEST_TARGETBRANCH').replace('refs/heads/', '')
	sonarParams += f'/d:sonar.pullrequest.branch={srcBranch} '
	sonarParams += f'/d:sonar.pullrequest.base={tgtBranch} '
	sonarParams += f'/d:sonar.pullrequest.key={os.getenv("SYSTEM_PULLREQUEST_PULLREQUESTID")} '
else:
	branch = os.getenv('BUILD_SOURCEBRANCH').replace('refs/heads/', '')
	sonarParams += f'/d:sonar.branch.name={branch} '
	sonarParams += f'/d:sonar.cppcheck.reportPath={buildDir}\cppcheck-report.xml '

print(sonarParams)

