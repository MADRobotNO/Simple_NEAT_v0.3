class Connection:

    def __init__(self, connection_id, from_node_id, to_node_id, enabled=True, recursive=False):
        self.connection_id = connection_id
        self.from_node_id = from_node_id
        self.to_node_id = to_node_id
        self.enabled = enabled
        self.recursive = recursive
