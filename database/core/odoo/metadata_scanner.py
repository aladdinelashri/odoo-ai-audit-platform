class OdooMetadataScanner:

    def __init__(self, metadata_service):
        self.metadata_service = metadata_service

    def scan(self):
        return self.metadata_service.get_tables()
