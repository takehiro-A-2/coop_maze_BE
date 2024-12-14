import asyncio
import websockets
import json

# 接続中のクライアントを追跡
connected_clients = set()
connected_id_list = []#{}

async def handler(websocket):
    print("Client connected")
    print(websocket)
    
    # クライアントを登録
    connected_clients.add(websocket)
    print(f"Client connected: {websocket.remote_address}")
    
    # JSONをパース
    #data = json.loads(websocket[0])
    
    # player_idと位置情報を取得
    #player_id = data.get("player_id")
    #connected_id_list.append(player_id)
    #print(f"connected_id_list_before_try:{connected_id_list}")

    
    
    
    try:
        async for message in websocket:
            # Unityからの位置情報を受信
            #print(f"Received message: {message}")
            
            
            # JSONをパース
            data = json.loads(message)
            player_id = data.get("player_id")
            
            if player_id not in connected_id_list:
                # listに IDを追加
                
                connected_id_list.append(player_id)
                print(f"connected_id_list_before_try:{connected_id_list}")
                

            # player_idと位置情報を取得
            #player_id = data.get("player_id")
            x = data.get("x")
            y = data.get("y")
            z = data.get("z")
            
            print(f"Received from {player_id}: Position x={x}, y={y}, z={z}")
            print(f"connected_id_list_after_try:{connected_id_list}")
            
            # 応答メッセージ（確認用）
            #await websocket.send(f"Received")
            
            # 受け取ったデータをブロードキャスト
            await broadcast(message)
            
    except websockets.exceptions.ConnectionClosed as e:
        print("Client disconnected")
    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        # クライアントを解除
        connected_clients.remove(websocket)


async def broadcast(message):
    # 全ての接続中クライアントにメッセージを送信
    #if connected_clients:
    #    await asyncio.wait([client.send(message) for client in connected_clients])
    
    # 送信者以外の接続中クライアントに、送信者の位置情報を送信
    for client_ in connected_id_list:
        await asyncio.wait(client_.send(message))
    
    

# サーバーをポート8765で起動
async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("WebSocket Server Started on ws://localhost:8765")
        await asyncio.Future()  # 無限ループ

asyncio.run(main())