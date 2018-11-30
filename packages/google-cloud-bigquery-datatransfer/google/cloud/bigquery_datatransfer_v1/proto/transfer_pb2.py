# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/cloud/bigquery/datatransfer_v1/proto/transfer.proto

import sys

_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode("latin1"))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from google.rpc import status_pb2 as google_dot_rpc_dot_status__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
    name="google/cloud/bigquery/datatransfer_v1/proto/transfer.proto",
    package="google.cloud.bigquery.datatransfer.v1",
    syntax="proto3",
    serialized_pb=_b(
        '\n:google/cloud/bigquery/datatransfer_v1/proto/transfer.proto\x12%google.cloud.bigquery.datatransfer.v1\x1a\x1cgoogle/api/annotations.proto\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x17google/rpc/status.proto"\xad\x03\n\x0eTransferConfig\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x1e\n\x16\x64\x65stination_dataset_id\x18\x02 \x01(\t\x12\x14\n\x0c\x64isplay_name\x18\x03 \x01(\t\x12\x16\n\x0e\x64\x61ta_source_id\x18\x05 \x01(\t\x12\'\n\x06params\x18\t \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x10\n\x08schedule\x18\x07 \x01(\t\x12 \n\x18\x64\x61ta_refresh_window_days\x18\x0c \x01(\x05\x12\x10\n\x08\x64isabled\x18\r \x01(\x08\x12/\n\x0bupdate_time\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x31\n\rnext_run_time\x18\x08 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x43\n\x05state\x18\n \x01(\x0e\x32\x34.google.cloud.bigquery.datatransfer.v1.TransferState\x12\x0f\n\x07user_id\x18\x0b \x01(\x03\x12\x16\n\x0e\x64\x61taset_region\x18\x0e \x01(\t"\xfe\x03\n\x0bTransferRun\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x31\n\rschedule_time\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12,\n\x08run_time\x18\n \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12(\n\x0c\x65rror_status\x18\x15 \x01(\x0b\x32\x12.google.rpc.Status\x12.\n\nstart_time\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12,\n\x08\x65nd_time\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12/\n\x0bupdate_time\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\'\n\x06params\x18\t \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x1e\n\x16\x64\x65stination_dataset_id\x18\x02 \x01(\t\x12\x16\n\x0e\x64\x61ta_source_id\x18\x07 \x01(\t\x12\x43\n\x05state\x18\x08 \x01(\x0e\x32\x34.google.cloud.bigquery.datatransfer.v1.TransferState\x12\x0f\n\x07user_id\x18\x0b \x01(\x03\x12\x10\n\x08schedule\x18\x0c \x01(\t"\x8a\x02\n\x0fTransferMessage\x12\x30\n\x0cmessage_time\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12X\n\x08severity\x18\x02 \x01(\x0e\x32\x46.google.cloud.bigquery.datatransfer.v1.TransferMessage.MessageSeverity\x12\x14\n\x0cmessage_text\x18\x03 \x01(\t"U\n\x0fMessageSeverity\x12 \n\x1cMESSAGE_SEVERITY_UNSPECIFIED\x10\x00\x12\x08\n\x04INFO\x10\x01\x12\x0b\n\x07WARNING\x10\x02\x12\t\n\x05\x45RROR\x10\x03*G\n\x0cTransferType\x12\x1d\n\x19TRANSFER_TYPE_UNSPECIFIED\x10\x00\x12\t\n\x05\x42\x41TCH\x10\x01\x12\r\n\tSTREAMING\x10\x02*s\n\rTransferState\x12\x1e\n\x1aTRANSFER_STATE_UNSPECIFIED\x10\x00\x12\x0b\n\x07PENDING\x10\x02\x12\x0b\n\x07RUNNING\x10\x03\x12\r\n\tSUCCEEDED\x10\x04\x12\n\n\x06\x46\x41ILED\x10\x05\x12\r\n\tCANCELLED\x10\x06\x42\xe7\x01\n)com.google.cloud.bigquery.datatransfer.v1B\rTransferProtoP\x01ZQgoogle.golang.org/genproto/googleapis/cloud/bigquery/datatransfer/v1;datatransfer\xa2\x02\x05GCBDT\xaa\x02%Google.Cloud.BigQuery.DataTransfer.V1\xca\x02%Google\\Cloud\\BigQuery\\DataTransfer\\V1b\x06proto3'
    ),
    dependencies=[
        google_dot_api_dot_annotations__pb2.DESCRIPTOR,
        google_dot_protobuf_dot_struct__pb2.DESCRIPTOR,
        google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,
        google_dot_rpc_dot_status__pb2.DESCRIPTOR,
    ],
)

_TRANSFERTYPE = _descriptor.EnumDescriptor(
    name="TransferType",
    full_name="google.cloud.bigquery.datatransfer.v1.TransferType",
    filename=None,
    file=DESCRIPTOR,
    values=[
        _descriptor.EnumValueDescriptor(
            name="TRANSFER_TYPE_UNSPECIFIED", index=0, number=0, options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="BATCH", index=1, number=1, options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="STREAMING", index=2, number=2, options=None, type=None
        ),
    ],
    containing_type=None,
    options=None,
    serialized_start=1433,
    serialized_end=1504,
)
_sym_db.RegisterEnumDescriptor(_TRANSFERTYPE)

TransferType = enum_type_wrapper.EnumTypeWrapper(_TRANSFERTYPE)
_TRANSFERSTATE = _descriptor.EnumDescriptor(
    name="TransferState",
    full_name="google.cloud.bigquery.datatransfer.v1.TransferState",
    filename=None,
    file=DESCRIPTOR,
    values=[
        _descriptor.EnumValueDescriptor(
            name="TRANSFER_STATE_UNSPECIFIED",
            index=0,
            number=0,
            options=None,
            type=None,
        ),
        _descriptor.EnumValueDescriptor(
            name="PENDING", index=1, number=2, options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="RUNNING", index=2, number=3, options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="SUCCEEDED", index=3, number=4, options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="FAILED", index=4, number=5, options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="CANCELLED", index=5, number=6, options=None, type=None
        ),
    ],
    containing_type=None,
    options=None,
    serialized_start=1506,
    serialized_end=1621,
)
_sym_db.RegisterEnumDescriptor(_TRANSFERSTATE)

TransferState = enum_type_wrapper.EnumTypeWrapper(_TRANSFERSTATE)
TRANSFER_TYPE_UNSPECIFIED = 0
BATCH = 1
STREAMING = 2
TRANSFER_STATE_UNSPECIFIED = 0
PENDING = 2
RUNNING = 3
SUCCEEDED = 4
FAILED = 5
CANCELLED = 6


_TRANSFERMESSAGE_MESSAGESEVERITY = _descriptor.EnumDescriptor(
    name="MessageSeverity",
    full_name="google.cloud.bigquery.datatransfer.v1.TransferMessage.MessageSeverity",
    filename=None,
    file=DESCRIPTOR,
    values=[
        _descriptor.EnumValueDescriptor(
            name="MESSAGE_SEVERITY_UNSPECIFIED",
            index=0,
            number=0,
            options=None,
            type=None,
        ),
        _descriptor.EnumValueDescriptor(
            name="INFO", index=1, number=1, options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="WARNING", index=2, number=2, options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="ERROR", index=3, number=3, options=None, type=None
        ),
    ],
    containing_type=None,
    options=None,
    serialized_start=1346,
    serialized_end=1431,
)
_sym_db.RegisterEnumDescriptor(_TRANSFERMESSAGE_MESSAGESEVERITY)


_TRANSFERCONFIG = _descriptor.Descriptor(
    name="TransferConfig",
    full_name="google.cloud.bigquery.datatransfer.v1.TransferConfig",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="name",
            full_name="google.cloud.bigquery.datatransfer.v1.TransferConfig.name",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="destination_dataset_id",
            full_name="google.cloud.bigquery.datatransfer.v1.TransferConfig.destination_dataset_id",
            index=1,
            number=2,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="display_name",
            full_name="google.cloud.bigquery.datatransfer.v1.TransferConfig.display_name",
            index=2,
            number=3,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="data_source_id",
            full_name="google.cloud.bigquery.datatransfer.v1.TransferConfig.data_source_id",
            index=3,
            number=5,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="params",
            full_name="google.cloud.bigquery.datatransfer.v1.TransferConfig.params",
            index=4,
            number=9,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="schedule",
            full_name="google.cloud.bigquery.datatransfer.v1.TransferConfig.schedule",
            index=5,
            number=7,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="data_refresh_window_days",
            full_name="google.cloud.bigquery.datatransfer.v1.TransferConfig.data_refresh_window_days",
            index=6,
            number=12,
            type=5,
            cpp_type=1,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="disabled",
            full_name="google.cloud.bigquery.datatransfer.v1.TransferConfig.disabled",
            index=7,
            number=13,
            type=8,
            cpp_type=7,
            label=1,
            has_default_value=False,
            default_value=False,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="update_time",
            full_name="google.cloud.bigquery.datatransfer.v1.TransferConfig.update_time",
            index=8,
            number=4,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="next_run_time",
            full_name="google.cloud.bigquery.datatransfer.v1.TransferConfig.next_run_time",
            index=9,
            number=8,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="state",
            full_name="google.cloud.bigquery.datatransfer.v1.TransferConfig.state",
            index=10,
            number=10,
            type=14,
            cpp_type=8,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="user_id",
            full_name="google.cloud.bigquery.datatransfer.v1.TransferConfig.user_id",
            index=11,
            number=11,
            type=3,
            cpp_type=2,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="dataset_region",
            full_name="google.cloud.bigquery.datatransfer.v1.TransferConfig.dataset_region",
            index=12,
            number=14,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=220,
    serialized_end=649,
)


_TRANSFERRUN = _descriptor.Descriptor(
    name="TransferRun",
    full_name="google.cloud.bigquery.datatransfer.v1.TransferRun",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="name",
            full_name="google.cloud.bigquery.datatransfer.v1.TransferRun.name",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="schedule_time",
            full_name="google.cloud.bigquery.datatransfer.v1.TransferRun.schedule_time",
            index=1,
            number=3,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="run_time",
            full_name="google.cloud.bigquery.datatransfer.v1.TransferRun.run_time",
            index=2,
            number=10,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="error_status",
            full_name="google.cloud.bigquery.datatransfer.v1.TransferRun.error_status",
            index=3,
            number=21,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="start_time",
            full_name="google.cloud.bigquery.datatransfer.v1.TransferRun.start_time",
            index=4,
            number=4,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="end_time",
            full_name="google.cloud.bigquery.datatransfer.v1.TransferRun.end_time",
            index=5,
            number=5,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="update_time",
            full_name="google.cloud.bigquery.datatransfer.v1.TransferRun.update_time",
            index=6,
            number=6,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="params",
            full_name="google.cloud.bigquery.datatransfer.v1.TransferRun.params",
            index=7,
            number=9,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="destination_dataset_id",
            full_name="google.cloud.bigquery.datatransfer.v1.TransferRun.destination_dataset_id",
            index=8,
            number=2,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="data_source_id",
            full_name="google.cloud.bigquery.datatransfer.v1.TransferRun.data_source_id",
            index=9,
            number=7,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="state",
            full_name="google.cloud.bigquery.datatransfer.v1.TransferRun.state",
            index=10,
            number=8,
            type=14,
            cpp_type=8,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="user_id",
            full_name="google.cloud.bigquery.datatransfer.v1.TransferRun.user_id",
            index=11,
            number=11,
            type=3,
            cpp_type=2,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="schedule",
            full_name="google.cloud.bigquery.datatransfer.v1.TransferRun.schedule",
            index=12,
            number=12,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=652,
    serialized_end=1162,
)


_TRANSFERMESSAGE = _descriptor.Descriptor(
    name="TransferMessage",
    full_name="google.cloud.bigquery.datatransfer.v1.TransferMessage",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="message_time",
            full_name="google.cloud.bigquery.datatransfer.v1.TransferMessage.message_time",
            index=0,
            number=1,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="severity",
            full_name="google.cloud.bigquery.datatransfer.v1.TransferMessage.severity",
            index=1,
            number=2,
            type=14,
            cpp_type=8,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="message_text",
            full_name="google.cloud.bigquery.datatransfer.v1.TransferMessage.message_text",
            index=2,
            number=3,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[_TRANSFERMESSAGE_MESSAGESEVERITY],
    options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=1165,
    serialized_end=1431,
)

_TRANSFERCONFIG.fields_by_name[
    "params"
].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_TRANSFERCONFIG.fields_by_name[
    "update_time"
].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_TRANSFERCONFIG.fields_by_name[
    "next_run_time"
].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_TRANSFERCONFIG.fields_by_name["state"].enum_type = _TRANSFERSTATE
_TRANSFERRUN.fields_by_name[
    "schedule_time"
].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_TRANSFERRUN.fields_by_name[
    "run_time"
].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_TRANSFERRUN.fields_by_name[
    "error_status"
].message_type = google_dot_rpc_dot_status__pb2._STATUS
_TRANSFERRUN.fields_by_name[
    "start_time"
].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_TRANSFERRUN.fields_by_name[
    "end_time"
].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_TRANSFERRUN.fields_by_name[
    "update_time"
].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_TRANSFERRUN.fields_by_name[
    "params"
].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_TRANSFERRUN.fields_by_name["state"].enum_type = _TRANSFERSTATE
_TRANSFERMESSAGE.fields_by_name[
    "message_time"
].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_TRANSFERMESSAGE.fields_by_name["severity"].enum_type = _TRANSFERMESSAGE_MESSAGESEVERITY
_TRANSFERMESSAGE_MESSAGESEVERITY.containing_type = _TRANSFERMESSAGE
DESCRIPTOR.message_types_by_name["TransferConfig"] = _TRANSFERCONFIG
DESCRIPTOR.message_types_by_name["TransferRun"] = _TRANSFERRUN
DESCRIPTOR.message_types_by_name["TransferMessage"] = _TRANSFERMESSAGE
DESCRIPTOR.enum_types_by_name["TransferType"] = _TRANSFERTYPE
DESCRIPTOR.enum_types_by_name["TransferState"] = _TRANSFERSTATE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TransferConfig = _reflection.GeneratedProtocolMessageType(
    "TransferConfig",
    (_message.Message,),
    dict(
        DESCRIPTOR=_TRANSFERCONFIG,
        __module__="google.cloud.bigquery.datatransfer_v1.proto.transfer_pb2",
        __doc__="""Represents a data transfer configuration. A transfer configuration
  contains all metadata needed to perform a data transfer. For example,
  ``destination_dataset_id`` specifies where data should be stored. When a
  new transfer configuration is created, the specified
  ``destination_dataset_id`` is created when needed and shared with the
  appropriate data source service account.
  
  
  Attributes:
      name:
          The resource name of the transfer config. Transfer config
          names have the form
          ``projects/{project_id}/transferConfigs/{config_id}``. Where
          ``config_id`` is usually a uuid, even though it is not
          guaranteed or required. The name is ignored when creating a
          transfer config.
      destination_dataset_id:
          The BigQuery target dataset id.
      display_name:
          User specified display name for the data transfer.
      data_source_id:
          Data source id. Cannot be changed once data transfer is
          created.
      params:
          Data transfer specific parameters.
      schedule:
          Data transfer schedule. If the data source does not support a
          custom schedule, this should be empty. If it is empty, the
          default value for the data source will be used. The specified
          times are in UTC. Examples of valid format: ``1st,3rd monday
          of month 15:30``, ``every wed,fri of jan,jun 13:15``, and
          ``first sunday of quarter 00:00``. See more explanation about
          the format here: https://cloud.google.com/appengine/docs/flexi
          ble/python/scheduling-jobs-with-cron-
          yaml#the\_schedule\_format NOTE: the granularity should be at
          least 8 hours, or less frequent.
      data_refresh_window_days:
          The number of days to look back to automatically refresh the
          data. For example, if ``data_refresh_window_days = 10``, then
          every day BigQuery reingests data for [today-10, today-1],
          rather than ingesting data for just [today-1]. Only valid if
          the data source supports the feature. Set the value to 0 to
          use the default value.
      disabled:
          Is this config disabled. When set to true, no runs are
          scheduled for a given transfer.
      update_time:
          Output only. Data transfer modification time. Ignored by
          server on input.
      next_run_time:
          Output only. Next time when data transfer will run.
      state:
          Output only. State of the most recently updated transfer run.
      user_id:
          Output only. Unique ID of the user on whose behalf transfer is
          done. Applicable only to data sources that do not support
          service accounts. When set to 0, the data source service
          account credentials are used. May be negative. Note, that this
          identifier is not stable. It may change over time even for the
          same user.
      dataset_region:
          Output only. Region in which BigQuery dataset is located.
  """,
        # @@protoc_insertion_point(class_scope:google.cloud.bigquery.datatransfer.v1.TransferConfig)
    ),
)
_sym_db.RegisterMessage(TransferConfig)

TransferRun = _reflection.GeneratedProtocolMessageType(
    "TransferRun",
    (_message.Message,),
    dict(
        DESCRIPTOR=_TRANSFERRUN,
        __module__="google.cloud.bigquery.datatransfer_v1.proto.transfer_pb2",
        __doc__="""Represents a data transfer run.
  
  
  Attributes:
      name:
          The resource name of the transfer run. Transfer run names have
          the form ``projects/{project_id}/locations/{location}/transfer
          Configs/{config_id}/runs/{run_id}``. The name is ignored when
          creating a transfer run.
      schedule_time:
          Minimum time after which a transfer run can be started.
      run_time:
          For batch transfer runs, specifies the date and time that data
          should be ingested.
      error_status:
          Status of the transfer run.
      start_time:
          Output only. Time when transfer run was started. Parameter
          ignored by server for input requests.
      end_time:
          Output only. Time when transfer run ended. Parameter ignored
          by server for input requests.
      update_time:
          Output only. Last time the data transfer run state was
          updated.
      params:
          Output only. Data transfer specific parameters.
      destination_dataset_id:
          Output only. The BigQuery target dataset id.
      data_source_id:
          Output only. Data source id.
      state:
          Data transfer run state. Ignored for input requests.
      user_id:
          Output only. Unique ID of the user on whose behalf transfer is
          done. Applicable only to data sources that do not support
          service accounts. When set to 0, the data source service
          account credentials are used. May be negative. Note, that this
          identifier is not stable. It may change over time even for the
          same user.
      schedule:
          Output only. Describes the schedule of this transfer run if it
          was created as part of a regular schedule. For batch transfer
          runs that are scheduled manually, this is empty. NOTE: the
          system might choose to delay the schedule depending on the
          current load, so ``schedule_time`` doesn't always matches
          this.
  """,
        # @@protoc_insertion_point(class_scope:google.cloud.bigquery.datatransfer.v1.TransferRun)
    ),
)
_sym_db.RegisterMessage(TransferRun)

TransferMessage = _reflection.GeneratedProtocolMessageType(
    "TransferMessage",
    (_message.Message,),
    dict(
        DESCRIPTOR=_TRANSFERMESSAGE,
        __module__="google.cloud.bigquery.datatransfer_v1.proto.transfer_pb2",
        __doc__="""Represents a user facing message for a particular data transfer run.
  
  
  Attributes:
      message_time:
          Time when message was logged.
      severity:
          Message severity.
      message_text:
          Message text.
  """,
        # @@protoc_insertion_point(class_scope:google.cloud.bigquery.datatransfer.v1.TransferMessage)
    ),
)
_sym_db.RegisterMessage(TransferMessage)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(
    descriptor_pb2.FileOptions(),
    _b(
        "\n)com.google.cloud.bigquery.datatransfer.v1B\rTransferProtoP\001ZQgoogle.golang.org/genproto/googleapis/cloud/bigquery/datatransfer/v1;datatransfer\242\002\005GCBDT\252\002%Google.Cloud.BigQuery.DataTransfer.V1\312\002%Google\\Cloud\\BigQuery\\DataTransfer\\V1"
    ),
)
# @@protoc_insertion_point(module_scope)
