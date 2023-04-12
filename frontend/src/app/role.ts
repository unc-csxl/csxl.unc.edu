import { Permission, Profile } from "./models.module";


export interface Role {
    id: number;
    name: string;
}

export interface RoleDetails {
    id: number;
    name: string;
    permissions: Permission[];
    users: Profile[];
}