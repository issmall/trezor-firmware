# Automatically generated by pb2py
import protobuf as p
t = p.MessageType('EncryptMessage')
t.wire_type = 49
t.add_field(1, 'pubkey', p.BytesType)
t.add_field(2, 'message', p.BytesType)
t.add_field(3, 'display_only', p.BoolType)
t.add_field(4, 'address_n', p.UVarintType, flags=p.FLAG_REPEATED)
t.add_field(5, 'coin_name', p.UnicodeType, default=u'Bitcoin')
EncryptMessage = t