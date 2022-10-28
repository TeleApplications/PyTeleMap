import socket
import time
from threading import Thread, Lock


class PortScanner:
    def __init__(self, ip_address: str) -> None:
        self.ip_address = ip_address
        self.__opened_ports = list()
        self.lock = Lock()

    def scan_port_range(self, start: int = 0, end: int = 65536, step: int = 1) -> list:
        """
        Scans all device ports
        :param start: starting port number
        :param end: ending port number
        :param step: step interval
        :return: list of opened and closed ports
        """

        threads = (Thread(target=self.scan_port, args=(i,), ) for i in range(start, end, step))
        g = 0
        for thread in threads:
            if g % 5 == 0:
                time.sleep(.01)
            thread.start()
            g += 1

        for thread in threads:
            thread.join()

        return self.__opened_ports

    def scan_port(self, port: int) -> int or None:
        """
        Scans device port
        :param port: port number which will be scaned
        :return: returns opened port number or None
        """

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex((self.ip_address, port)) == 0:
                self.__opened_ports.append(port)
        return self.__opened_ports


if __name__ == '__main__':
    p = PortScanner("10.0.0.53")
    print(p.scan_port_range(1, 65536))