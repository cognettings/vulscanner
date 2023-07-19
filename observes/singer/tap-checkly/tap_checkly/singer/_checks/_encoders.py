from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from fa_purity import (
    PureIter,
)
from fa_purity.frozen import (
    freeze,
)
from fa_purity.pure_iter.factory import (
    from_flist,
)
from fa_singer_io.json_schema import (
    JSchemaFactory,
)
from fa_singer_io.singer import (
    SingerRecord,
)
from fa_singer_io.singer.encoder import (
    EncodeItem,
    SingerEncoder,
)
from fa_singer_io.singer.schema.core import (
    Property,
)
from tap_checkly.objs import (
    CheckId,
    CheckObj,
)
from tap_checkly.singer._core import (
    SingerStreams,
)
from tap_checkly.singer._encoder import (
    ObjEncoder,
)
from typing import (
    Dict,
)

_str_type = JSchemaFactory.from_prim_type(str)
_int_type = JSchemaFactory.from_prim_type(int)
_bool_type = JSchemaFactory.from_prim_type(bool)
_date_type = JSchemaFactory.datetime_schema()


def _core_encoder_fx() -> SingerEncoder[CheckObj]:
    _mapper: Dict[str, EncodeItem[CheckObj]] = {
        "id": EncodeItem.new(
            lambda x: x.id_obj.id_str,
            Property(_str_type, True, False),
            CheckObj,
        ),
        "name": EncodeItem.new(
            lambda x: x.obj.name, Property(_str_type, False, False), CheckObj
        ),
        "created_at": EncodeItem.new(
            lambda x: x.obj.created_at.isoformat(),
            Property(_date_type, False, False),
            CheckObj,
        ),
        "updated_at": EncodeItem.new(
            lambda x: x.obj.updated_at.map(lambda d: d.isoformat()).value_or(
                None
            ),
            Property(JSchemaFactory.opt_datetime_schema(), False, False),
            CheckObj,
        ),
        "activated": EncodeItem.new(
            lambda x: x.obj.conf_1.activated,
            Property(_bool_type, False, False),
            CheckObj,
        ),
        "muted": EncodeItem.new(
            lambda x: x.obj.conf_1.muted,
            Property(_bool_type, False, False),
            CheckObj,
        ),
        "double_check": EncodeItem.new(
            lambda x: x.obj.conf_1.double_check,
            Property(_bool_type, False, False),
            CheckObj,
        ),
        "should_fail": EncodeItem.new(
            lambda x: x.obj.conf_1.should_fail,
            Property(_bool_type, False, False),
            CheckObj,
        ),
        "use_global_alert_settings": EncodeItem.new(
            lambda x: x.obj.conf_1.use_global_alert_settings,
            Property(_bool_type, False, False),
            CheckObj,
        ),
        "runtime_ver": EncodeItem.new(
            lambda x: x.obj.conf_2.runtime_ver.value_or(None),
            Property(JSchemaFactory.opt_prim_type(str), False, False),
            CheckObj,
        ),
        "check_type": EncodeItem.new(
            lambda x: x.obj.conf_2.check_type,
            Property(_str_type, False, False),
            CheckObj,
        ),
        "frequency": EncodeItem.new(
            lambda x: x.obj.conf_2.frequency,
            Property(_int_type, False, False),
            CheckObj,
        ),
        "frequency_offset": EncodeItem.new(
            lambda x: x.obj.conf_2.frequency_offset,
            Property(_int_type, False, False),
            CheckObj,
        ),
        "degraded_response_time": EncodeItem.new(
            lambda x: x.obj.conf_2.degraded_response_time,
            Property(_int_type, False, False),
            CheckObj,
        ),
        "max_response_time": EncodeItem.new(
            lambda x: x.obj.conf_2.max_response_time,
            Property(_int_type, False, False),
            CheckObj,
        ),
    }
    return SingerEncoder.new(SingerStreams.checks.value, freeze(_mapper))


_check_encoder = _core_encoder_fx()


@dataclass(frozen=True)
class LocationItem:
    check_id: CheckId
    index: int
    location: str

    @staticmethod
    def from_check_obj(item: CheckObj) -> PureIter[LocationItem]:
        return (
            from_flist(item.obj.locations)
            .enumerate(0)
            .map(
                lambda t: LocationItem(
                    item.id_obj,
                    t[0],
                    t[1],
                ),
            )
        )


def _locations_encoder_fx() -> SingerEncoder[LocationItem]:
    _mapper: Dict[str, EncodeItem[LocationItem]] = {
        "id": EncodeItem.new(
            lambda x: x.check_id.id_str,
            Property(_str_type, True, False),
            LocationItem,
        ),
        "index": EncodeItem.new(
            lambda x: x.index, Property(_int_type, True, False), LocationItem
        ),
        "location": EncodeItem.new(
            lambda x: x.location,
            Property(_str_type, False, False),
            LocationItem,
        ),
    }
    return SingerEncoder.new(
        SingerStreams.check_locations.value, freeze(_mapper)
    )


_locations_encoder = _locations_encoder_fx()


def _to_records(item: CheckObj) -> PureIter[SingerRecord]:
    _records = LocationItem.from_check_obj(item).map(
        lambda l: _locations_encoder.record(l)
    ).to_list() + (_check_encoder.record(item),)
    return from_flist(_records)


encoder: ObjEncoder[CheckObj] = ObjEncoder.new(
    from_flist((_check_encoder.schema, _locations_encoder.schema)),
    _to_records,
)
