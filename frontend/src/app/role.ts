import { Permission, Profile } from "./profile/profile.service";

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