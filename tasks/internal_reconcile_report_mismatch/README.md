[![Known Vulnerabilities](https://snyk.io/test/github/nasa/cumulus-orca/badge.svg?targetFile=tasks/internal_reconcile_report_mismatch/requirements.txt)](https://snyk.io/test/github/nasa/cumulus-orca?targetFile=tasks/internal_reconcile_report_mismatch/requirements.txt)

**Lambda function internal_reconcile_report_mismatch **

Receives job id and page index from end user and returns reporting information of files that are missing from ORCA S3 bucket or have different metadata values than what is expected. 

Visit the [Developer Guide](https://nasa.github.io/cumulus-orca/docs/developer/development-guide/code/contrib-code-intro) for information on environment setup and testing.

- [Deployment](#deployment)
- [Input/Output Schemas and Examples](#input-output-schemas)
- [pydoc internal_reconcile_report_mismatch](#pydoc)

<a name="deployment"></a>
## Deployment
```
    see bin/build.sh to build the zip file. Upload the zip file to AWS.
    
```
<a name="input-output-schemas"></a>
## Input/Output Schemas and Examples
Fully defined json schemas written in the schema of https://json-schema.org/ can be found in the [schemas folder](schemas).

### Example Input
```json
{
  "jobId": 123,
  "pageIndex": 0
}
```
### Example Output
```json
{
  "jobId": 123,
  "anotherPage": false,
  "mismatches": [
    {
      "collectionId": "MOD09GQ___061",
      "granuleId": "MOD09GQ.A2017025.h21v00.006.2017034065109",
      "filename": "MOD09GQ.A2017025.h21v00.006.2017034065109.hdf",
      "keyPath": "MOD09GQ/006/MOD09GQ.A2017025.h21v00.006.2017034065109.hdf",
      "cumulusArchiveLocation": "cumulus-public",
      "orcaEtag": "d41d8cd98f00b204e9800998ecf8427",
      "s3Etag": "1f78ve1d3f41vbhg4nbb4kjhong4x14",
      "orcaGranuleLastUpdate": "2020-01-01T23:00:00Z",
      "s3FileLastUpdate": "2020-01-01T23:00:00Z",
      "orcaSizeInBytes": 6543277389,
      "s3SizeInBytes": 1987618731,
      "discrepancyType": "etag, size_in_bytes",
      "comments": null
    }
  ]
}
```
<a name="pydoc"></a>
## pydoc internal_reconcile_report_mismatch
[See the API documentation for more details.](API.md)