import requests
import json
import os
from datetime import date
from awscli.clidriver import create_clidriver

def aws_cli(*cmd):
    old_env = dict(os.environ)
    try:

        # Environment
        env = os.environ.copy()
        env['LC_CTYPE'] = u'en_US.UTF'
        os.environ.update(env)

        # Run awscli in the same process
        exit_code = create_clidriver().main(*cmd)

        # Deal with problems
        if exit_code > 0:
            raise RuntimeError('AWS CLI exited with code {}'.format(exit_code))
    finally:
        os.environ.clear()
        os.environ.update(old_env)

if __name__ == "__main__":

	dir_path = os.path.dirname(os.path.realpath(__file__))
	auth_key = os.environ['PIWIK_API_KEY'] 
	start_date = date(2016, 1, 1)
	end_date = date(2018, 12, 31)

	sites = {
		1: "old-export",
		2: "inasafe",
		3: "learnosm",
		4: "summit",
		5: "website",
		6: "donate",
		7: "tasks",
		8: "osm-analytics",
		9: "oam-docs",
		10: "export",
		11: "visualize-change",
		12: "campaigns"
	}
	# download records by id, by day, since 2016/01/01
	for id, site in sites.items():

		print ("Archiving %s " % site)
		# check for directory
		site_path = os.path.join(dir_path, "archive/" + site)
		
		if not os.path.exists(site_path):
			# Make the directory
			try:
				os.mkdir(site_path)
			except OSError:  
			    print ("Creation of the directory %s failed" % path)

		request_string = ("https://piwik.hotosm.org/index.php?module=API&method=API.get&format=CSV&"
						  "idSite={0}&period=day&date={1},{2}&filter_limit=false&format_metrics=1&"
						  "expanded=1&translateColumnNames=1&language=en&token_auth={3}".format(id, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"), auth_key))
		print(request_string)
		r = requests.get(request_string)
		# validate the response
		if r.status_code == 200:
			with open(os.path.join(site_path, '{0}.csv'.format(site)), 'w') as outfile:
				outfile.write(r.text)
	
	# sync to s3
	print("Syncing files to s3 bucket hotosm-backups")
	aws_cli(['s3', 'sync', os.path.join(dir_path, 'archive/'), 's3://hotosm-backups/piwik/archive', '--delete'])
