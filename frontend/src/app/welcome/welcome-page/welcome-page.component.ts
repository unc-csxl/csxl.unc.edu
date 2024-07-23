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
  computed,
  effect,
  signal
} from '@angular/core';
import { welcomeResolver } from '../welcome.resolver';
import { WelcomeOverview } from '../welcome.model';
import { ActivatedRoute } from '@angular/router';
import { ProfileService } from 'src/app/profile/profile.service';
import { NagivationAdminGearService } from 'src/app/navigation/navigation-admin-gear.service';

@Component({
  selector: 'app-welcome-page',
  templateUrl: './welcome-page.component.html',
  styleUrl: './welcome-page.component.css'
})
export class WelcomePageComponent implements OnInit {
  /** Route information to be used in the routing module */
  public static Route = {
    path: '',
    title: 'Welcome to the CSXL',
    component: WelcomePageComponent,
    resolve: {
      welcomeOverview: welcomeResolver
    }
  };

  /** Variable to store the current welcome status. */
  welcomeOverview: Signal<WelcomeOverview>;

  /** Signal to determine the opening office hours. */
  openOperatingHours = computed(() => {
    let now = new Date();
    return this.welcomeOverview().operating_hours.find(
      (hours) => hours.start <= now
    );
  });

  /** Constructor */
  constructor(
    private route: ActivatedRoute,
    protected profileService: ProfileService,
    private gearService: NagivationAdminGearService
  ) {
    const data = this.route.snapshot.data as {
      welcomeOverview: WelcomeOverview;
    };
    this.welcomeOverview = signal(data.welcomeOverview);
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
