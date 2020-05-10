from multiprocessing import cpu_count


max_requests = 1000
worker_class = 'gevent'
worker_connections = 1000
timeout = 300
keepalive = 2
workers = cpu_count() * 2 + 1
threads = cpu_count()
bind = "0.0.0.0:80"
