from dataclasses import dataclass

from sqlalchemy.orm import Session

from ...entities.permission_entity import PermissionEntity
from ...entities.role_entity import RoleEntity
from ...entities.user_entity import UserEntity
from ...entities.user_role_table import user_role_table
from ...models import Permission, Role
from ...models.user import User
from .reset_table_id_seq import reset_table_id_seq


@dataclass(frozen=True)
class AuthScenario:
    root_role: Role
    ambassador_role: Role
    root_permission: Permission
    ambassador_permission: Permission
    ambassador_permission_coworking_reservation: Permission
    root: User
    ambassador: User
    user: User
    instructor: User
    uta: User
    student: User

    @property
    def roles(self) -> list[Role]:
        return [self.root_role, self.ambassador_role]

    @property
    def permissions(self) -> list[Permission]:
        return [
            self.root_permission,
            self.ambassador_permission,
            self.ambassador_permission_coworking_reservation,
        ]

    @property
    def users(self) -> list[User]:
        return [
            self.root,
            self.ambassador,
            self.user,
            self.instructor,
            self.uta,
            self.student,
        ]


def build_auth_scenario() -> AuthScenario:
    root_role = Role(id=1, name="root")
    ambassador_role = Role(id=2, name="ambassadors")

    root_permission = Permission(id=1, action="*", resource="*")
    ambassador_permission = Permission(
        id=2, action="checkin.create", resource="checkin"
    )
    ambassador_permission_coworking_reservation = Permission(
        id=3,
        action="coworking.reservation.*",
        resource="*",
    )

    root = User(
        id=1,
        pid=999999999,
        onyen="root",
        email="root@unc.edu",
        first_name="Rhonda",
        last_name="Root",
        pronouns="She / Her / Hers",
        accepted_community_agreement=True,
    )
    ambassador = User(
        id=2,
        pid=888888888,
        onyen="xlstan",
        email="amam@unc.edu",
        first_name="Amy",
        last_name="Ambassador",
        pronouns="They / Them / Theirs",
        accepted_community_agreement=True,
    )
    user = User(
        id=3,
        pid=111111111,
        onyen="user",
        email="user@unc.edu",
        first_name="Sally",
        last_name="Student",
        pronouns="She / They",
        accepted_community_agreement=True,
    )
    instructor = User(
        id=4,
        pid=222222222,
        onyen="Ina",
        email="ina@unc.edu",
        first_name="Ina",
        last_name="Instructor",
        pronouns="They / Them / Theirs",
    )
    uta = User(
        id=5,
        pid=333333333,
        onyen="uhlissa",
        email="uhlissa@unc.edu",
        first_name="Uhlissa",
        last_name="UTA",
        pronouns="They / Them / Theirs",
    )
    student = User(
        id=6,
        pid=555555555,
        onyen="Stewie",
        email="stewie@unc.edu",
        first_name="Stewie",
        last_name="Student",
        pronouns="They / Them / Theirs",
    )

    return AuthScenario(
        root_role=root_role,
        ambassador_role=ambassador_role,
        root_permission=root_permission,
        ambassador_permission=ambassador_permission,
        ambassador_permission_coworking_reservation=ambassador_permission_coworking_reservation,
        root=root,
        ambassador=ambassador,
        user=user,
        instructor=instructor,
        uta=uta,
        student=student,
    )


def arrange_auth_scenario(session: Session) -> AuthScenario:
    scenario = build_auth_scenario()

    session.add_all([RoleEntity.from_model(role) for role in scenario.roles])
    session.add_all([UserEntity.from_model(user) for user in scenario.users])
    session.flush()

    session.execute(
        user_role_table.insert(),
        [
            {"role_id": scenario.root_role.id, "user_id": scenario.root.id},
            {
                "role_id": scenario.ambassador_role.id,
                "user_id": scenario.ambassador.id,
            },
        ],
    )

    session.add_all(
        [
            PermissionEntity(
                id=scenario.root_permission.id,
                role_id=scenario.root_role.id,
                action=scenario.root_permission.action,
                resource=scenario.root_permission.resource,
            ),
            PermissionEntity(
                id=scenario.ambassador_permission.id,
                role_id=scenario.ambassador_role.id,
                action=scenario.ambassador_permission.action,
                resource=scenario.ambassador_permission.resource,
            ),
            PermissionEntity(
                id=scenario.ambassador_permission_coworking_reservation.id,
                role_id=scenario.ambassador_role.id,
                action=scenario.ambassador_permission_coworking_reservation.action,
                resource=scenario.ambassador_permission_coworking_reservation.resource,
            ),
        ]
    )

    reset_table_id_seq(session, RoleEntity, RoleEntity.id, len(scenario.roles) + 1)
    reset_table_id_seq(session, UserEntity, UserEntity.id, len(scenario.users) + 1)
    reset_table_id_seq(
        session,
        PermissionEntity,
        PermissionEntity.id,
        len(scenario.permissions) + 1,
    )
    session.commit()

    return scenario
