import asyncio
import websockets
import json

# WebSocketハンドラ関数
async def handler(websocket, path):
    print(f"Client connected to path: {path}")
    try:
        async for message in websocket:
            data = json.loads(message)
            player_id = data.get("player_id", "unknown")
            position = data.get("position", {})
            x, y, z = position.get("x", 0), position.get("y", 0), position.get("z", 0)
            print(f"Received from {player_id}: Position x={x}, y={y}, z={z}")
            
            # 応答メッセージ（確認用）
            await websocket.send(f"Received position of {player_id}: x={x}, y={y}, z={z}")
    except websockets.exceptions.ConnectionClosed as e:
        print("Client disconnected")
    except Exception as e:
        print(f"Error: {e}")

# サーバーをポート8765で起動
async def main():
    # `handler`関数を指定してWebSocketサーバーを起動
    async with websockets.serve(handler, "localhost", 8765):
        print("WebSocket Server Started on ws://localhost:8765")
        await asyncio.Future()  # 無限ループ

asyncio.run(main())