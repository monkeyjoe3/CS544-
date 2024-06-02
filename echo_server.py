import asyncio
from typing import Coroutine,Dict
import json
from echo_quic import EchoQuicConnection, QuicStreamEvent
import pdu



async def echo_server_proto(scope:Dict, conn:EchoQuicConnection):

        ## reads in the user data
        ## will be used to verify user is legit
        with open('user_db.json') as f:
                users = json.load(f)
                f.close()
        
        message:QuicStreamEvent = await conn.receive()
        
        dgram_in = pdu.Datagram.from_bytes(message.data)
        print("[svr] received message: ", dgram_in.msg)
        
        stream_id = message.stream_id
        
        dgram_out = dgram_in
        dgram_out.mtype |= pdu.MSG_TYPE_DATA_ACK
        dgram_out.msg = "SVR-ACK: " + dgram_out.msg
        rsp_msg = dgram_out.to_bytes()
        rsp_evnt = QuicStreamEvent(stream_id, rsp_msg, False)
        await conn.send(rsp_evnt)