from kubernetes import client, config


class KubeConnector:
    def __init__(self):
        config.load_kube_config()
        self.v1 = client.CoreV1Api()

    def get_secret(name: str):
        pass
