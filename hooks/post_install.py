import asyncio
import logging
import os

from apolo_kube_client.client import kube_client_from_config
from apolo_kube_client.errors import ResourceNotFound

from hooks.kube import create_kube_config, create_admission_controller, get_admission_controller

logger = logging.getLogger(__name__)


async def main():
    service_name = os.environ["SERVICE_NAME"]
    webhook_name = os.environ["WEBHOOK_NAME"]
    webhook_path = os.environ["WEBHOOK_PATH"]
    match_label_name = os.environ["MATCH_LABEL_NAME"]
    failure_policy = os.environ["FAILURE_POLICY"]

    kube_config = create_kube_config()

    async with kube_client_from_config(kube_config) as kube:
        try:
            await get_admission_controller(kube, service_name)
        except ResourceNotFound:
            await create_admission_controller(
                kube, service_name, webhook_name, webhook_path, failure_policy, match_label_name
            )
        else:
            return


if __name__ == '__main__':
    asyncio.run(main())
