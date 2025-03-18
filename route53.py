import os
from flask import Flask, Response
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST
import threading
import time
from boto3.session import Session

app = Flask(__name__)

# Environment variables
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
HOSTED_ZONE_ID = os.environ.get('HOSTED_ZONE_ID')
AWS_SESSION_TOKEN = os.environ.get('AWS_SESSION_TOKEN')


rrset_limit_gauge = Gauge('route53_rrset_limit', 'The maximum number of record sets that can be created in the hosted zone', labelnames=['hosted_zone_name'])
rrset_count_gauge = Gauge('route53_rrset_count', 'The current number of record sets in the hosted zone', labelnames=['hosted_zone_name'])

# Add new Gauge metrics for hosted zone quotas and usage
hosted_zone_quota_gauge = Gauge('route53_hosted_zone_quota', 'The quota for the number of hosted zones that can be created', labelnames=['account'])
hosted_zone_usage_gauge = Gauge('route53_hosted_zone_usage', 'The current number of hosted zones being used', labelnames=['account'])

# Add new Gauge metrics for reusable delegation sets quota and usage
delegation_sets_quota_gauge = Gauge('route53_delegation_sets_quota', 'The quota for the number of reusable delegation sets that can be created', labelnames=['account'])
delegation_sets_usage_gauge = Gauge('route53_delegation_sets_usage', 'The current number of reusable delegation sets being used', labelnames=['account'])

def fetch_route53_limits():
    while True:
        session = Session(aws_access_key_id=AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                          aws_session_token=AWS_SESSION_TOKEN)
        client = session.client('route53')

        hosted_zone_details = client.get_hosted_zone(Id=HOSTED_ZONE_ID)
        hosted_zone_name = hosted_zone_details['HostedZone']['Name'][:-1]

        # Fetch record set limits
        limit_type = 'MAX_RRSETS_BY_ZONE'
        response = client.get_hosted_zone_limit(HostedZoneId=HOSTED_ZONE_ID, Type=limit_type)

        rrset_limit_gauge.labels(hosted_zone_name=hosted_zone_name).set(response['Limit']['Value'])
        rrset_count_gauge.labels(hosted_zone_name=hosted_zone_name).set(response['Count'])

        # Get AWS account ID
        account_id = session.client('sts').get_caller_identity()['Account']

        # Fetch hosted zone quota and usage
        account_limit = client.get_account_limit(Type='MAX_HOSTED_ZONES_BY_OWNER')
        hosted_zone_quota_gauge.labels(account=account_id).set(account_limit['Limit']['Value'])
        hosted_zone_usage_gauge.labels(account=account_id).set(account_limit['Count'])

        # Fetch delegation sets quota and usage
        delegation_sets_limit = client.get_account_limit(Type='MAX_REUSABLE_DELEGATION_SETS_BY_OWNER')
        delegation_sets_quota_gauge.labels(account=account_id).set(delegation_sets_limit['Limit']['Value'])
        delegation_sets_usage_gauge.labels(account=account_id).set(delegation_sets_limit['Count'])

        time.sleep(300)

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    threading.Thread(target=fetch_route53_limits, daemon=True).start()
    app.run(host='0.0.0.0', port=8000)
