# Automatically generated by pb2py
import protobuf as p
t = p.MessageType('TxOutputBinType')
t.add_field(1, 'amount', p.UVarintType, flags=p.FLAG_REQUIRED)
t.add_field(2, 'script_pubkey', p.BytesType, flags=p.FLAG_REQUIRED)
TxOutputBinType = t