from ReverseProxy import ReverseProxy

proxy = ReverseProxy("192.168.1.5", 8080, "www.mako.co.il", 443)
proxy.start_proxy()