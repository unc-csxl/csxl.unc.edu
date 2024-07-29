/**
 * The Welcome Component showcases news articles and details relevant to the user.
 *
 * @author Ajay Gandecha
 * @copyright 2024
 * @license MIT
 */

import {
  Component,
  OnInit,
  Signal,
  WritableSignal,
  computed,
  effect,
  signal
} from '@angular/core';
import { welcomeResolver } from '../welcome.resolver';
import { WelcomeOverview } from '../welcome.model';
import { ActivatedRoute } from '@angular/router';
import { ProfileService } from 'src/app/profile/profile.service';
import { NagivationAdminGearService } from 'src/app/navigation/navigation-admin-gear.service';
import { WelcomeService } from '../welcome.service';
import { profileResolver } from 'src/app/profile/profile.resolver';
import { Profile } from 'src/app/models.module';

@Component({
  selector: 'app-welcome-page',
  templateUrl: './welcome-page.component.html',
  styleUrl: './welcome-page.component.css'
})
export class WelcomePageComponent implements OnInit {
  /** Route information to be used in the routing module */
  public static Route = {
    path: '',
    title: 'CS Experience Labs @ UNC',
    component: WelcomePageComponent,
    resolve: {
      profile: profileResolver
    }
  };

  /** Variable to store the current welcome status. */
  welcomeOverview: WritableSignal<WelcomeOverview | undefined> =
    signal(undefined);

  /** Signal to determine the opening office hours. */
  openOperatingHours = computed(() => {
    let now = new Date();
    return this.welcomeOverview()!.operating_hours.find(
      (hours) => hours.start <= now
    );
  });

  /** Constructor */
  constructor(
    private route: ActivatedRoute,
    protected profileService: ProfileService,
    private gearService: NagivationAdminGearService,
    protected welcomeService: WelcomeService
  ) {
    const data = this.route.snapshot.data as {
      profile: Profile | undefined;
    };

    // If the user is logged in, call the regular API.
    // If the user is logged out, call the unauthenticated API.
    if (data.profile) {
      this.welcomeService.getWelcomeStatus().subscribe((welcomeStatus) => {
        this.welcomeOverview.set(welcomeStatus);
      });
    } else {
      this.welcomeService
        .getWelcomeStatusUnauthenticated()
        .subscribe((welcomeStatus) => {
          this.welcomeOverview.set(welcomeStatus);
        });
    }
  }

  ngOnInit(): void {
    this.gearService.showAdminGearByPermissionCheck(
      'article.*',
      '*',
      '',
      'article/admin'
    );
  }
}
