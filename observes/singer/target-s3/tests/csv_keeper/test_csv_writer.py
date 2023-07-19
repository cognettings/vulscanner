from fa_purity.frozen import (
    FrozenList,
)
from fa_purity.pure_iter.factory import (
    from_flist,
)
import pytest
from target_s3._parallel import (
    ThreadPool,
)
from target_s3.core import (
    TempReadOnlyFile,
)
from target_s3.csv_keeper._format import (
    _Private,
    RawFormatedRecord,
)
from target_s3.csv_keeper._writer import (
    multifile_save,
    save_raw,
)


def test_save_raw() -> None:
    test_data = from_flist(
        (
            RawFormatedRecord(_Private(), (1, 2, 3)),
            RawFormatedRecord(_Private(), (4, 5, 6)),
        )
    )

    def _verify(data: FrozenList[str], expected: FrozenList[str]) -> None:
        assert data == expected

    with pytest.raises(SystemExit):
        ThreadPool.new(1).bind(
            lambda p: save_raw(p, test_data).map(
                lambda f: _verify(f.read().to_list(), ("1,2,3\n", "4,5,6\n"))
            )
        ).compute()


def test_multifile_save() -> None:
    test_data = from_flist(
        (
            RawFormatedRecord(_Private(), (1, 2, 3)),
            RawFormatedRecord(_Private(), (4, 5, 6)),
            RawFormatedRecord(_Private(), (10, 20, 30)),
            RawFormatedRecord(_Private(), (40, 50, 60)),
        )
    )

    def _verify(files: FrozenList[TempReadOnlyFile]) -> None:
        expected = ("1,2,3\n", "4,5,6\n")
        expected_2 = ("10,20,30\n", "40,50,60\n")
        data = files[0].read().to_list()
        data2 = files[1].read().to_list()
        assert data == expected
        assert data2 == expected_2

    with pytest.raises(SystemExit):
        ThreadPool.new(1).bind(
            lambda p: multifile_save(p, test_data, 2, 2).map(_verify)
        ).compute()
