from sqlalchemy.orm import Session
from ...models import User
from ...services import AccessControlService
    
def test_foo(test_session: Session):
    svc = AccessControlService(test_session)
    assert not svc.has_permission_to(User(pid=123), 'foo', 'bar')