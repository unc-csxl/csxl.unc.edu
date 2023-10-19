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
import { permissionGuard } from 'src/app/permission.guard';
import { organizationDetailResolver } from '../organization.resolver'

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
    canActivate: [permissionGuard('admin.view', 'admin/')],
    resolve: { profile: profileResolver, organization: organizationDetailResolver },
  };

  /** Store the organization.  */
  public organization: Organization;

  /** Store the currently-logged-in user's profile.  */
  public profile: Profile | null = null;

  /** Stores whether the user has admin permission over the current organization. */
  public adminPermission$: Observable<boolean>;

  /** Store the organization id. */
  organization_slug: string = 'new';

  /** Add validators to the form */
  name = new FormControl('', [Validators.required]);
  slug = new FormControl('', [Validators.required, Validators.pattern('^(?!new$)[a-z0-9-]+$')]);
  logo = new FormControl('', [Validators.required]);
  email = new FormControl('', [Validators.email]);
  shortDescription = new FormControl('', [Validators.required, Validators.maxLength(150)]);
  longDescription = new FormControl('', [Validators.maxLength(2000)]);

  /** Organization Editor Form */
  public organizationForm = this.formBuilder.group({
    name: this.name,
    slug: this.slug,
    logo: this.logo,
    short_description: this.shortDescription,
    long_description: this.longDescription,
    email: this.email,
    shorthand: "",
    website: "",
    instagram: "",
    linked_in: "",
    youtube: "",
    heel_life: "",
    public: false
  });

  getEmailErrorMessage() {
    return this.email.hasError('email') ? 'Not a valid email' : '';
  }

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    protected formBuilder: FormBuilder,
    protected snackBar: MatSnackBar,
    private organizationService: OrganizationService,
    private permission: PermissionService) {

    /** Get currently-logged-in user and and organization. */
    const data = this.route.snapshot.data as { profile: Profile, organization: Organization };
    this.profile = data.profile;

    /** Initialize organization */
    this.organization = data.organization;

    /** Set organization form data */
    this.organizationForm.setValue({
      name: this.organization.name,
      slug: this.organization.slug,
      shorthand: this.organization.shorthand,
      logo: this.organization.logo,
      short_description: this.organization.short_description,
      long_description: this.organization.long_description,
      email: this.organization.email,
      website: this.organization.website,
      instagram: this.organization.instagram,
      linked_in: this.organization.linked_in,
      youtube: this.organization.youtube,
      heel_life: this.organization.heel_life,
      public: this.organization.public
    })

    /** Get id from the url */
    let organization_slug = this.route.snapshot.params['slug'];
    this.organization_slug = organization_slug;

    /** Set permission value */
    this.adminPermission$ = this.permission.check('admin.view', 'admin/');    
  }

  /** Event handler to handle submitting the Update Organization Form.
   * @returns {void}
   */
  onSubmit(): void {
    if (this.organizationForm.valid) {
      Object.assign(this.organization, this.organizationForm.value)
      if(this.organization_slug == "new") {
        this.organizationService.createOrganization(this.organization).subscribe(
          {
            next: (organization) => this.onSuccess(organization),
            error: (err) => this.onError(err)
          }
        );
      }
      else {
        this.organizationService.updateOrganization(this.organization).subscribe(
          {
            next: (organization) => this.onSuccess(organization),
            error: (err) => this.onError(err)
          }
        );
      }
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
