# Install dependencies

```bash
pip3 install -r requirements.txt
```

# Download all state files

```bash
download_state_files.py --host example.scalr.io --token xxx --output-dir /tmp/scalr-state-files
```

# Environment variables

Instead of providing the host and token on the command line, you can set the following environment variables:

```bash
export SCALR_HOST=example.scalr.io
export SCALR_TOKEN=xxx
```

# Automatically upload state file to s3 bucket

Put the following in the "POST-APPLY" hook:

```bash
aws s3 cp <(terraform show) s3://my-bucket/my-state.json
```

Make sure to set the following environment variables in your workspace:

```bash
AWS_ACCESS_KEY_ID=your_access_key_id
AWS_SECRET_ACCESS_KEY=your_secret_access_key
```
