from base64 import b64encode

from kubernetes import client


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
        self.namespace = namespace

    def create_secret(self, name: str, data: dict) -> bool:
        data_encoded = {key: b64encode(data[key].encode()).decode() for key in data}
        self.api.create_namespaced_secret(self.namespace, {'data': data_encoded,
                                                  'metadata': {'name': name}})
        return True

    def get_secret(self, name: str):
        return self.api.read_namespaced_secret(name, self.namespace)

    def update_secret(self, name: str, key: str, value: str):
        return self.api.replace_namespaced_secret(name, self.namespace, None)

    def is_secret_existing(self, name: str):
        secret_list = self.api.list_namespaced_secret(self.namespace).items
        secret_list_names = [item.metadata.name for item in secret_list]
        return name in secret_list_names
