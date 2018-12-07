# Piwik Archiving tool

This small tool will pull daily aggregated stats from the HOTOSM piwik site using their reporting API, then sync that with our AWS S3 backups bucket. 

## How to use

Install the dependencies
```bash
pip install -r requirements.txt
```

You will need the following environment variables set: 
```
export PIWIK_API_KEY= # This is found in the piwik super user admin page
```

You will also need to configure the `awscli` before running the python script by running
```
aws configure
```

and using the keys associated with your HOTOSM AWS account

Finally, run 
```
python piwik-archive.py
```
