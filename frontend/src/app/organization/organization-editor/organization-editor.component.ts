/**
 * The Organization Editor Component allows organization managers to edit information
 * about their organization which is publically displayed on the organizations page.
 * 
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2023
 * @license MIT
 */

import { Component } from '@angular/core';
import { ActivatedRoute, Route, Router } from '@angular/router';
import { FormBuilder, FormControl, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Observable } from 'rxjs';
import { profileResolver } from 'src/app/profile/profile.resolver';
import { PermissionService } from 'src/app/permission.service';
import { Organization, OrganizationService } from '../organization.service';
import { Profile } from 'src/app/profile/profile.service';

@Component({
  selector: 'app-organization-editor',
  templateUrl: './organization-editor.component.html',
  styleUrls: ['./organization-editor.component.css']
})
export class OrganizationEditorComponent {
  public static Route: Route = {
    path: ':slug/edit',
    component: OrganizationEditorComponent,
    title: 'Organization Editor',
    resolve: { profile: profileResolver }
  };

  /** Store the organization and its observable.  */
  public organization$: Observable<Organization> | null = null;
  public organization: Organization;

  /** Store the currently-logged-in user's profile.  */
  public profile: Profile | null = null;

  /** Stores whether the user has admin permission over the current organization. */
  public adminPermission: boolean = false;

  /** Store the organization id. */
  organization_slug: string = 'new';

  /** Organization Editor Form */
  public organizationForm = this.formBuilder.group({
    name: "",
    slug: "",
    shorthand: "",
    logo: "",
    short_description: "",
    long_description: "",
    email: "",
    website: "",
    instagram: "",
    linked_in: "",
    youtube: "",
    heel_life: "",
    public: false
  });

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    protected formBuilder: FormBuilder,
    protected snackBar: MatSnackBar,
    private organizationService: OrganizationService,
    private permission: PermissionService) {
    /** Add validators to the form */
    const form = this.organizationForm;
    form.get('name')?.addValidators(Validators.required);
    form.get('logo')?.addValidators(Validators.required);
    form.get('short_description')?.addValidators(Validators.required);

    /** Get currently-logged-in user. */
    const data = this.route.snapshot.data as { profile: Profile };
    this.profile = data.profile;

    /** Get id from the url */
    let organization_slug = this.route.snapshot.params['slug'];
    this.organization_slug = organization_slug;

    /** Set permission value if profile exists */
    if (this.organization_slug == 'new') {
      this.permission.check('admin.view', 'admin/').subscribe((perm) => this.adminPermission = perm)
    }

    /** Initialize organization */
    this.organization = {
      id: null,
      name: "",
      shorthand: "",
      slug: "",
      logo: "",
      short_description: "",
      long_description: "",
      email: "",
      website: "",
      instagram: "",
      linked_in: "",
      youtube: "",
      heel_life: "",
      public: false
    };
  }

  /** Event handler to handle submitting the Update Organization Form.
   * @returns {void}
   */
  onSubmit(): void {
    if (this.organizationForm.valid) {
      Object.assign(this.organization, this.organizationForm.value)
      this.organizationService.createOrganization(this.organization).subscribe(
        {
          next: (organization) => this.onSuccess(organization),
          error: (err) => this.onError(err)
        }
      );
    }
  }

  /** Event handler to handle the first change in the organization name field
   * Automatically generates a slug from the organization name (that can be edited)
   * @returns {void}
   */
  generateSlug(): void {
    const name = this.organizationForm.controls['name'].value;
    const slug = this.organizationForm.controls['slug'].value;
    if(name && !slug) {
      var generatedSlug = name.toLowerCase().replace(/[^a-zA-Z0-9]/g, "-");
      this.organizationForm.setControl("slug", new FormControl(generatedSlug));
    }
  }

  /** Opens a confirmation snackbar when an organization is successfully updated.
   * @returns {void}
   */
  private onSuccess(organization: Organization): void {
    this.router.navigate(['/organizations/', organization.slug]);
    this.snackBar.open("Organization Created", "", { duration: 2000 })
  }

  /** Opens a snackbar when there is an error updating an organization.
   * @returns {void}
   */
  private onError(err: any): void {
    console.error("Error: Organization Not Created");
    this.snackBar.open("Error: Organization Not Created", "", { duration: 2000 })
  }
}
