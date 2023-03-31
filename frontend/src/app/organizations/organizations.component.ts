import { HttpClient } from '@angular/common/http';
import { NONE_TYPE } from '@angular/compiler';
import { Component } from '@angular/core';
import { MatIconRegistry } from '@angular/material/icon';
import { DomSanitizer } from '@angular/platform-browser';
import { Observable } from 'rxjs';
import { isAuthenticated } from '../gate/gate.guard';
import { profileResolver } from '../profile/profile.resolver';
import { OrganizationsService, Organization } from './organizations.service';

@Component({
  selector: 'app-organizations',
  templateUrl: './organizations.component.html',
  styleUrls: ['./organizations.component.css']
})
export class OrganizationsComponent {

  public static Route = { 
    path: 'organizations',
    title: 'CS Organizations',
    component: OrganizationsComponent,
    canActivate: [],
    resolve: { profile: profileResolver } 
  }

  public organizations$: Observable<Organization[]>;

  searchBarQuery = "";

  constructor(private organizationService: OrganizationsService, iconRegistry: MatIconRegistry, sanitizer: DomSanitizer) {
    iconRegistry.addSvgIcon('instagram', sanitizer.bypassSecurityTrustResourceUrl('https://simpleicons.org/icons/instagram.svg'));
    iconRegistry.addSvgIcon('github', sanitizer.bypassSecurityTrustResourceUrl('https://simpleicons.org/icons/github.svg'));
    iconRegistry.addSvgIcon('linkedin', sanitizer.bypassSecurityTrustResourceUrl('https://simpleicons.org/icons/linkedin.svg'))
    iconRegistry.addSvgIcon('youtube', sanitizer.bypassSecurityTrustResourceUrl('https://simpleicons.org/icons/youtube.svg'))
    this.organizations$ = this.organizationService.getOrganizations();
    }
}
