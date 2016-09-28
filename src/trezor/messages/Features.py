# Automatically generated by pb2py
import protobuf as p
from .CoinType import CoinType
t = p.MessageType('Features')
t.wire_type = 17
t.add_field(1, 'vendor', p.UnicodeType)
t.add_field(2, 'major_version', p.UVarintType)
t.add_field(3, 'minor_version', p.UVarintType)
t.add_field(4, 'patch_version', p.UVarintType)
t.add_field(5, 'bootloader_mode', p.BoolType)
t.add_field(6, 'device_id', p.UnicodeType)
t.add_field(7, 'pin_protection', p.BoolType)
t.add_field(8, 'passphrase_protection', p.BoolType)
t.add_field(9, 'language', p.UnicodeType)
t.add_field(10, 'label', p.UnicodeType)
t.add_field(11, 'coins', p.EmbeddedMessage(CoinType), flags=p.FLAG_REPEATED)
t.add_field(12, 'initialized', p.BoolType)
t.add_field(13, 'revision', p.BytesType)
t.add_field(14, 'bootloader_hash', p.BytesType)
t.add_field(15, 'imported', p.BoolType)
t.add_field(16, 'pin_cached', p.BoolType)
t.add_field(17, 'passphrase_cached', p.BoolType)
Features = t