import socket
import sys

def start_server(ip, port, accounts, session_timeout, root_dir):
    ip = sys.argv[1]
    port = int(sys.argv[2])
    accounts = sys.argv[3]
    session_timeout = int(sys.argv[4])
    root_dir = sys.argv[5]

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((ip, port))
    sock.listen()

    while True:
        conn, addr = sock.accept()
        with conn:
            request = conn.recv(1024).decode()
            http_method = request.split(" ")[0]
            request_target = request.split(" ")[1]
            http_version = "HTTP/1.0"

            if http_method == "POST" and request_target == "/":
                status, headers, body = post(request, accounts)
                message = http_version + " " + status + "\r\n" + headers + "\r\n\r\n" + body
                conn.sendall(message.encode())
            elif http_method == "GET":
                status, body = get_request(request, session_timeout, root_dir, request_target)
                if (len(body) == 0):
                    message = f"{http_version} {status}\r\n\r\n"
                else:
                    message = f"{http_version} {status}\r\n\r\n{body}"
                conn.sendall(message.encode())
            else:
                message = f"{http_version} 501 Not Implemented\r\n\r\n"
                conn.sendall(message.encode())

        conn.close()

def main():
    start_server(sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), sys.argv[5])

main()



print("AVERAGE LATENCY: <float>")
print("PERCENTILES: <float-25%> , <float-50%>, <float-75%>, <float-95%>, <float-99%>")
