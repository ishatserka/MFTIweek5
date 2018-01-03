import datetime
import socket



class Client:
    
    def __init__(self, ip, port, timeout=None):
        self.ip = ip
        self.port = int(port)
        self.timeout = timeout
    
    def get(self, key=None):
        if key is None: key = "*"
        data = f"get {key}\n"
        data = self._send_info_to_server(data)
        
        dict_result = dict()
        
        if "error\n" in data: raise ClientError
        elif "ok\n\n" in data: return {}
        else:
            data = data[3:][:-2]
            key = None
            for part in data.split(sep="\n"):
                dict_part = part.split(sep=" ")
                key = dict_part[0]
                tup = (int(dict_part[2]), float(dict_part[1]))
                if key in dict_result:
                    dict_result[key].append(tup)
                else:
                    dict_result[key] = [tup]        
        
        return dict_result
        
        
    
    def put(self, key, value, timestamp = None):
        test_time = timestamp or str(int(time.time()))
        data = "put {} {} {}\n".format(key, value, test_time)
        self._send_info_to_server(data)

        
    def _send_info_to_server(self, data):
        result = None
        with socket.create_connection((self.ip, self.port), self.timeout) as sock:
            try:
                sock.sendall(data.encode("utf8"))
                result = sock.recv(1024)
            except:
                raise ClientError
            return result.decode("utf8")
    
        
class ClientError(BaseException):
    pass

