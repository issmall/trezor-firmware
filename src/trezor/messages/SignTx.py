# Automatically generated by pb2py
import protobuf as p
t = p.MessageType('SignTx')
t.wire_type = 15
t.add_field(1, 'outputs_count', p.UVarintType, flags=p.FLAG_REQUIRED)
t.add_field(2, 'inputs_count', p.UVarintType, flags=p.FLAG_REQUIRED)
t.add_field(3, 'coin_name', p.UnicodeType, default=u'Bitcoin')
t.add_field(4, 'version', p.UVarintType, default=1)
t.add_field(5, 'lock_time', p.UVarintType, default=0)
SignTx = t