/** Constructs the Organizations page and stores/retrieves any necessary data for it. */

import { Component } from '@angular/core';
import { MatIconRegistry } from '@angular/material/icon';
import { DomSanitizer } from '@angular/platform-browser';
import { Observable } from 'rxjs';
import { profileResolver } from '../profile/profile.resolver';
import { OrganizationsService, Organization } from './organizations.service';

@Component({
  selector: 'app-organizations',
  templateUrl: './organizations.component.html',
  styleUrls: ['./organizations.component.css']
})
export class OrganizationsComponent {

  /** Route information to be used in App Routing Module */
  public static Route = { 
    path: 'organizations',
    title: 'CS Organizations',
    component: OrganizationsComponent,
    canActivate: [],
    resolve: { profile: profileResolver } 
  }

  /** Store Observable list of Organizations */
  public organizations$: Observable<Organization[]>;

  /** Store searchBarQuery */
  searchBarQuery = "";

  constructor(private organizationService: OrganizationsService, iconRegistry: MatIconRegistry, sanitizer: DomSanitizer) {
    /** Import Logos using MatIconRegistry */
    iconRegistry.addSvgIcon('instagram', sanitizer.bypassSecurityTrustResourceUrl('https://simpleicons.org/icons/instagram.svg'));
    iconRegistry.addSvgIcon('github', sanitizer.bypassSecurityTrustResourceUrl('https://simpleicons.org/icons/github.svg'));
    iconRegistry.addSvgIcon('linkedin', sanitizer.bypassSecurityTrustResourceUrl('https://simpleicons.org/icons/linkedin.svg'))
    iconRegistry.addSvgIcon('youtube', sanitizer.bypassSecurityTrustResourceUrl('https://simpleicons.org/icons/youtube.svg'))
    
    /** Retrieve Organizations using OrganizationsService */
    this.organizations$ = this.organizationService.getOrganizations();
    }
    
}
