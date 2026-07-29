import time

class OdooModelDiscovery:
    # ... existing __init__

    def discover_fields(self, model_name, max_retries=3, delay=1):
        for attempt in range(max_retries):
            try:
                return self.client.search_read(
                    'ir.model.fields',
                    [('model', '=', model_name), ('store', '=', True)],
                    ['name', 'field_description', 'ttype', 'relation', 'required', 'readonly', 'size']
                )
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                time.sleep(delay)
