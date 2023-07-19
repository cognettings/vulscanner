from fa_purity import (
    FrozenDict,
    Maybe,
    Result,
    ResultE,
)
from fa_purity.json_2 import (
    JsonObj,
    JsonPrimitive,
    UnfoldedFactory,
    Unfolder,
)
from fa_purity.json_2.primitive import (
    JsonPrimitiveUnfolder,
)
from redshift_client.sql_client.connection import (
    Credentials as DbCredentials,
    DatabaseId,
)
from tap_zoho_crm.api.auth import (
    Credentials,
)
from typing import (
    IO,
    Tuple,
    TypeVar,
)

_K = TypeVar("_K")
_V = TypeVar("_V")


def _get(items: FrozenDict[_K, _V], key: _K) -> Maybe[_V]:
    if key in items:
        return Maybe.from_value(items[key])
    return Maybe.empty()


def _require(items: FrozenDict[_K, _V], key: _K) -> ResultE[_V]:
    return _get(items, key).to_result().alt(lambda _: Exception(KeyError(key)))


def _try_to_int(raw: JsonPrimitive) -> ResultE[int]:
    def _to_int(data: str) -> ResultE[int]:
        try:
            return Result.success(int(data))
        except ValueError as err:
            return Result.failure(Exception(err))

    return JsonPrimitiveUnfolder.to_int(raw).lash(
        lambda _: JsonPrimitiveUnfolder.to_str(raw).bind(_to_int)
    )


def decode_zoho_creds(auth_file: IO[str]) -> ResultE[Credentials]:
    def _decode(raw: JsonObj) -> ResultE[Credentials]:
        client_id = (
            _require(raw, "client_id")
            .bind(Unfolder.to_primitive)
            .bind(JsonPrimitiveUnfolder.to_str)
        )
        client_secret = (
            _require(raw, "client_secret")
            .bind(Unfolder.to_primitive)
            .bind(JsonPrimitiveUnfolder.to_str)
        )
        refresh_token = (
            _require(raw, "refresh_token")
            .bind(Unfolder.to_primitive)
            .bind(JsonPrimitiveUnfolder.to_str)
        )
        scopes_result = _require(raw, "scopes").bind(
            lambda i: Unfolder.to_list_of(
                i,
                lambda x: Unfolder.to_primitive(x).bind(
                    JsonPrimitiveUnfolder.to_str
                ),
            )
        )
        return client_id.bind(
            lambda cid: client_secret.bind(
                lambda secret: refresh_token.bind(
                    lambda token: scopes_result.map(
                        lambda scopes: Credentials(
                            cid, secret, token, frozenset(scopes)
                        )
                    )
                )
            )
        )

    return UnfoldedFactory.load(auth_file).bind(_decode)


def decode_db_id(raw: JsonObj) -> ResultE[DatabaseId]:
    db_name_result = (
        _require(raw, "dbname")
        .bind(Unfolder.to_primitive)
        .bind(JsonPrimitiveUnfolder.to_str)
    )
    host_result = (
        _require(raw, "host")
        .bind(Unfolder.to_primitive)
        .bind(JsonPrimitiveUnfolder.to_str)
    )
    port_result = (
        _require(raw, "port").bind(Unfolder.to_primitive).bind(_try_to_int)
    )
    return db_name_result.bind(
        lambda db_name: host_result.bind(
            lambda host: port_result.map(
                lambda port: DatabaseId(db_name, host, port)
            )
        )
    )


def decode_db_creds(raw: JsonObj) -> ResultE[DbCredentials]:
    name_result = (
        _require(raw, "user")
        .bind(Unfolder.to_primitive)
        .bind(JsonPrimitiveUnfolder.to_str)
    )
    password_result = (
        _require(raw, "password")
        .bind(Unfolder.to_primitive)
        .bind(JsonPrimitiveUnfolder.to_str)
    )
    return name_result.bind(
        lambda name: password_result.map(
            lambda password: DbCredentials(name, password)
        )
    )


def decode_db_conf(
    auth_file: IO[str],
) -> ResultE[Tuple[DatabaseId, DbCredentials]]:
    return UnfoldedFactory.load(auth_file).bind(
        lambda j: decode_db_id(j).bind(
            lambda db_id: decode_db_creds(j).map(lambda c: (db_id, c))
        )
    )
