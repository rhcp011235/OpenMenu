# whoever came here to read this, shu shu
import logging
import os
import json
import requests
import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse, Response, JSONResponse
from pydantic import BaseModel

app = FastAPI()
logger = logging.getLogger("uvicorn")
logging.basicConfig(level=logging.CRITICAL + 1)


class Item(BaseModel):
  data: dict


@app.get("/")
async def get_html():
  return HTMLResponse('<pre>t.me/rhcp011235</pre>')


@app.get("/favicon.ico")
def get_favicon():
  return FileResponse("favicon.ico")


@app.post("/json")
async def receive_json(item: Item):
  data = item.data
  print("Received JSON data:")
  print(data)
  # This is where the actual OpenMenu removeal API is. 
  API_ENDPOINT = ''
  datastring = f"?pet={data.get('KEY')}&ID={data.get('ID')}&KEY={data.get('KEY')}&UDID={data.get('UDID')}&SN={data.get('SN')}"
  print("generated url", API_ENDPOINT + datastring)
  useragent = {
      "User-agent":
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
  }
  r = requests.get(url=API_ENDPOINT + datastring,
                   headers=useragent,
                   timeout=300)
  jsonresp = json.loads(r.content.decode('utf-8'))
  code = jsonresp.get("code")
  msg = jsonresp.get("msg")
  if str(code) == "0" or 'Success' in msg:
    return JSONResponse(content={"success": "true"}, status_code=200)
  elif str(code) == "-1" or 'Success' not in msg:
    return JSONResponse(content={"success": "false"}, status_code=401)
  else:
    return JSONResponse(content={"success": "false"}, status_code=888)


if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=443)