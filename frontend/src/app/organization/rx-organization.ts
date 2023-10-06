import { RxObject } from "../rx-object";
import { Organization, Organizations } from "./organization.service"

export class RxOrganization extends RxObject<Organizations> {

    pushOrganization(organization: Organization): void {
        this.value.organizations.push(organization);
        this.notify();
    }

    updateOrganization(organization: Organization): void {
        this.value.organizations = this.value.organizations.map((o) => {
            return o.id !== organization.id ? o : organization;
        });
        this.notify();
    }

    removeOrganization(organizationToRemove: Organization): void {
        this.value.organizations = this.value.organizations.filter(organization => 
          organizationToRemove.id !== organization.id);
        this.notify();
    }

}