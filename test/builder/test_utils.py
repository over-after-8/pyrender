import pytest
from render.builder.viewmodel import ViewModel

from render.builder.utils import inheritors


@pytest.fixture(scope="module")
def klass():
    return ViewModel


def test_inheritors(klass):
    from render.www.views.role_view_model import RoleVM
    from render.www.views.user_view_model import UserVM
    from render.www.views.permission_view_model import PermissionVM

    res = inheritors(klass)
    assert res is not None
    for k in res:
        print(k.__name__)
