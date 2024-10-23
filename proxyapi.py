# This is the API part of the proxy which will let you only allow certain users to use the proxy
# Registers SN

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class DataItem(BaseModel):
    key: str
    udid: str
    sn: str

def save_sn_to_file(udid: str, sn: str):
    fpath = 'dumps/'
    filename = udid + 'SN'
    with open(fpath+filename, 'w') as file:
        file.write(sn)

@app.post("/register/")
async def save_sn(data: DataItem):
    correct_key = 'gingergurlwashere'
    if data.key == correct_key:
        save_sn_to_file(data.udid, data.sn)
        return {"message": "SN registered successfully"}
    else:
        raise HTTPException(status_code=401, detail="Invalid key")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=800)