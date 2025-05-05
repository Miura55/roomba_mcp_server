import os
from fastapi import FastAPI, HTTPException
from fastapi_mcp import FastApiMCP
from schemes import MoveCommand
from utils.mqtt_client import MQTTClient
from utils.roomba_controller import RoombaController
from contextlib import asynccontextmanager

mqtt_endpoint = os.getenv("MQTT_ENDPOINT", "localhost")
mqtt_port = int(os.getenv("MQTT_PORT", 1883))
# MQTTクライアントのインスタンスを作成
mqtt_client = MQTTClient(mqtt_endpoint, mqtt_port)

# Roombaコントローラーのインスタンスを作成
roomba_controller = RoombaController(mqtt_client)

# MQTTブローカーに接続
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        if not mqtt_client.connect():
            raise Exception("MQTTブローカーへの接続に失敗しました")
        yield
    finally:
        mqtt_client.disconnect()

# FastAPIアプリケーションの初期化
app = FastAPI(title="Roomba MCP API", description="MQTTを使用してRoombaを操作するためのAPI", lifespan=lifespan)

# エンドポイント定義
@app.post("/move", summary="Roombaを移動させる" , operation_id="move_roomba")
async def move_roomba(command: MoveCommand):
    try:
        roomba_controller.move(command)

        response = {
            "status": "success",
            "message": f"Roomba movement command sent: velocity {command.velocity}, yaw_rate {command.yaw_rate}"
        }
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Roomba制御エラー: {str(e)}")


@app.post("/home", summary="Roombaをホームに戻す", operation_id="home_roomba")
async def home_roomba():
    try:
        roomba_controller.home()
        return {
            "status": "success",
            "message": "Roomba home command sent"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Roombaホームコマンドエラー: {str(e)}")

mcp = FastApiMCP(
    app,
    name="Roomba MCP API",
    description="MQTTを使用してRoombaを操作するためのAPI",
)
mcp.mount()

def main():
    import uvicorn
    print("Roomba MCP API サーバーを起動しています...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main()
