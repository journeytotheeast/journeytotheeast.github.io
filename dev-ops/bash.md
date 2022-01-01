# Bash sample

```shell
#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo "Usage: ./ingest_from_crsbucket.sh  destination-bucket-name"
    exit
fi
BUCKET=$1
FROM=gs://data-science-on-gcp/flights/raw
TO=gs://$BUCKET/flights/raw
CMD="gsutil -m cp "
for MONTH in `seq -w 1 12`; do
  CMD="$CMD ${FROM}/2015${MONTH}.csv"
done
CMD="$CMD ${FROM}/201601.csv $TO"
echo $CMD
$CMD
```
`output`
```shell
gsutil -m cp gs://data-science-on-gcp/flights/raw/201501.csv gs://data-science-on-gcp/flights/raw/201502.csv gs://data-science-on-gcp/flights/raw/201503.csv gs://data-science-on-gcp/flights/raw/201504.csv gs://data-science-on-gcp/flights/raw/201505.csv gs://data-science-on-gcp/flights/raw/201506.csv gs://data-science-on-gcp/flights/raw/201507.csv gs://data-science-on-gcp/flights/raw/201508.csv gs://data-science-on-gcp/flights/raw/201509.csv gs://data-science-on-gcp/flights/raw/201510.csv gs://data-science-on-gcp/flights/raw/201511.csv gs://data-science-on-gcp/flights/raw/201512.csv gs://data-science-on-gcp/flights/raw/201601.csv gs://qwiklabs-gcp-00-3dc878e14873-ml/flights/raw
```

```
while [[ -z $SERVICE_IP ]]; do SERVICE_IP=$(kubectl get svc wp-repd-wordpress -o jsonpath='{.status.loadBalancer.ingress[].ip}'); echo "Waiting for service external IP..."; sleep 2; done; echo http://$SERVICE_IP/admin
```
