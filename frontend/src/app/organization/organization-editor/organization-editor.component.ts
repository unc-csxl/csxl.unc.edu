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
import { Organization } from '../organization.model';
import { Profile, ProfileService } from 'src/app/profile/profile.service';
import { organizationResolver } from '../organization.resolver';
import { OrganizationService } from '../organization.service';
import { organizationEditorGuard } from './organization-editor.guard';

@Component({
  selector: 'app-organization-editor',
  templateUrl: './organization-editor.component.html',
  styleUrls: ['./organization-editor.component.css']
})
export class OrganizationEditorComponent {
  /** Route information to be used in Organization Routing Module */
  public static Route: Route = {
    path: ':slug/edit',
    component: OrganizationEditorComponent,
    title: 'Organization Editor',
    canActivate: [organizationEditorGuard],
    resolve: {
      organization: organizationResolver
    }
  };

  /** Store the organization.  */
  public organization: Organization;

  /** Store the currently-logged-in user's profile.  */
  public profile: Profile;

  /** Organization Editor Form */
  public organizationForm = this.formBuilder.group({
    name: new FormControl('', [Validators.required]),
    slug: new FormControl('', [
      Validators.required,
      Validators.pattern('^(?!new$)[a-z0-9-]+$')
    ]),
    logo: new FormControl('', [Validators.required]),
    short_description: new FormControl('', [
      Validators.required,
      Validators.maxLength(150)
    ]),
    long_description: new FormControl('', [Validators.maxLength(2000)]),
    email: new FormControl('', [Validators.email]),
    shorthand: '',
    website: '',
    instagram: '',
    linked_in: '',
    youtube: '',
    heel_life: '',
    public: false
  });

  /** Constructs the organization editor component */
  constructor(
    private route: ActivatedRoute,
    private router: Router,
    protected formBuilder: FormBuilder,
    protected snackBar: MatSnackBar,
    private organizationService: OrganizationService,
    private profileService: ProfileService
  ) {
    /** Initialize the profile. */
    this.profile = this.profileService.profile()!;

    /** Initialize data from resolvers. */
    const data = this.route.snapshot.data as {
      organization: Organization;
    };

    this.organization = data.organization;

    /** Set organization form data */
    this.organizationForm.patchValue(this.organization);
  }

  /** Event handler to handle submitting the Update Organization Form.
   * @returns {void}
   */
  onSubmit(): void {
    if (this.organizationForm.valid) {
      Object.assign(this.organization, this.organizationForm.value);

      let submittedOrganization = this.isNew()
        ? this.organizationService.createOrganization(this.organization)
        : this.organizationService.updateOrganization(this.organization);

      submittedOrganization.subscribe({
        next: (organization) => this.onSuccess(organization),
        error: (err) => this.onError(err)
      });
    }
  }

  /** Event handler to handle cancelling the editor and going back to
   * the previous organization page.
   * @returns {void}
   */
  onCancel(): void {
    this.router.navigate([`organizations/${this.organization.slug}`]);
  }

  /** Opens a confirmation snackbar when an organization is successfully updated.
   * @returns {void}
   */
  private onSuccess(organization: Organization): void {
    this.router.navigate(['/organizations/', organization.slug]);
    this.snackBar.open(`Organization ${this.action()}`, '', { duration: 2000 });
  }

  /** Opens a snackbar when there is an error updating an organization.
   * @returns {void}
   */
  private onError(err: any): void {
    this.snackBar.open(`Error: Organization Not ${this.action()}`, '', {
      duration: 2000
    });
  }

  /** Event handler to handle the first change in the organization name field
   * Automatically generates a slug from the organization name (that can be edited)
   * @returns {void}
   */
  generateSlug(): void {
    const name = this.organizationForm.controls['name'].value;
    const slug = this.organizationForm.controls['slug'].value;
    if (name && !slug) {
      var generatedSlug = name.toLowerCase().replace(/[^a-zA-Z0-9]/g, '-');
      this.organizationForm.setControl('slug', new FormControl(generatedSlug));
    }
  }

  /** Retreives an error message if an email is invalid */
  getEmailErrorMessage() {
    return this.organizationForm.controls['email'].hasError('email')
      ? 'Not a valid email'
      : '';
  }

  /** Shorthand for whether an organization is new or not. */
  isNew(): boolean {
    return this.organization.slug === 'new';
  }

  /** Shorthand for determining the action being performed on the organization. */
  action(): string {
    return this.isNew() ? 'Created' : 'Updated';
  }
}
