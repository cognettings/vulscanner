from .types import (
    UPD_SCA_TABLE_STR,
)
from aioextensions import (
    run,
)
import pytest
from pytest_mock import (
    MockerFixture,
)
from schedulers.invoker import (
    main as invoker_main,
)


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.parametrize("is_coroutine", [True, False])
def test_invoker_main(mocker: MockerFixture, is_coroutine: bool) -> None:
    table_main_func_str: str = f"{UPD_SCA_TABLE_STR}.main"
    invoker_mod_str: str = "schedulers.invoker"
    dyn_start_mock = mocker.patch(f"{invoker_mod_str}.dynamo_startup")
    dyn_down_mock = mocker.patch(f"{invoker_mod_str}.dynamo_shutdown")
    in_thread_mock = mocker.patch(f"{invoker_mod_str}.in_thread")
    table_main_mock = mocker.patch(table_main_func_str)
    mocker.patch(f"{invoker_mod_str}.sys", argv=["test", table_main_func_str])
    mocker.patch(
        f"{invoker_mod_str}.asyncio.iscoroutinefunction",
        return_value=is_coroutine,
    )
    run(invoker_main())
    assert dyn_start_mock.await_count == 1
    assert dyn_down_mock.await_count == 1
    if is_coroutine:
        assert table_main_mock.await_count == 1
    else:
        assert in_thread_mock.await_count == 1
