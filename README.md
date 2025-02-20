Apolo helm chart for an admission controller
---

Configuration
=============

Helm charts expects next values to be set:

```yaml
namespace: ...

apoloAdmissionController:
  serviceName: a name of the webhook service 
  webhookName: a name of the webhook
  webhookPath: a URL path on the webhook service
  matchLabelName: a label which future pods should defined, so admission controller will take the into account
  failurePolicy: one of Ignore or Fail
```