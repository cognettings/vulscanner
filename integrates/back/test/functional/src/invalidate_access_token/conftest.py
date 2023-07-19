# pylint: disable=import-error
from back.test import (
    db,
)
from db_model.stakeholders.types import (
    AccessTokens,
    Stakeholder,
)
import pytest
import pytest_asyncio
from typing import (
    Any,
)
import uuid


@pytest.mark.resolver_test_group("invalidate_access_token")
@pytest_asyncio.fixture(autouse=True, scope="session")
async def populate(generic_data: dict[str, Any]) -> bool:
    data = {
        "stakeholders": [
            Stakeholder(
                email="admin@gmail.com",
                access_tokens=[
                    AccessTokens(
                        id=str(uuid.uuid4()),
                        issued_at=1634677195,
                        jti_hashed=(
                            "c8d9d5f058cf200f7435508fc2dba37d07447ec12dcd07"
                        ),
                        salt="27c7f38dd7cc432871c84b63e78cd716739c40055253c",
                    )
                ],
                legal_remember=False,
                is_registered=True,
            ),
            Stakeholder(
                email="hacker@gmail.com",
                access_tokens=[
                    AccessTokens(
                        id=str(uuid.uuid4()),
                        issued_at=1634677195,
                        jti_hashed="958cf200f7408fc2dba37d07447ec12dcd07",
                        salt="32871c84b68cd716739c40055253c",
                    )
                ],
                legal_remember=False,
                is_registered=True,
            ),
            Stakeholder(
                email="reattacker@gmail.com",
                access_tokens=[
                    AccessTokens(
                        id=str(uuid.uuid4()),
                        issued_at=1657298463,
                        jti_hashed=(
                            "c8d9d5f058cf200f7435508fc2dba37d07447ec12dcd07"
                        ),
                        salt="27c7f38dd7cc432871c84b63e78cd716739c40055253c",
                    )
                ],
                legal_remember=False,
                is_registered=True,
            ),
            Stakeholder(
                email="user@gmail.com",
                access_tokens=[
                    AccessTokens(
                        id=str(uuid.uuid4()),
                        issued_at=1657298264,
                        jti_hashed=(
                            "c8d9d5f09595200f7435508fc2dba37d07447ec12dcd07"
                        ),
                        salt="27c7f388ccdc432871c84b63e78cd716739c40055253c",
                    )
                ],
                legal_remember=False,
                is_registered=True,
            ),
            Stakeholder(
                email="user_manager@gmail.com",
                access_tokens=[
                    AccessTokens(
                        id=str(uuid.uuid4()),
                        issued_at=1657298299,
                        jti_hashed=(
                            "c8d9d5f09595800f7435508fc2dba37d07447ec12dcd07"
                        ),
                        salt="27c7f388ccdd432871c84b63e78cd716739c40055253c",
                    )
                ],
                legal_remember=False,
                is_registered=True,
            ),
            Stakeholder(
                email="vulnerability_manager@gmail.com",
                access_tokens=[
                    AccessTokens(
                        id=str(uuid.uuid4()),
                        issued_at=1657298346,
                        jti_hashed=(
                            "c8d9d5f09595200f7435508fc2dba37d07447ec12dcd07"
                        ),
                        salt="27c7fccdd7cc432871c84b63e78cd716739c40055253c",
                    )
                ],
                legal_remember=False,
                is_registered=True,
            ),
            Stakeholder(
                email="resourcer@gmail.com",
                access_tokens=[
                    AccessTokens(
                        id=str(uuid.uuid4()),
                        issued_at=1657298463,
                        jti_hashed=(
                            "c8d9d5f09595200f7435508fc2dba37d07447ec12dcd07"
                        ),
                        salt="27c7f388cccc432871c84b63e78cd716739c40055253c",
                    )
                ],
                legal_remember=False,
                is_registered=True,
            ),
            Stakeholder(
                email="reviewer@gmail.com",
                access_tokens=[
                    AccessTokens(
                        id=str(uuid.uuid4()),
                        issued_at=1657295874,
                        jti_hashed=(
                            "c8d9d5f09595200f7435508fc2dba37d07447ec12dcd07"
                        ),
                        salt="27c7f388ccdc432871c84b63e78cd716739c40055253c",
                    )
                ],
                legal_remember=False,
                is_registered=True,
            ),
            Stakeholder(
                email="service_forces@gmail.com",
                access_tokens=[
                    AccessTokens(
                        id=str(uuid.uuid4()),
                        issued_at=1657278953,
                        jti_hashed=(
                            "c8d9d5f0959f200f7435508fc2dba37d07447ec12dcd07"
                        ),
                        salt="27c7f388c7cc432871c84b63e78cd716739c40055253c",
                    )
                ],
                legal_remember=False,
                is_registered=True,
            ),
            Stakeholder(
                email="customer_manager@fluidattacks.com",
                access_tokens=[
                    AccessTokens(
                        id=str(uuid.uuid4()),
                        issued_at=1657287433,
                        jti_hashed=(
                            "c8d9d5f0959f200f7435508fc2dba37d07447ec12dcd07"
                        ),
                        salt="27c7f388cccc432871c84b63e78cd716739c40055253c",
                    )
                ],
                legal_remember=False,
                is_registered=True,
            ),
        ],
    }
    return await db.populate({**generic_data["db_data"], **data})
