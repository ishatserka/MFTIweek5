import datetime


class Client:
    def get(self, *keys):
        pass
    
    def put(self, key, value, timestp = None):
        test_time_str = str(timestp or datetime.datetime.microsecond())
        
        pass
    
    



class ClientError(BaseException):
    pass

