#[中文文档]()
# Portube
Software-implemented port forwarding, transparent proxy, bypassing the firewall in certain cases where the host restricts inbound rules but does not limit outbound rules

# installation
```json
pip install portube
```

# usage
```
portube [t|s|l] -l addr1 -p port1 -R addr2 -P port2
```
## tran mode
>The local port starts listening to the port1 port. When the port1 port receives the active connection from the client, it will actively connect to ip:port2 and be responsible for data forwarding between the port1 port and ip:port2.
```
portube t  -p 3307 -R 127.0.0.1 -P 3306
portube tran  -p 3307 -R 127.0.0.1 -P 3306
```
## listen mode
>At the same time, the port1 port and port2 port are monitored. When the two clients actively connect to the two listening ports,and they are responsible for data forwarding between the two ports.
```
portube l -p 9917 -P 9907
portube listen -p 9917 -P 9907
```

## slave mode
>Locally, the ip1:port1 host and the ip2:port2 host are actively connected. After the connection is successful, the data is forwarded between the two hosts. Short and long connections are not supported. 
```
portube s -l 127.0.0.1 -p 3307 -R 127.0.0.1 -P 9907
portube slave  -l 127.0.0.1 -p 3307 -R 127.0.0.1 -P 9907
```