# AWS Route53 Exporter

The AWS Route53 Exporter enables Prometheus to collect metrics regarding the number of records within AWS Route53 hosted zones. This tool is essential for administrators and DevOps engineers who need to monitor their DNS records for capacity planning and operational health.

## Features

- **Record Count Metrics**: Exports the total count of Route53 records across all hosted zones in your AWS Route53 account.
- **Hosted Zone Specific Metrics**: Offers the ability to monitor record counts on a per-hosted-zone basis.
- **Flexible Configuration**: Easy to set up and configure with AWS credentials and region information.

## Getting Started

Before you begin, ensure you have Prometheus installed and running in your environment. This guide also assumes you have AWS CLI configured with access to your AWS account.

### Installation

1. Clone this repository to your local machine or server where Prometheus is running:

    ```bash
    git clone https://github.com/nexolabs/aws-route53-exporter.git
    cd aws-route53-exporter
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

- `route53_rrset_count`: The total number of AWS Route53 records for a specific hosted zones.
- `route53_rrset_limit`: The Limit of AWS Route53 records for a specific hosted zone.

## Security Considerations

Ensure that the AWS credentials used have minimal permissions, only allowing `ListResourceRecordSets` and `ListHostedZones` actions.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you have feedback, suggestions, or want to contribute code.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
