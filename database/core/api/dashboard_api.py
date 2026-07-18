class DashboardAPI:

    def execute(self, request):
        return {
            "status": "ok",
            "dashboard": request,
        }
