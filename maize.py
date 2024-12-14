import asyncio
import websockets
import json

# 接続中のクライアントを追跡
connected_clients = set()

async def handler(websocket, path):
    # クライアントを登録
    connected_clients.add(websocket)
    print(f"Client connected: {websocket.remote_address}")

    try:
        async for message in websocket:
            # Unityからの位置情報を受信
            print(f"Received message: {message}")

            # 受け取ったデータをブロードキャスト
            await broadcast(message)
    except websockets.exceptions.ConnectionClosed:
        print(f"Client disconnected: {websocket.remote_address}")
    finally:
        # クライアントを解除
        connected_clients.remove(websocket)

async def broadcast(message):
    # 全ての接続中クライアントにメッセージを送信
    if connected_clients:
        await asyncio.wait([client.send(message) for client in connected_clients])

# サーバーの起動設定
async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("WebSocket server started on ws://localhost:8765")
        await asyncio.Future()  # 無限ループを維持

if __name__ == "__main__":
    asyncio.run(main())