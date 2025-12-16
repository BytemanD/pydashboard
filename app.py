from gevent import monkey

# monkey.patch_all()


from gevent.pywsgi import WSGIServer
import flask
from loguru import logger
import quart


# APP = quart.Quart(__name__)
APP = flask.Flask(__name__)


class Manaeger:

    def cpu_task(self):
        logger.info("cpu task start")
        result = 1
        for i in range(8000):
            a = i**i
        logger.info("cpu task end")
        return result


from concurrent.futures import ProcessPoolExecutor, as_completed


executor = ProcessPoolExecutor(max_workers=10)
# loop = asyncio.get_event_loop()

MANAGER = Manaeger()


# @APP.before_request
# def before_request():
#     logger.info("Recive {}", flask.request.path)


@APP.route("/demo")
def demo():
    # result = as_completed([executor.submit(MANAGER.cpu_task)])
    # return quart.jsonify({"result": next(result).result()})
    # await asyncio.sleep(0.1)
    result = MANAGER.cpu_task()
    # result = 1
    logger.info("result: {}", result)
    return flask.jsonify({"result": result})


def create_shared_socket(port=8000):
    """Windows 下创建可共享的套接字"""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Windows 特定选项
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 0)
    sock.bind(('0.0.0.0', port))
    sock.listen(100)
    return sock

# def main():
    
#     APP.run(port=8000, host="0.0.0.0")
#     # sock = create_shared_socket()
#     # s = WSGIServer(sock, APP)
#     # s.serve_forever()
    

# if __name__ == "__main__":
#     main()
