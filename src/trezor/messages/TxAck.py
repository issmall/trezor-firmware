# Automatically generated by pb2py
import protobuf as p
from .TransactionType import TransactionType
t = p.MessageType('TxAck')
t.wire_type = 22
t.add_field(1, 'tx', p.EmbeddedMessage(TransactionType))
TxAck = t