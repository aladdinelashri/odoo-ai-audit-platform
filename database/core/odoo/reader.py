class OdooReader:

    def read(self, model, domain=None):
        return {
            "model": model,
            "domain": domain or []
        }
