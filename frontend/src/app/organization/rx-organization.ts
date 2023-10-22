import { RxObject } from "../rx-object";
import { Organization } from "./organization.model"

export class RxOrganization extends RxObject<Organization[]> {

    pushOrganization(organization: Organization): void {
        this.value.push(organization);
        this.notify();
    }

    updateOrganization(organization: Organization): void {
        this.value = this.value.map((o) => {
            return o.id !== organization.id ? o : organization;
        });
        this.notify();
    }

    removeOrganization(organizationToRemove: Organization): void {
        this.value = this.value.filter(organization => 
          organizationToRemove.slug !== organization.slug);
        this.notify();
    }

}