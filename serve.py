from __future__ import print_function
import sys

if sys.version_info[0] > 2:
  import http.server as SimpleHTTPServer
  import socketserver as SocketServer
else:
  import SimpleHTTPServer
  import SocketServer

import threading
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from subprocess import check_output, CalledProcessError, STDOUT
import json
import timeit
import webbrowser
from io import BytesIO

PORT = 7637
PYTHON_COMMAND = "python"

html = u"""
<!doctype html>
<html lang='en'>
  <head>
    <meta charset='utf-8'>
    <meta http-equiv='x-ua-compatible' content='ie=edge'>
    <title>RPM Testing Environment</title>
    <meta name='description' content=''>
    <meta name='viewport' content='width=device-width, initial-scale=1, shrink-to-fit=no'>
    <link rel='shortcut icon' href='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAQAAADZc7J/AAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAAmJLR0QA/4ePzL8AAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAAAHdElNRQfiARgLJxGDtTufAAABh0lEQVRIx+2VPUsDQRCGnxMjMYaQIiIp7CIEwYiVgoWNiB91Km1Ef4CFrWhhZWMj+BNUsLCysBFENBfBIIKKCMHCj0IEEyxMlLG447KX3N4ZbCy8t9iduZl3Z3Zm7gzhd0/LL/3/AEGrl9JIkiVDhjRF8piYcqllkDoQYpFSgzrPpOCFerGTC0SDHGMBBMQpaN0tbNCmJSDKqYfLDkuc8+nIWxoCIhxqTl0QCDPAlS1vM1GLo3b6kTbsD1YZZYWKonugWyEgxklA7o0oEHGnEOe5SYopQZROXKOrySZMKp1oDDMf6PBKjrIjjfOldCJ7AeG+MIfhKt+glYIlJKjyhKl1L9One2XdQYpjerjVjst0wDCRokPgTHPIsl9u6rbkafFOzI/AKaMRIuwZ4q6U/ErjEEiVa0+LA//aqp+0gr2WXRY3Pycw7XWWR0Vb9CdQL7GdewQhyRBvjjrq32FuIYsgJAR6ubOV4SYIBDYR+u3pXKeCEGqKQGCGEWefZt89AY0w/v+NfAO8YO2MKZFBGgAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAxOC0wMS0yNFQxMTozOToxNyswMTowMIAKCZoAAAAldEVYdGRhdGU6bW9kaWZ5ADIwMTgtMDEtMjRUMTE6Mzk6MTcrMDE6MDDxV7EmAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAAFd6VFh0UmF3IHByb2ZpbGUgdHlwZSBpcHRjAAB4nOPyDAhxVigoyk/LzEnlUgADIwsuYwsTIxNLkxQDEyBEgDTDZAMjs1Qgy9jUyMTMxBzEB8uASKBKLgDqFxF08kI1lQAAAABJRU5ErkJggg=='>
    <link rel='stylesheet' href='https://atomiks.github.io/tippyjs/tippy/themes.css'>
    <style>
      body {
        background: #6190e8;
        background: -webkit-linear-gradient(to right, #6190e8, #a7bfe8);
        background: linear-gradient(to right, #6190e8, #a7bfe8);
        font-family: -apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica Neue,Ubuntu,Arial,sans-serif;
        margin: 3rem;
      }

      .main {
        background-color: #fff;
        border-radius: 4px;
        box-shadow: 0 2px 8px rgba(0,0,0,.33);
        display: flex;
      }

      .left {
        border-right: 1px solid #dfdfdf;
        width: 60%;
        padding: 1rem 2rem 3rem;
      }

      .right {
        font-family: Consolas;
        padding: 1rem;
        width: 40%;
      }

      .right pre {
        color: #262A35;
        padding: 0 1rem;
        font-family: Consolas;
        font-size: 15px;
        line-height: 150%;
        white-space: pre-wrap;
        overflow-x: scroll;
      }

      table {
        width: 100%;
        border-top: 1px solid #f0f0f0;
        margin-top: 0.5rem;
        padding-top: 0.5rem;
      }

      p {
        padding: 0 1rem;
        font-size: 14px;
        color: #9897A8;
      }

      p span {
        font-size: 12px;
        color: #C2C1D7;
        padding-left: 0.3rem;
      }

      th {
        font-weight: 500;
      }

      th, td {
        color: #262A35;
        padding: 0.5rem 1rem;
        font-size: 14px;
        text-align: left;
      }

      .summary {
        display: flex;
        align-items: center;
        justify-content: space-between;
      }

      .progress {
        background: #f0f0f0;
        width: 55%;
        height: 10px;
        border-radius: 10px;
        display: flex;
        margin-right: 0.5rem;
      }

      .bar {
        width: 100%;
        display: block;
        border-radius: 10px;
        background: linear-gradient(to right, #FFE883, #7BEFE3);
      }

      .correct {
        color: #78BF2E;
      }

      .skipped {
        color: #F0CE3E;
      }

      .incorrect {
        color: #FD6669;
      }

      .skip {
        color: #C2C1D7;
      }

      a, a:hover, a:visited {
        color: #6696F5;
        text-decoration: none;
        padding-bottom: 0.1rem;
        border-bottom: dashed 1px #6A9DFF;
      }

      a:hover {
        color: #8FB2FF;
      }

      footer {
        text-align: center;
        margin-top: 3rem;
        font-size: 12px;
        font-weight: 100;
        color: #B8D0E8;
      }

      .loading {
        opacity: 0.3;
      }

      .loading-message {
        color: #000;
      }

      hr {
        margin: 0 auto;
        background: #eee;
        width: calc(100% - 2rem);
        border: none;
        border-top: 1px solid #f0f0f0;
      }

      .tippy-popper .tippy-tooltip.light-theme {
        color:#26323d;
        box-shadow: 0 2px 16px rgba(0,0,0,.13);
      }

      .image-preview {
        cursor: pointer;
        padding-bottom: 0.1rem;
        border-bottom: dashed 1px #aaa;
      }

      .skip > .image-preview {
        border-bottom: none;
        cursor: default;
      }

      .image-preview img {
        display: none;
      }

      .tippy-tooltip img {
        width: 80px;
      }
    </style>
  </head>
  <body>
    <div class='main'>
      <div class='left'>
        <progress-bar></progress-bar>

        <div>
          <results-table></results-table>
        </div>
      </div>
      <div class='right'>
        <script-output></script-output>
      </div>
    </div>
    <footer>
      &copy; 2018 Alex Peattie
    </footer>

    <script type='riot/tag'>
      <results-table>
        <table class={ loading: loading }>
          <tr>
            <th>Problem</th>
            <th>Agent's Answer</th>
            <th>Correct Answer</th>
            <th>Correct?</th>
          </tr>
          <tr each={ items }>
            <td><a href={ problemUrl(problemName) } target='_blank'>{ problemName }</a></td>
            <td class={ skip: agentAnswer < 0 }>
              <span class='image-preview'>
                { agentAnswer }
                <img src={ problemUrl(problemName, agentAnswer) }>
              </span>
            </td>
            <td>
              <span class='image-preview'>
                { correctAnswer }
                <img src={ problemUrl(problemName, correctAnswer) }>
              </span>
            </td>
            <td class={ (correctness || '').toLowerCase() }>{ correctness }</td>
          </tr>
        </table>

        var self = this
        self.items = []
        self.loading = false

        problemUrl(problemName, number) {
          if(number < 1 || number > 8) return ''

          return ['/Problems', problemName.split('-')[0].replace('Problem', 'Problems'), problemName, (number || problemName) + '.PNG'].join('/')
        }

        riot.store.on('fetchCsv', function(items) {
          self.items  = items
          self.loading = false
          self.update()
        })

        riot.store.on('loading', function() {
          self.loading = true
          self.update()
        })

        self.on('updated', function() {
          tippy(':not(.skip) > .image-preview', { arrow: true, theme: 'light', html: el => el.querySelector('img') })
        })
      </results-table>

      <progress-bar>
        <div class='summary' if={ items.length }>
          <p>{ items.filter(isCorrect).length } of { items.length } correct <span>({ items.filter(isSkipped).length } skipped, { items.filter(isIncorrect).length } incorrect)</span></p>
          <div class='progress'>
            <span class='bar' style={ barStyle() }></span>
          </div>
        </div>

        isSkipped(item) {
          return item.correctness === 'Skipped'
        }

        isCorrect(item) {
          return item.correctness === 'Correct'
        }

        isIncorrect(item) {
          return item.correctness === 'Incorrect'
        }

        barStyle() {
          if(!self.items.length) return ''
          var fraction = self.items.filter(self.isCorrect).length / self.items.length
          var percent = Math.round(fraction * 100)

          var value = 'linear-gradient(to right, rgba(0, 0, 0, 1.0) 0%, rgba(0, 0, 0, 1.0) ' + percent + '%, transparent ' + percent + '.1%, transparent 100%)'
          return ['-webkit-mask-image: ' + value, 'mask-image' + value].join(';')
        }

        var self = this;
        self.items = []
        self.loading = false

        riot.store.on('fetchCsv', function(items) {
          self.items  = items
          self.update()
        })
      </progress-bar>

      <script-output>
        <p if={ !completionTime && !loading }>Ready for code changes.</p>
        <p class='loading-message' if={ loading }>Loading....</p>
        <p if={ completionTime && !loading }>
          <strong class={ incorrect: exitCode !== 0 }>
            { exitCode === 0 ? 'Completed' : 'Failed' }
          </strong> in { completionTime.toPrecision(4) } seconds
        </p>
        <p if={ completionTime && !loading }>Exited with code { exitCode }</p>

        <hr if={ output.length }>
        <pre>{ output }</pre>

        var self = this
        self.completionTime = null
        self.loading = false
        self.output = ''

        riot.store.on('loading', function() {
          self.loading = true
          self.output = ''
          self.update()
        })

        riot.store.on('completed', function(info) {
          self.loading = false
          self.completionTime = info.time
          self.exitCode = info.returncode
          self.output = info.output
          self.update()
        })
      </script-output>
    </script>
    </script>
    <script src='https://unpkg.com/tippy.js@2.0.2/dist/tippy.all.min.js'></script>
    <script src='https://cdn.jsdelivr.net/npm/riot@3.7/riot+compiler.min.js'></script>
    <script src='https://rawgit.com/mholt/PapaParse/master/papaparse.min.js'></script>
    <script>
      var Store = function(){
        riot.observable(this)
      }
      riot.store = new Store()
      riot.mount('*')

      function withHeaders(collection) {
        collection.shift()
        var keys = ['problemName', 'agentAnswer', 'correctness', 'correctAnswer']
        return collection.map(function (row) {
          return keys.reduce(function (obj, key, i) {
            obj[key] = row[i];
            return obj;
          }, {});
        });
      }

      function refetchCsv() {
        Papa.parse('http://localhost:7637/ProblemResults.csv?t=' + Date.now(), {
          download: true,
          skipEmptyLines: true,
          complete: function(results) {
            var items = withHeaders(results.data)
            riot.store.trigger('fetchCsv', items)
          }
        })
      }
      refetchCsv()

      var wsPort = parseInt(window.location.port, 10) + 1
      var socket = new WebSocket('ws://' + window.location.hostname + ':' + wsPort)
      socket.onmessage = function (event) {
        var message = JSON.parse(event.data)
        if(message.loading) {
          riot.store.trigger('loading')
        }

        if(message.completed) {
          riot.store.trigger('completed', message)

          if(message.returncode === 0) {
            refetchCsv()
          }
        }
      }
    </script>
  </body>
</html>
"""
conns = []

class SimpleStdinPub(WebSocket):
  def handleConnected(self):
    conns.append(self)

  def handleClose(self):
    conns.remove(self)

server = SimpleWebSocketServer('', PORT + 1, SimpleStdinPub)
thread = threading.Thread(target=server.serveforever)
thread.daemon = True
thread.start()

class StringBodyHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
  def send_head(self):
    if self.translate_path(self.path).endswith('/'):
      self.send_response(200)
      self.send_header("Content-type", "text/html; charset=utf-8")
      self.send_header("Content-Length", str(len(html)))
      self.end_headers()
      return BytesIO(html.encode())
    else:
      return SimpleHTTPServer.SimpleHTTPRequestHandler.send_head(self)

SocketServer.TCPServer.allow_reuse_address = True
httpd = SocketServer.TCPServer(("", PORT), StringBodyHandler)

def ensureUtf(s):
  try:
    return unicode(s)
  except:
    return str(s)

def sendWsJson(dict):
  for conn in conns:
    conn.sendMessage(ensureUtf(json.dumps(dict)))

class AgentCodeChangeHandler(PatternMatchingEventHandler):
  def on_any_event(self, event):
    print("Detected change in " + event.src_path)
    sendWsJson({ 'loading': True })

    start = timeit.default_timer()
    try:
      output = check_output([PYTHON_COMMAND, "RavensProject.py"], stderr = STDOUT)
      stop = timeit.default_timer()
      sendWsJson({ 'completed': True, 'output': output.decode('utf-8'), 'returncode': 0, 'time': stop - start })
    except CalledProcessError as e:
      stop = timeit.default_timer()
      sendWsJson({ 'completed': True, 'output': e.output.decode('utf-8'), 'returncode': e.returncode, 'time': stop - start })

observer = Observer()
try:
  thread2 = threading.Thread(target=httpd.serve_forever)
  thread2.daemon = True
  thread2.start()

  url = "http://localhost:" + str(PORT)
  print("Serving at " + url)
  webbrowser.open(url)

  ignore_patterns = ['*/.git', '*/.git/*', '*/.hg', '*/.hg/*']
  event_handler = AgentCodeChangeHandler(patterns=["*.py", "*.txt"], ignore_patterns=ignore_patterns)
  observer.schedule(event_handler, '.', recursive=True)
  observer.start()

  while True:
    time.sleep(1)
  observer.join()
finally:
  httpd.server_close()
  observer.stop()