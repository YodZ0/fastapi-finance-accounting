from pydantic import BaseModel, ConfigDict


class Permissions(BaseModel):
    can_create_categories: bool = False
    can_read_categories: bool = True
    can_delete_categories: bool = False

    can_create_role: bool = False
    can_read_roles: bool = False
    can_delete_roles: bool = False


class RoleBase(BaseModel):
    name: str
    permissions: Permissions = Permissions()


class RoleCreate(RoleBase):
    pass


class Role(RoleBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
