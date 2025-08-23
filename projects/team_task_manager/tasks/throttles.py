from rest_framework.throttling import UserRateThrottle,AnonRateThrottle

class BurstRateThrottle(UserRateThrottle):
    scope = 'burst'
    
class SustainedRateThrottle(AnonRateThrottle):
    scope = 'sustained'