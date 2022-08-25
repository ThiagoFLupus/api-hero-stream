from flask import Flask, stream_with_context
from flask import request, Response, json
from flask import jsonify
from datetime import datetime, timedelta
import time
import os
import re

app = Flask(__name__)

# array hero objects
heroes = [
    {'id': 1, 'name': 'Batman'},
    {'id': 2, 'name': 'Green Lantern'},
    {'id': 3, 'name': 'Wonder Woman'},
    {'id': 4, 'name': 'Green Arrow'},
    {'id': 5, 'name': 'Super Girl'},
    {'id': 6, 'name': 'Cyborg'},
    {'id': 7, 'name': 'Nightwing'},
]

headers = {
    'Content-Type': 'application/json',
}

@app.route('/api', methods=['GET'])
def index():
    return "server is running on port 5100..."

@app.route("/api/heroes", methods=['GET'])
def getHeroes():
    statusResponse = '200'
    dataResponse = {
        'message': 'success',
        'data': heroes
    }
    return json.dumps(dataResponse), statusResponse, headers

@app.route('/api/create-hero', methods=['POST'])
def createHero():
    statusResponse = '200'
    dataResponse = {
        'message': 'success'
    }
    if not request.data:
        statusResponse = 400
        dataResponse = {
            'message': 'bad request',
            'error': ['Attribrutes are required']
        }
        return json.dumps(dataResponse), statusResponse, {'content-type': 'application/json'}
    else:
        lastElement = heroes[-1]
        dataRequest = request.json
        newElement = {'id': lastElement['id'] + 1, 'name': dataRequest['name']}
        heroes.append(newElement)
        dataResponse = {
            'message': 'success',
            'data': heroes
        }
    return json.dumps(dataResponse), statusResponse, headers

@app.route('/api/update-hero', methods=['PUT'])
def updateHero():
    statusResponse = '200'
    dataResponse = {
        'message': 'success'
    }
    if not request.data:
        statusResponse = 400
        dataResponse = {
            'message': 'bad request',
            'error': ['Attribrutes are required']
        }
        return json.dumps(dataResponse), statusResponse, {'content-type': 'application/json'}
    else:
        lst = heroes
        dataRequest = request.json
        index = next((i for i, x in enumerate(lst) if x["id"] == dataRequest['hero']['id']), None)
        if index:
            updatedElement = {'id': dataRequest['hero']['id'], 'name': dataRequest['hero']['name']}
            heroes[index] = updatedElement
            dataResponse = {
                'message': 'success',
                'data': heroes
            }
        else: 
            statusResponse = 403
            dataResponse = {
                'message': 'Nenhum registro encontrado',
                'data': heroes
            }
        
    return json.dumps(dataResponse), statusResponse, headers

# rota para autenticação
@app.route('/api/auth', methods=['POST'])
def auth():
    statusResponse = '200'
    dataResponse = {
        'message': 'success'
    }
    time.sleep(1)
    if not request.data:
        statusResponse = 400
        dataResponse = {
            'message': 'bad request',
            'error': ['Attribrutes are required']
        }
        return json.dumps(dataResponse), statusResponse, headers
    else:
        emailCheck = 'test@test.com'
        passwordCheck = '12345'
        dataRequest = request.json
        if dataRequest['email'] == emailCheck and dataRequest['password'] == passwordCheck:
            # generating token
            actualTime = datetime.utcnow()
            actualTimeToToken = actualTime + timedelta(minutes=1)
            dataToken = {
                'token': 'FKFJ446FdffgsKG9080990FDG09F8G0904',
                'exp': actualTimeToToken.strftime("%Y/%m/%d %H:%M:%S")
            }
            
            dataResponse = {
                'message': 'success',
                'data': dataToken
            }
        else:
            dataResponse = {
                'message': 'E-mail ou senha incorretos'
            }
        
    return json.dumps(dataResponse), statusResponse, headers

# rota para checagem de autenticação
@app.route('/api/update-auth', methods=['POST'])
def updateAuth():
    statusResponse = '200'
    dataResponse = {
        'message': 'success'
    }
    if not request.data:
        statusResponse = 400
        dataResponse = {
            'message': 'bad request',
            'error': ['Attribrutes are required']
        }
        return json.dumps(dataResponse), statusResponse, headers
    else:
        dataRequest = request.json
        # checking token
        actualTime = datetime.utcnow()
        timeToken = datetime.strptime(dataRequest['exp'], "%Y/%m/%d %H:%M:%S")
        diferentTime = actualTime - timeToken
        if dataRequest['token'] == 'FKFJ446FdffgsKG9080990FDG09F8G0904' and ((diferentTime.total_seconds() / 60) < 1):
            actualTime = datetime.utcnow()
            actualTimeToToken = actualTime + timedelta(minutes=30)
            dataToken = {
                'token': 'FKFJ446FdffgsKG9080990FDG09F8G0904',
                'exp': actualTimeToToken.strftime("%Y/%m/%d %H:%M:%S")
            }
            dataResponse = {
                'message': 'success',
                'data': dataToken
            }
        else:
            statusResponse = 401
            
            dataResponse = {
                'message': 'Token expirado'
            }
        
    return json.dumps(dataResponse), statusResponse, headers

@app.route('/api/video/<id>', methods=['GET'])
def getVideo(id):
    statusResponse = '200'
    dataResponse = {
        'message': 'success'
    }
    headersVideo = {

    }
    if id:
        def read_file_chunks(path, startRange, endRange):
            with open(path, 'rb') as fd:
                while 1:                   
                    fd.seek(startRange)
                    buf = fd.read()
                    if buf:
                        yield buf
                    else:
                        break

        def serve_video(id):
            fp = './files/video3.mp4'
            rangeHeader = request.headers.get('range')

            if id == '1' or id == '7' or id == '11' or id == '13':
                fp = "./files/video.mp4"
            elif id == '0' or id == '3' or id == '9' or id == '12':
                fp = "./files/video2.mp4"

            print("************")
            print(id)
            print(fp)

            if rangeHeader:
                sizeVideo = os.stat(fp).st_size
                CHUNK_SIZE = 10 ** 6
                start = int(re.sub(r'[^0-9]', '', rangeHeader))
                end = min(start + CHUNK_SIZE, sizeVideo - 1)
                contentLength = end - start + 1
                return Response(
                    response=stream_with_context(read_file_chunks(fp, start, end)),
                    status=206,
                    headers={
                        # 'Content-Disposition': f'attachment; filename={name}',
                        # 'Content-Type': 'Blob',
                        'Content-Range': 'bytes {}-{}/{}'.format(start, end, sizeVideo),
                        'Accept-Ranges': 'bytes',
                        'Content-Length': contentLength,
                        'Content-Type': 'video/mp4',
                    },
                    mimetype='video/mp4'
                )
            else:
                raise 'not found'

        return serve_video(id)
    else:
        statusResponse = 400
            
        dataResponse = {
            'message': 'Bad request'
        }

    return json.dumps(dataResponse), statusResponse, headersVideo


if __name__ == "__main__":
    print('Inicializando servidor na porta 5100...')
    app.run(host="0.0.0.0", debug=True)
else:
    print('Erro na inicialização do servidor!')