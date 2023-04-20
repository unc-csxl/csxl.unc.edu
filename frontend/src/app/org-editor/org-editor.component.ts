import { Component } from '@angular/core';
import { ActivatedRoute, Route, Router } from '@angular/router';
import { OrganizationSummary, Profile } from 'src/app/models.module';
import { FormBuilder } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { OrgEditorService } from './org-editor.service';
import { Observable } from 'rxjs';
import { profileResolver } from '../profile/profile.resolver';


@Component({
  selector: 'app-org-editor',
  templateUrl: './org-editor.component.html',
  styleUrls: ['./org-editor.component.css']
})
export class OrgEditorComponent {
  public static Route: Route = {
    path: 'organization/:id/org-editor',
    component: OrgEditorComponent, 
    title: 'Update Organization', 
    resolve: { profile: profileResolver }
  };

  /** Store the organization and its observable.  */
  public organization$: Observable<OrganizationSummary> | null = null;
  public org: OrganizationSummary | null = null;
  
  /** Store the currently-logged-in user's profile.  */
  public profile: Profile | null = null;

  /** Stores the user permission value for current organization. */
  public permValue: number = -1;

  /** Stores whether the user has admin permission over the current organization. */
  public adminPermission: boolean = false;

  /** Store the organization id.  */
  id: number = -1;

  public orgForm = this.formBuilder.group({
    name: "",
    slug: "",
    logo: "",
    short_description: "",
    long_description: "",
    email: "",
    website: "",
    instagram: "",
    linked_in: "",
    youtube: "",
    heel_life: ""
  });

  ngOnInit(): void {
     /** Get currently-logged-in user. */
     const data = this.route.snapshot.data as { profile: Profile };
     this.profile = data.profile;

     // Load current route ID
     let id = this.route.snapshot.params['id'];
     this.id = id;
 
     // Retrieve Organization using OrgDetailsService
     this.organization$ = this.orgEditorService.getOrganization(this.id);
     this.organization$.subscribe(organization => this.org = organization);
 
     // Set permission value if profile exists
     if(this.profile) {
       let assocFilter = this.profile.organization_associations.filter((orgRole) => orgRole.org_id == +this.id);
       if(assocFilter.length > 0) {
         this.permValue = assocFilter[0].membership_type.valueOf();
         this.adminPermission = (this.permValue >= 1);
         console.log(this.adminPermission);
       }
     }

    this.orgEditorService.getOrganization(this.id).subscribe((organization) => {
      this.org = organization;
      let org = this.org;

      if(org) {
        this.orgForm.setValue({
          name: String(org.name),
          slug: String(org.slug),
          logo: String(org.logo),
          short_description: String(org.short_description),
          long_description: String(org.long_description),
          email: String(org.email),
          website: String(org.website),
          instagram: String(org.instagram),
          linked_in: String(org.linked_in),
          youtube: String(org.youtube),
          heel_life: String(org.heel_life)
        });
      }
    });
  }

  constructor(private route: ActivatedRoute, private router: Router, protected formBuilder: FormBuilder, protected snackBar: MatSnackBar, private orgEditorService: OrgEditorService) {}

  /** Event handler to handle submitting the Update Organization Form.
   * @returns {void}
  */
  onSubmit(): void {
    if (this.orgForm.valid && this.org) {
      Object.assign(this.org, this.orgForm.value)
      this.orgEditorService.updateOrganization(this.org).subscribe(
        {
          next: (org) => this.onSuccess(org),
          error: (err) => this.onError(err)
        } 
      );
      this.router.navigate(['/organization/', this.id]);
    }
  }

  /** Opens a confirmation snackbar when an organization is successfully updated.
   * @returns {void}
  */
  private onSuccess(org: OrganizationSummary) {
    this.snackBar.open("Organization Updated", "", { duration: 2000 })
  }

  /** Opens a confirmation snackbar when there is an error updating an organization.
   * @returns {void}
  */
  private onError(err: any) {
    console.error("Error: Organization Not Updated");
  }
}
