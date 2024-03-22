from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    new_user = User(username='test', email='teste@teste', password='secret')
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'test'))

    assert user.username == 'test'
