import select
import socket
import argparse


class Portube(object):
    DATA_BLOCK = 4096

    def __init__(self, laddr, lport, raddr, rport):
        self.l_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.r_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.l_connected = None
        self.r_connected = None
        self.laddr = laddr
        self.lport = lport
        self.raddr = raddr
        self.rport = rport

    # -tran
    # 本地开始监听port1端口，当port1端口上接收到来自客户端的主动连接之后，将主动连接ip:port2，并且负责port1端口和ip:port2之间的数据转发。
    def port2host(self):
        try:
            self.l_socket.bind((self.laddr, self.lport))
            self.l_socket.listen(1)
        except Exception as reason:
            print("Create Listen Port Failed!")
            exit(0)
        self.rlist = [self.l_socket]
        self.wlist = []
        self.elist = []
        tube = []
        while True:
            rs, ws, es = select.select(self.rlist, self.wlist, self.elist)
            for sockfd in rs:
                if sockfd == self.l_socket:
                    self.l_connected, addr = sockfd.accept()
                    self.rlist.append(self.l_connected)
                    print("[√] Local connected:laddr={},raddr={}".format(self.l_connected.getsockname(),
                                                                         self.l_connected.getpeername()))
                    try:
                        self.r_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        self.r_socket.connect((self.raddr, self.rport))
                    except Exception as reason:
                        print("Connect Source Port Failed!")
                        exit(0)
                    self.rlist.append(self.r_socket)
                    print("[√] Remote connected:laddr={},raddr={}".format(self.r_socket.getsockname(),
                                                                          self.r_socket.getpeername()))
                    tube.append((self.l_connected, self.r_socket))
                    continue
                else:
                    for tb in tube:
                        if sockfd in tb:
                            r_i = tb.index(sockfd)
                            w_i = 0 if r_i == 1 else 1
                            rr = self.copy(sockfd, tb[w_i])
                            if rr < 0:
                                self.rlist.remove(tb[0])
                                self.rlist.remove(tb[1])
                                tube.remove(tb)
                                print("[x] connect close:laddr={},raddr={}".
                                      format(tb[0].getsockname(), tb[0].getpeername()))
                                tb[0].close()

                                print("[x] connect close:laddr={},raddr={}".
                                      format(tb[1].getsockname(), tb[1].getpeername()))
                                tb[1].close()

    # -slave
    # 本地开始主动连接ip1:port1主机和ip2:port2主机，当连接成功之后，负责这两个主机之间的数据转发。
    def host2host(self):
        try:
            self.l_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.l_socket.connect((self.laddr, self.lport))
            self.r_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.r_socket.connect((self.raddr, self.rport))
        except Exception as reason:
            print("Connect Source Port Failed!")
            exit(0)
        self.rlist = [self.l_socket, self.r_socket]
        self.wlist = []
        self.elist = [self.l_socket, self.r_socket]
        loop_w = True
        while loop_w:
            rs, ws, es = select.select(self.rlist, self.wlist, self.elist)
            for sockfd in rs:
                for i, v in enumerate(self.rlist):
                    ret = 0
                    rev = None
                    if sockfd == v and i % 2 == 0:
                        rev = self.rlist[i + 1]
                        ret = self.copy(sockfd, rev)
                    elif sockfd == v and i % 2 == 1:
                        rev = self.rlist[i - 1]
                        ret = self.copy(sockfd, rev)
                    if ret < 0:
                        self.rlist.remove(sockfd)
                        self.rlist.remove(rev)
                        print("[x] connect close:laddr={},raddr={}".
                              format(sockfd.getsockname(), sockfd.getpeername()))
                        sockfd.close()

                        print("[x] connect close:laddr={},raddr={}".
                              format(rev.getsockname(), rev.getpeername()))
                        rev.close()
                        loop_w = False
                        break
        self.host2host()

    # -listen
    # 同时监听port1端口和port2端口，当两个客户端主动连接上这两个监听端口之后，负责这两个端口间的数据转发。
    def port2port(self):
        try:
            self.l_socket.bind((self.laddr, self.lport))
            self.l_socket.listen(1)

            self.r_socket.bind((self.raddr, self.rport))
            self.r_socket.listen(1)
        except Exception as reason:
            print("Create Listen Port Failed!")
            exit(0)
        self.rlist = [self.l_socket, self.r_socket]
        self.wlist = []
        self.elist = []
        while True:
            rs, ws, es = select.select(self.rlist, self.wlist, self.elist)
            for sockfd in rs:
                if sockfd == self.l_socket:
                    self.l_connected, addr = sockfd.accept()
                    self.rlist.append(self.l_connected)
                    continue
                elif sockfd == self.r_socket:
                    self.r_connected, addr = sockfd.accept()
                    self.rlist.append(self.r_connected)
                    continue
                else:
                    tube = self.rlist[2:]
                    if len(tube) < 2 or len(tube) % 2 == 1:
                        continue
                    for i, v in enumerate(tube):
                        ret = 0
                        rev = None
                        if sockfd == v and i % 2 == 0:
                            rev = tube[i + 1]
                            ret = self.copy(sockfd, rev)
                        elif sockfd == v and i % 2 == 1:
                            rev = tube[i - 1]
                            ret = self.copy(sockfd, rev)
                        if ret < 0:
                            self.rlist.remove(sockfd)
                            self.rlist.remove(rev)
                            print("[x] connect close:laddr={},raddr={}".
                                  format(sockfd.getsockname(), sockfd.getpeername()))
                            sockfd.close()

                            print("[x] connect close:laddr={},raddr={}".
                                  format(rev.getsockname(), rev.getpeername()))
                            rev.close()

    def copy(self, reader, writer):
        data = reader.recv(self.DATA_BLOCK)
        if len(data) <= 0:
            return -1
        w = writer.send(data)
        if w <= 0:
            return -2
        print("[->] tran [{}] : from {} to {} ".format(len(data), reader.getsockname(), writer.getsockname()))
        return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('type', help="[listen] [slave] [tran] [l] [s] [t]")
    parser.add_argument('-l', '--laddr', dest='laddr', default='0.0.0.0', help="IP eg: 0.0.0.0")
    parser.add_argument("-p", "--lport", dest="lport", help="Port eg: 3306")
    parser.add_argument('-R', '--raddr', dest='raddr', default='0.0.0.0', help="IP eg: 0.0.0.0")
    parser.add_argument("-P", "--rport", dest="rport", help="Port eg: 3306")
    options = parser.parse_args()
    pt = Portube(options.laddr, int(options.lport), options.raddr, int(options.rport))
    if options.type in ("listen", "l"):
        pt.port2port()
    elif options.type in ("slave", "s"):
        pt.host2host()
    elif options.type in ("tran", "t"):
        pt.port2host()


if __name__ == "__main__":
    main()
