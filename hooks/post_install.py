import asyncio
import logging
import os

from apolo_kube_client.client import KubeClient, kube_client_from_config
from apolo_kube_client.errors import ResourceNotFound

from hooks.kube import create_kube_config

logger = logging.getLogger(__name__)


async def main():
    namespace = os.environ["NP_K8S_NS"]
    service_name = os.environ["SERVICE_NAME"]
    webhook_name = os.environ['WEBHOOK_NAME']
    webhook_path = os.environ['WEBHOOK_PATH']
    kube_config = create_kube_config()
    secret_name = f"admission-controller-certs-{service_name}"

    async with kube_client_from_config(kube_config) as kube:
        kube: KubeClient

        secret_value = await kube.get(f'{kube.namespace_url}/secrets/{secret_name}')
        ca_bundle = secret_value["data"]["ca.crt"]

        ac_name = f"{service_name}-admission-controller"

        # 6.2 Build MWC body
        mwc_body = {
            "apiVersion": "admissionregistration.k8s.io/v1",
            "kind": "MutatingWebhookConfiguration",
            "metadata": {
                "name": ac_name
            },
            "webhooks": [
                {
                    "name": webhook_name,
                    "admissionReviewVersions": ["v1", "v1beta1"],
                    "sideEffects": "None",
                    "clientConfig": {
                        "service": {
                            "namespace": namespace,
                            "name": service_name,
                            "path": webhook_path
                        },
                        "caBundle": ca_bundle
                    },
                    "rules": [
                        {
                            "operations": ["CREATE"],
                            "apiGroups": [""],
                            "apiVersions": ["v1"],
                            "resources": ["pods"],
                            "scope": "Namespaced"
                        }
                    ],
                    "failurePolicy": "Ignore",
                    "objectSelector": {
                        "matchLabels": {
                            "platform.apolo.us/storage-injection-webhook": "enabled"
                        }
                    }
                }
            ]
        }

        # 6.3 Check if MWC exists
        get_url = f"{kube._base_url}/apis/admissionregistration.k8s.io/v1/mutatingwebhookconfigurations/{ac_name}"
        create_url = f"{kube._base_url}/apis/admissionregistration.k8s.io/v1/mutatingwebhookconfigurations"

        try:
            response = await kube.get(get_url)
        except ResourceNotFound:
            await kube.post(create_url, json=mwc_body)
        else:
            return


if __name__ == '__main__':
    os.environ['NP_K8S_API_URL'] = 'https://34.135.39.6'
    os.environ['NP_K8S_AUTH_TYPE'] = 'token'
    os.environ['NP_K8S_TOKEN_PATH'] = '/tmp/token'
    os.environ['NP_K8S_NS'] = 'platform'
    os.environ['SERVICE_NAME'] = 'dsmyk-test-admission-controller'
    os.environ['WEBHOOK_NAME'] = 'dsmyk-test-pod-volume-injector.apolo.us'
    os.environ['WEBHOOK_PATH'] = '/mutate'

    asyncio.run(main())
