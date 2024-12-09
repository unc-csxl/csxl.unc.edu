from enum import Enum


class OrganizationRole(str, Enum):
    PRESIDENT = "President"
    OFFICER = "Officer"
    MEMBER = "Member"
    ADMIN = "Member with Admin"
    PENDING = "Membership pending"
