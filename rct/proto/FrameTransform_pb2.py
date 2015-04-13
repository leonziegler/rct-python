# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: FrameTransform.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)


import rst.geometry.Pose_pb2
import rst.timing.Timestamp_pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='FrameTransform.proto',
  package='rct',
  serialized_pb='\n\x14\x46rameTransform.proto\x12\x03rct\x1a\x17rst/geometry/Pose.proto\x1a\x1arst/timing/Timestamp.proto\"\x87\x01\n\x0e\x46rameTransform\x12%\n\ttransform\x18\x01 \x01(\x0b\x32\x12.rst.geometry.Pose\x12\x14\n\x0c\x66rame_parent\x18\x02 \x02(\t\x12\x13\n\x0b\x66rame_child\x18\x03 \x02(\t\x12#\n\x04time\x18\x04 \x01(\x0b\x32\x15.rst.timing.TimestampB\x1b\n\trct.protoB\x0e\x46rameTransform')




_FRAMETRANSFORM = _descriptor.Descriptor(
  name='FrameTransform',
  full_name='rct.FrameTransform',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='transform', full_name='rct.FrameTransform.transform', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='frame_parent', full_name='rct.FrameTransform.frame_parent', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='frame_child', full_name='rct.FrameTransform.frame_child', index=2,
      number=3, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='time', full_name='rct.FrameTransform.time', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=83,
  serialized_end=218,
)

_FRAMETRANSFORM.fields_by_name['transform'].message_type = rst.geometry.Pose_pb2._POSE
_FRAMETRANSFORM.fields_by_name['time'].message_type = rst.timing.Timestamp_pb2._TIMESTAMP
DESCRIPTOR.message_types_by_name['FrameTransform'] = _FRAMETRANSFORM

class FrameTransform(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _FRAMETRANSFORM

  # @@protoc_insertion_point(class_scope:rct.FrameTransform)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), '\n\trct.protoB\016FrameTransform')
# @@protoc_insertion_point(module_scope)
