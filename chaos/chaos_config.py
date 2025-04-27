from django_chaos_monkey.middleware import ChaosMonkeyMiddleware

class CustomChaosMonkeyMiddleware(ChaosMonkeyMiddleware):
    def process_request(self, request):
        # Custom chaos rules
        if 'dashboard' in request.path and self.roll_dice(0.05):
            # 5% chance of simulating database timeout on dashboard
            import time
            time.sleep(10)
        
        if 'client' in request.path and self.roll_dice(0.1):
            # 10% chance of returning server error for client actions
            from django.http import HttpResponse
            return HttpResponse('Chaos Error!', status=500)
        
        return super().process_request(request)