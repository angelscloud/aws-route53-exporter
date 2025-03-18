# AWS Route53 Exporter

The AWS Route53 Exporter enables Prometheus to collect metrics regarding the number of records and quotas within AWS Route53 hosted zones. This tool is essential for administrators and DevOps engineers who need to monitor their DNS records for capacity planning and operational health.

## Features

- **Record Count Metrics**: Exports the total count of Route53 records across specified hosted zones
- **Quota Monitoring**: Tracks various AWS Route53 quotas including hosted zones and delegation sets
- **Account-level Metrics**: Provides account-wide quota information
- **Flexible Configuration**: Easy to set up and configure with AWS credentials

## Prerequisites

- Python 3.x
- Prometheus server
- AWS account with Route53 access
- Required Python packages: flask, prometheus_client, boto3

## Getting Started

### Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/angelscloud/aws-route53-exporter.git
    cd aws-route53-exporter
    ```

2. Install required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

1. The exporter reads AWS credentials from your environment. Ensure you have your AWS access key ID and secret access key configured. 

2. Configure Prometheus to scrape the exporter endpoint. Add the following job to your `prometheus.yml` configuration file:

    ```yaml
    - job_name: 'aws-route53-exporter'
      static_configs:
      - targets: ['localhost:8000']
    ```

3. Reload Prometheus configuration.

### Metrics

The exporter provides the following metrics:

| Metric Name | Description | Labels | Type |
|------------|-------------|--------|------|
| `route53_rrset_count` | Current number of record sets in the hosted zone | `hosted_zone_name` | Gauge |
| `route53_rrset_limit` | Maximum number of record sets allowed in the hosted zone | `hosted_zone_name` | Gauge |
| `route53_hosted_zone_quota` | Maximum number of hosted zones that can be created | `account` | Gauge |
| `route53_delegation_sets_quota` | Maximum number of reusable delegation sets that can be created | `account` | Gauge |

### Running the Exporter

```bash
python route53.py
```
The exporter will run on port 8000 and metrics will be available at `/metrics`.

## Security Considerations

Ensure that the AWS credentials used have the following minimum permissions:
- `route53:GetHostedZone`
- `route53:GetHostedZoneLimit`
- `route53:GetAccountLimit`
- `sts:GetCallerIdentity`

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you have feedback, suggestions, or want to contribute code.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
