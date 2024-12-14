import asyncio
import websockets
import uuid
import json

# 接続中のクライアントを管理する辞書
connected_clients = {}

async def handler(mywebsocket):
    # UUIDを生成してクライアントに割り当て
    client_id = str(uuid.uuid4())
    
    connected_clients[client_id] = mywebsocket
    print(f"Client connected: {client_id}")
    print(f"connected_clients[client_id]: {connected_clients[client_id]}")
    
    try:
        async for message in connected_clients[client_id]:
            # Unityからの位置情報を受信
            #print(f"Received message: {message}")
            
            #player_id = data.get("player_id")
            
            #if player_id not in connected_id_list:
            #    # listに IDを追加
            #    connected_id_list.append(player_id)
            #    print(f"connected_id_list_before_try:{connected_id_list}")
            
            #print(f"type(message)1:{type(message)}")
            # JSONをパース
            data = json.loads(message)
            #print(f"type(data)1:{type(data)}")
            # player_idと位置情報を取得
            player_id = data.get("player_id")
            x = data.get("x")
            y = data.get("y")
            z = data.get("z")
            
            rotX = data.get("rotX")
            rotY = data.get("rotY")
            rotZ = data.get("rotZ")
            rotW = data.get("rotW")
            
            
            print(f"Received from {player_id}: Position x={x}, y={y}, z={z} Rotation rotX={rotX}, rotY={rotY}, rotZ={rotZ}, rotW={rotW}")
            print(f"len(connected_clients):{len(connected_clients)}")
            
            # 応答メッセージ（確認用）
            #await websocket.send(f"Received")
            
            # 受け取ったデータをブロードキャスト
            await broadcast(message, connected_clients[client_id], player_id)
            
    except websockets.exceptions.ConnectionClosed as e:
        print("Client disconnected")
    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        # クライアントを解除
        if client_id in connected_clients:
            del connected_clients[client_id]


async def broadcast(data, mywebsocket, player_id):
    # 全ての接続中クライアントにメッセージを送信
    #if connected_clients:
    #    await asyncio.wait([client.send(message) for client in connected_clients])
    
    # 送信者以外の接続中クライアントに、送信者の位置情報を送信
    for client_ in connected_clients.values():
        if client_ != mywebsocket:
            
            print(f"Send Info of {player_id}")
            await client_.send(data)
    
    
# サーバーをポート8765で起動
async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("WebSocket Server Started on ws://localhost:8765")
        await asyncio.Future()  # 無限ループ

asyncio.run(main())