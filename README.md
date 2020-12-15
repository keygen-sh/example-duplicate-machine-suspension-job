# Example Duplicate Machine Suspension Job

⚠️ **NOTICE: this can now be enforced at the license policy level using
the policy's [fingerprint uniqueness strategy](https://keygen.sh/docs/api/#policies-object-attrs-fingerprintUniquenessStrategy)
attribute. No need to run a background job.** We're leaving this here
for educational purposes, as an example for other types of jobs. ⚠️

This is an example of a job which can be run that is responsible for
suspending licenses associated with a duplicate machine fingerprint,
allowing you to enforce fingerprint uniqueness across a policy. This
is especially useful for disallowing trial licenses for a machine
that has previously completed a trial evaluation.

## Running the example

First up, configure a few environment variables:

```bash
# Keygen product token (don't share this!)
export KEYGEN_PRODUCT_TOKEN="YOUR_KEYGEN_PRODUCT_TOKEN"

# Your Keygen account ID (find yours at: https://app.keygen.sh/settings)
export KEYGEN_ACCOUNT_ID="YOUR_KEYGEN_ACCOUNT_ID"

# The Keygen policy to scope duplicate checks for. This is especially
# useful for when you want to disallow duplicates for a free trial
# policy, but not for the full version of your software.
export KEYGEN_POLICY_ID="YOUR_KEYGEN_POLICY_ID"
```

You can either run each line above within your terminal session before
starting the app, or you can add the above contents to your `~/.bashrc`
file and then run `source ~/.bashrc` after saving the file.

Next, install dependencies with [`pip`](https://packaging.python.org/):

```
pip install -r requirements.txt
```

## Manually running the job

To check for duplicate fingerprints and suspend the associated licenses,
run the script manually:

```
python main.py
```

The script does not handle running the job in an interval. That should be
handled with a job scheduler, such as `crontab`.

## Questions?

Reach out at [support@keygen.sh](mailto:support@keygen.sh) if you have any
questions or concerns!
