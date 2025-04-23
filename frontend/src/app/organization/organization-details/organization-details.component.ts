/**
 * The Organization Detail Component displays more information and options regarding
 * UNC CS organizations.
 *
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2024
 * @license MIT
 */

import { Component, OnInit } from '@angular/core';
import {
  ActivatedRoute,
  ActivatedRouteSnapshot,
  ResolveFn,
  Route
} from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Organization, OrganizationMembership } from '../organization.model';
import { OrganizationRosterService } from '../widgets/organization-roster/organization-roster.widget.service';
import { Profile, ProfileService } from '../../profile/profile.service';
import { organizationResolver } from '../organization.resolver';
import { EventService } from '../../event/event.service';
import { Observable } from 'rxjs';
import { PermissionService } from '../../permission.service';
import { GroupEventsPipe } from '../../event/pipes/group-events.pipe';
import { NagivationAdminGearService } from 'src/app/navigation/navigation-admin-gear.service';
import { EventOverview, EventStatusOverview } from 'src/app/event/event.model';
import {
  TimeRangePaginationParams,
  DEFAULT_TIME_RANGE_PARAMS,
  Paginated
} from 'src/app/pagination';
import { signal, WritableSignal, computed } from '@angular/core';

/** Injects the organization's name to adjust the title. */
let titleResolver: ResolveFn<string> = (route: ActivatedRouteSnapshot) => {
  return (
    route.parent!.data['organization']?.shorthand ?? 'Organization Not Found'
  );
};

@Component({
  selector: 'app-organization-details',
  templateUrl: './organization-details.component.html',
  styleUrls: ['./organization-details.component.css']
})
export class OrganizationDetailsComponent implements OnInit {
  /** Route information to be used in Organization Routing Module */
  public static Route: Route = {
    path: ':slug',
    component: OrganizationDetailsComponent,
    resolve: {
      organization: organizationResolver
    },
    children: [
      {
        path: '',
        title: titleResolver,
        component: OrganizationDetailsComponent
      }
    ]
  };

  public eventStatus: WritableSignal<EventStatusOverview | undefined> =
    signal(undefined);
  public page: WritableSignal<
    Paginated<EventOverview, TimeRangePaginationParams> | undefined
  > = signal(undefined);
  private previousParams: TimeRangePaginationParams = DEFAULT_TIME_RANGE_PARAMS;

  protected eventsByDate = computed(() => {
    const items = this.page()?.items ?? [];
    // 👇 Replace 'event.organization.slug' with the actual key from your model
    const filtered = items.filter(
      (event) => event.organization_slug === this.organization?.slug
    );
    return this.groupEventsPipe.transform(filtered);
  });
  /** Store the currently-logged-in user's profile.  */
  public profile: Profile;

  /** The organization to show */
  public organization: Organization | undefined;

  /** The organization's roster to show */
  public organizationRoster: OrganizationMembership[] | undefined;

  // TODO: Refactor once the event feature is refactored.
  /** Whether or not the user has permission to update events. */
  public eventCreationPermission$: Observable<boolean>;

  /** Constructs the Organization Detail component */
  constructor(
    private route: ActivatedRoute,
    protected snackBar: MatSnackBar,
    private profileService: ProfileService,
    protected organizationRosterService: OrganizationRosterService,
    protected eventService: EventService,
    protected groupEventsPipe: GroupEventsPipe,
    private permission: PermissionService,
    private gearService: NagivationAdminGearService
  ) {
    this.profile = this.profileService.profile()!;

    const data = this.route.snapshot.data as {
      organization: Organization;
      events: Event[];
    };

    this.organization = data.organization;

    if (this.organization) {
      this.getRoster(this.organization.slug);
    }

    this.eventCreationPermission$ = this.permission.check(
      'organization.*',
      `organization/${this.organization?.slug ?? '*'}`
    );

    // TEST START
    this.eventService
      .getEvents(this.previousParams, this.profile !== undefined)
      .subscribe((events) => {
        this.page.set(events);
      });

    this.eventService
      .getEventStatus(this.profile !== undefined)
      .subscribe((status) => {
        this.eventStatus.set(status);
      });
    // TEST END
  }

  ngOnInit(): void {
    this.gearService.showAdminGearByPermissionCheck(
      'organization.*',
      `organization/${this.organization?.slug}`,
      '',
      `/organizations/${this.organization?.slug}/edit`
    );
  }

  private getRoster(slug: string): void {
    this.organizationRosterService.getOrganizationRoster(slug).subscribe({
      next: (roster) => {
        if (roster?.length !== 0) {
          this.organizationRoster = roster;
        }
      }
    });
  }

  // Arrow function is necessary to make sure "this.service" is still passed with child
  protected joinOrganization = (
    slug: string,
    user_id: number,
    onSuccess: () => void
  ): void => {
    this.organizationRosterService
      .addOrganizationMembership(slug, user_id)
      .subscribe({
        complete: () => {
          this.getRoster(slug);
          onSuccess();
        },
        error: (error) => {
          this.snackBar.open('Unable to join organization', 'Close', {
            duration: 5000
          });
        }
      });
  };

  reloadPage() {
    this.eventService
      .getEvents(this.previousParams, this.profile !== undefined)
      .subscribe((events) => {
        this.page.set(events);
      });
    this.eventService
      .getEventStatus(this.profile !== undefined)
      .subscribe((status) => {
        this.eventStatus.set(status);
      });
  }
}
