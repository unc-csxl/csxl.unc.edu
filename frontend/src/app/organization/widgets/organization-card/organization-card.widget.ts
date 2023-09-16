/**
 * The Organization Card widget abstracts the implementation of each
 * individual organization card from the whole organization page.
 * 
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2023
 * @license MIT
 */

import { Component, Input } from '@angular/core';
import { Organization } from '../../organization.service';
import { Profile } from '/workspace/frontend/src/app/profile/profile.service';

@Component({
    selector: 'organization-card',
    templateUrl: './organization-card.widget.html',
    styleUrls: ['./organization-card.widget.css']
})
export class OrganizationCard {

    @Input() organization!: Organization
    @Input() profile?: Profile
    @Input() profilePermissions!: Map<number, number>

    isTooltipDisabled(element: HTMLElement): boolean {
        return element.scrollHeight <= element.clientHeight;
    }

    constructor() { }
}


