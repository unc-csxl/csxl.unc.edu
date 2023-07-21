import { Component } from '@angular/core';
import { ActivatedRoute, Route, Router } from '@angular/router';
import { OrganizationSummary, Profile } from 'src/app/models.module';
import { FormBuilder, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { OrgEditorService } from './org-editor.service';
import { Observable } from 'rxjs';
import { profileResolver } from '../profile/profile.resolver';
import { permissionGuard } from '../permission.guard';
import { PermissionService } from '../permission.service';


@Component({
  selector: 'app-org-editor',
  templateUrl: './org-editor.component.html',
  styleUrls: ['./org-editor.component.css']
})
export class OrgEditorComponent {
  public static Route: Route = {
    path: 'organization/:id/org-editor',
    component: OrgEditorComponent,
    title: 'Organization Editor',
    resolve: { profile: profileResolver }
  };

  /** Store the organization and its observable.  */
  public organization$: Observable<OrganizationSummary> | null = null;
  public org: OrganizationSummary;

  /** Store the currently-logged-in user's profile.  */
  public profile: Profile | null = null;

  /** Stores the user permission value for current organization. */
  public permValue: number = -1;

  /** Stores whether the user has admin permission over the current organization. */
  public adminPermission: boolean = false;

  /** Store the organization id. */
  org_id: number = -1;

  /** Organization Editor Form */
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

  constructor(private route: ActivatedRoute, private router: Router, protected formBuilder: FormBuilder, protected snackBar: MatSnackBar, private orgEditorService: OrgEditorService, private permission: PermissionService) {
    /** Add validators to the form */
    const form = this.orgForm;
    form.get('name')?.addValidators(Validators.required);
    form.get('logo')?.addValidators(Validators.required);
    form.get('short_description')?.addValidators(Validators.required);

    /** Get currently-logged-in user. */
    const data = this.route.snapshot.data as { profile: Profile };
    this.profile = data.profile;

    /** Get id from the url */
    let org_id = this.route.snapshot.params['id'];
    this.org_id = org_id;

    /** Set permission value if profile exists */
    if (this.profile) {
      if (this.org_id == -1) {
        this.permission.check('admin.view', 'admin/').subscribe((perm) => this.adminPermission = perm)
      } else {
        let assocFilter = this.profile.organization_associations.filter((orgRole) => orgRole.org_id == +this.org_id);
        if (assocFilter.length > 0) {
          this.permValue = assocFilter[0].membership_type;
          this.adminPermission = (this.permValue >= 1);
        }
      }
    }

    /** Initialize organization */
    this.org = {
      id: null,
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
    };

    /** Retrieve the event with the eventEditorService */
    if (this.org_id != -1) {
      orgEditorService.getOrganization(this.org_id).subscribe((org) => this.org = org);
    }
  }

  ngOnInit() {
    /** Get currently-logged-in user. */
    const data = this.route.snapshot.data as { profile: Profile };
    this.profile = data.profile;

    /** Get id from the url */
    let org_id = this.route.snapshot.params['id'];
    this.org_id = org_id;

    /** Set permission value if profile exists */
    if (this.profile) {
      if (this.org_id == -1) {
        this.permission.check('admin.view', 'admin/').subscribe((perm) => this.adminPermission = perm)
      } else {
        let assocFilter = this.profile.organization_associations.filter((orgRole) => orgRole.org_id == +this.org_id);
        if (assocFilter.length > 0) {
          this.permValue = assocFilter[0].membership_type;
          this.adminPermission = (this.permValue >= 1);
        }
      }
    }

    /** If you are editing an org (id not default -1) */
    if (this.org_id != -1) {
      /** Get the organization and set the form to the org's values */
      this.orgEditorService.getOrganization(this.org_id).subscribe((org) => { 
        this.org = org;

        this.orgForm.setValue({
          name: org.name,
          slug: org.slug,
          logo: org.logo,
          short_description: org.short_description,
          long_description: org.long_description,
          email: org.email,
          website: org.website,
          instagram: org.instagram,
          linked_in: org.linked_in,
          youtube: org.youtube,
          heel_life: org.heel_life
        });
      
      });

    }

  }

  /** Event handler to handle submitting the Update Organization Form.
   * @returns {void}
   */
  onSubmit = () => {
    if (this.orgForm.valid) {
      Object.assign(this.org, this.orgForm.value)
      this.orgEditorService.updateOrganization(this.org).subscribe(
        {
          next: (org) => this.onSuccess(org),
          error: (err) => this.onError(err)
        }
      );
    }
  }

  /** Opens a confirmation snackbar when an organization is successfully updated.
   * @returns {void}
   */
  private onSuccess = (org: OrganizationSummary) => {
    this.router.navigate(['/organization/', org.id]);
    this.snackBar.open("Organization Updated", "", { duration: 2000 })
  }

  /** Opens a snackbar when there is an error updating an organization.
   * @returns {void}
   */
  private onError = (err: any) => {
    console.error("Error: Organization Not Updated");
    this.snackBar.open("Error: Organization Not Updated", "", { duration: 2000 })
  }
}
