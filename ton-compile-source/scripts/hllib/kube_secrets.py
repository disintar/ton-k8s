from kubernetes import client, config


class KubeConnector:
    def __init__(self, namespace: str):
        """
        Interact with kubernetes secrets
        :param namespace:
        """

        configuration = client.Configuration()

        token = open('/etc/secret-volume/token').read()
        host = 'https://kubernetes.default.svc'
        ssl_ca_cert = '/etc/secret-volume/ca.crt'

        configuration.api_key["authorization"] = token
        configuration.api_key_prefix['authorization'] = 'Bearer'
        configuration.host = host
        configuration.ssl_ca_cert = ssl_ca_cert

        self.api = client.CoreV1Api(client.ApiClient(configuration))
        self.v1 = client.CoreV1Api()
        self.namespace = namespace

    def get_secret(self, name: str):
        return self.v1.read_namespaced_secret(name, self.namespace)

    def update_secret(self, name: str, key: str, value: str):
        return self.v1.replace_namespaced_secret(name, self.namespace, None)
