import sanic
import ffmpeg
import requests
import requests
import time
from urllib.parse import urlparse, parse_qs


cookies = {}

headers = {}

params = {}

json_data = {}

def func(video_url):
    parsed_url = urlparse(video_url)

    # 获取查询参数
    query_params = parse_qs(parsed_url.query)

    # 输出查询参数
    print("查询参数:")
    for param, values in query_params.items():
        print(f"{param}: {', '.join(values)}")
    probe = ffmpeg.probe(video_url)
    duration = probe['format']['duration']

    # 更新参数
    json_data.update({
        "latestTime": round(float(duration)),
        "courseId": query_params["courseid"][0],
        "courseWareId": query_params['coursewareId'][0],
    })

    response = requests.post(
        'https://elearning.tcsasac.com/learn/app/clientapi/course/progress/reportLearnProgress.do',
        params=params,
        cookies=cookies,
        headers=headers,
        json=json_data,
        verify=False,
        proxies={"http":None, "https":None}
    )
    print(response.text)



from sanic import Sanic
from sanic.response import text
import sanic
app = Sanic("hello")
from sanic_cors import CORS
CORS(app)
@app.post("/")
async def hello_world(request: sanic.Request):
    data = request.json
    video_url = data.get('url')
    func(video_url)
    return text("ok")

# must write `name == main`
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000, debug=True)