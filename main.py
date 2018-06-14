import requests
import json
import os
import sys

# Retrieve a list of all machines, following all pagination links.
def get_all_machines():
  machines = []
  link = "/v1/accounts/{account}/machines?page[size]={page_size}&page[number]={page_number}&policy={policy}".format(
    account=os.environ["KEYGEN_ACCOUNT_ID"],
    policy=os.environ["KEYGEN_POLICY_ID"],
    page_size=10,
    page_number=1
  )

  while link != None:
    res = requests.get(
      "https://api.keygen.sh/{link}".format(link=link.strip("/")),
      headers={
        "Authorization": "Bearer {token}".format(token=os.environ["KEYGEN_PRODUCT_TOKEN"]),
        "Content-Type": "application/vnd.api+json",
        "Accept": "application/vnd.api+json"
      }
    ).json()

    for machine in res["data"]:
      machines.append(machine)

    link = res["links"]["next"]

  return machines

# Check if the given fingerprint is associated with more than 1 license
# for this particular policy (we don't want to allow duplicates).
machines = get_all_machines()

# Exit early if no machines were found.
if len(machines) > 0:
  print("found {count} machines for policy {policy}".format(
    policy=os.environ["KEYGEN_POLICY_ID"],
    count=len(machines)
  ))
else:
  print("no machines found")

  sys.exit()

# Keep track of duplicate machine fingerprints.
seen = {}
dups = []

for machine in machines:
  fingerprint = machine["attributes"]["fingerprint"]
  if fingerprint not in seen:
    seen[fingerprint] = 1
  else:
    if seen[fingerprint] == 1:
      print("duplicate fingerprint: {fingerprint}".format(fingerprint=fingerprint))

      dups.append(machine)

    seen[fingerprint] += 1

# Exit early if no duplicates were found.
if len(dups) > 0:
  print("found {count} duplicate fingerprints for policy {policy}".format(
    policy=os.environ["KEYGEN_POLICY_ID"],
    count=len(dups)
  ))
else:
  print("no duplicate fingerprints found")

  sys.exit()

# If we've gotten this far, we've found some fingerprints which are associated
# with more than 1 license. Next, we'll suspend all these licenses. Suspending
# a license will not delete it, so the customer can still resolve the issue
# by deactivating one of the machines. You may want to send them an email.
license_ids = map(lambda m: m["relationships"]["license"]["data"]["id"], dups)

for license_id in license_ids:
  suspension = requests.post(
    "https://api.keygen.sh/v1/accounts/{account}/licenses/{license}/actions/suspend".format(account=os.environ["KEYGEN_ACCOUNT_ID"], license=license_id),
    headers={
      "Authorization": "Bearer {token}".format(token=os.environ["KEYGEN_PRODUCT_TOKEN"]),
      "Content-Type": "application/vnd.api+json",
      "Accept": "application/vnd.api+json"
    }
  ).json()

  if "errors" in suspension:
    errs = suspension["errors"]

    print("license suspension failed: {errors} ({license})".format(
      errors=map(lambda e: "{} - {}".format(e["title"], e["detail"]).lower(), errs),
      license=license_id
    ))

    continue

  print("license suspended: {}".format(license_id))