import random
import sys
import threading
import time

import webview

html = """
<!DOCTYPE html>
<html>
<head lang="en">
<meta charset="UTF-8">

<style>
    #response-container {
        display: none;
        padding: 1rem;
        margin: 3rem 5%;
        font-size: 120%;
        border: 5px dashed #ccc;
        word-wrap: break-word;
    }

    label {
        margin-left: 0.3rem;
        margin-right: 0.3rem;
    }

    button {
        font-size: 100%;
        padding: 0.5rem;
        margin: 0.3rem;
        text-transform: uppercase;
    }
</style>
</head>
<body>

<h1>JS 接口 示例</h1>
<p id='pywebview-status'><i>pywebview</i> 未就绪</p>

<button onClick="initialize()">你好 Python</button><br/>
<button id="heavy-stuff-btn" onClick="doHeavyStuff()">执行繁重操作</button><br/>
<button onClick="getRandomNumber()">获取随机数</button><br/>
<label for="name_input">向谁问好:</label><input id="name_input" placeholder="输入一个名字">
<button onClick="greet()">打招呼</button><br/>
<button onClick="catchException()">捕捉异常</button><br/>

<div id="response-container"></div>
<script>
    window.addEventListener('pywebviewready', function() {
        var container = document.getElementById('pywebview-status')
        container.innerHTML = '<i>pywebview</i> 已就绪'
    })

    function showResponse(response) {
        var container = document.getElementById('response-container')

        container.innerText = response.message
        container.style.display = 'block'
    }

    function initialize() {
        pywebview.api.init().then(showResponse)
    }

    function doHeavyStuff() {
        var btn = document.getElementById('heavy-stuff-btn')

        pywebview.api.heavy_stuff.doHeavyStuff().then(function(response) {
            showResponse(response)
            btn.onclick = doHeavyStuff
            btn.innerText = '执行繁重操作'
        })

        showResponse({message: '处理中...'})
        btn.innerText = '取消繁重操作'
        btn.onclick = cancelHeavyStuff
    }

    function cancelHeavyStuff() {
        pywebview.api.heavy_stuff.cancelHeavyStuff()
    }

    function getRandomNumber() {
        pywebview.api.getRandomNumber().then(showResponse)
    }

    function greet() {
        var name_input = document.getElementById('name_input').value;
        pywebview.api.sayHelloTo(name_input).then(showResponse)
    }

    function catchException() {
        pywebview.api.error().catch(showResponse)
    }
</script>
</body>
</html>
"""

class HeavyStuffAPI:
    def __init__(self):
        self.cancel_heavy_stuff_flag = False

    def doHeavyStuff(self):
        time.sleep(0.1)  # 睡眠一小段时间以避免 UI 线程冻结
        now = time.time()
        self.cancel_heavy_stuff_flag = False
        for i in range(0, 1000000):
            _ = i * random.randint(0, 1000)
            if self.cancel_heavy_stuff_flag:
                response = {'message': '操作已取消'}
                break
        else:
            then = time.time()
            response = {
                'message': '操作耗时 {0:.1f} 秒 在线程 {1}'.format(
                    (then - now), threading.current_thread()
                )
            }
        return response

    def cancelHeavyStuff(self):
        time.sleep(0.1)
        self.cancel_heavy_stuff_flag = True

class NotExposedApi:
    def notExposedMethod(self):
        return '此方法未暴露'

class Api:
    heavy_stuff = HeavyStuffAPI()
    _this_wont_be_exposed = NotExposedApi()

    def init(self):
        response = {'message': '你好从 Python {0}'.format(sys.version)}
        return response

    def getRandomNumber(self):
        time.sleep(3)
        response = {
            'message': '这是一个随机数 courtesy of randint: {0}'.format(
                random.randint(0, 100000000)
            )
        }
        return response

    def sayHelloTo(self, name):
        response = {'message': '你好 {0}!'.format(name)}
        return response

    def error(self):
        raise Exception('这是一个 Python 异常')

if __name__ == '__main__':
    api = Api()
    window = webview.create_window('JS 接口 示例', html=html, js_api=api)
    webview.start()