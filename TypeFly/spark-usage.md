# Spark Usage on Windows/WSL
In Windows, connect to regular WiFi on one adapter and the drone's on the second. Then, boot up the DJI Control Server on the phone.

Figure out the IP address of the drone, i.e.:
```powershell
> # Windows; you may need to do --interface after the following curl command if Windows doesn't automatically pick up on it, i.e.:
> # curl http://192.168.1.20:8080/ --interface 192.168.1.21
> # Try combinations of *.20/*.21/*.22
> curl http://192.168.1.20:8080/
Connected
>
```
Now, figure out the IP address of your WSL machine:
```shell
> # Within WSL
> ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet 10.255.255.254/32 brd 10.255.255.254 scope global lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether 00:15:5d:71:1e:2a brd ff:ff:ff:ff:ff:ff
    inet 172.26.255.87/20 brd 172.26.255.255 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::215:5dff:fe71:1e2a/64 scope link
       valid_lft forever preferred_lft forever
```
Now that you know the drone is at `http://192.168.1.20:8080`, and WSL's virtual adapter is at `172.26.255.87`, enable passthrough so WSL can access the drone:
```powershell
> # Windows
> sudo netsh interface portproxy add v4tov4 listenport=8080 listenaddress=192.168.1.20 connectport=8080 connectaddress=172.26.255.87
```
Finally, in WSL, set all environment variables and run both services:
```shell
> # WSL
> make SERVICE=yolo build
> VISION_SERVICE_IP=172.26.255.87:50050 OPENAI_API_KEY=API_KEY make typefly INTERFACE=172.26.255.87 URL=http://192.168.1.20:8080
```