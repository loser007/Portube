# Portube
软件实现的端口转发，透明代理，在主机限制入站规则但不限制出站规则的特定情况下可绕过防火墙

# 安装
```json
pip install portube
```

# 用法
```
portube [t|s|l] -l addr1 -p port1 -R addr2 -P port2
```
## -tran模式
>本地开始监听port1端口，当port1端口上接收到来自客户端的主动连接之后，将主动连接ip:port2，并且负责port1端口和ip:port2之间的数据转发。 
```
portube t  -p 3307 -R 127.0.0.1 -P 3306
portube tran  -p 3307 -R 127.0.0.1 -P 3306
```
## -listen模式
>同时监听port1端口和port2端口，当两个客户端主动连接上这两个监听端口之后，负责这两个端口间的数据转发。
```
portube l -p 9917 -P 9907
portube listen -p 9917 -P 9907
```

## -slave模式
>本地开始主动连接ip1:port1主机和ip2:port2主机，当连接成功之后，负责这两个主机之间的数据转发，不支持短连接和长连接同时存在。 
```
portube s -l 127.0.0.1 -p 3307 -R 127.0.0.1 -P 9907
portube slave  -l 127.0.0.1 -p 3307 -R 127.0.0.1 -P 9907
```