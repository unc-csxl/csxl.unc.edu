/**
 * The Coworking Component serves as the hub for students to create reservations
 * for tables, rooms, and equipment from the CSXL.
 *
 * @author Kris Jordan, Ajay Gandecha, John Schachte
 * @copyright 2024
 * @license MIT
 */

import { Component, OnDestroy, OnInit, Signal, computed } from '@angular/core';
import { ActivatedRoute, Route, Router } from '@angular/router';
import { isAuthenticated } from 'src/app/gate/gate.guard';
import { profileResolver } from 'src/app/profile/profile.resolver';
import { CoworkingService } from '../coworking.service';
import { Profile } from 'src/app/models.module';
import { ProfileService } from 'src/app/profile/profile.service';
import {
  CoworkingStatus,
  Reservation,
  SeatAvailability
} from '../coworking.models';
import { Subscription, timer } from 'rxjs';
import { RoomReservationService } from '../room-reservation/room-reservation.service';
import { ReservationService } from '../reservation/reservation.service';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-coworking-home',
  templateUrl: './coworking-home.component.html',
  styleUrls: ['./coworking-home.component.css']
})
export class CoworkingPageComponent implements OnInit, OnDestroy {
  public status: Signal<CoworkingStatus>;

  /** Store the currently-logged-in user's profile.  */
  public profile: Profile | null = null;

  openOperatingHours = computed(() => {
    let now = new Date();
    return this.status().operating_hours.find((hours) => hours.start <= now);
  });

  upcomingReservations = computed(() => {
    const isUpcomingRoomReservation = (reservation: Reservation) => {
      return (
        !this.coworkingService.findActiveReservationPredicate(reservation) &&
        reservation &&
        reservation.room &&
        reservation.state === 'CONFIRMED'
      );
    };

    return this.status().my_reservations.filter(isUpcomingRoomReservation);
  });

  isOpen = computed(() => {
    let now = new Date();
    let hours = this.openOperatingHours();
    return hours && hours.start <= now && hours.end > now;
  });

  activeReservation = computed(() => {
    return this.status().my_reservations.find(
      this.coworkingService.findActiveReservationPredicate
    );
  });

  private timerSubscription!: Subscription;

  /** Route information to be used in App Routing Module */
  public static Route: Route = {
    path: '',
    component: CoworkingPageComponent,
    title: 'Coworking',
    canActivate: [isAuthenticated],
    resolve: { profile: profileResolver }
  };

  constructor(
    public coworkingService: CoworkingService,
    private router: Router,
    private route: ActivatedRoute,
    private reservationService: ReservationService,
    protected snackBar: MatSnackBar,
    private roomReservationService: RoomReservationService,
    private profileService: ProfileService,
    private dialog: MatDialog
  ) {
    this.status = coworkingService.status;

    const data = this.route.snapshot.data as {
      profile: Profile;
    };
    this.profile = data.profile;
  }

  /**
   * A lifecycle hook that is called after Angular has initialized all data-bound properties of a directive.
   *
   * Use this hook to initialize the directive or component. This is the right place to fetch data from a server,
   * set up any local state, or perform operations that need to be executed only once when the component is instantiated.
   *
   * @returns {void} - This method does not return a value.
   */
  ngOnInit(): void {
    this.status = this.coworkingService.status;
    this.timerSubscription = timer(0, 10000).subscribe(() => {
      this.coworkingService.pollStatus();
    });
  }

  ngOnDestroy(): void {
    this.timerSubscription.unsubscribe();
  }

  reserve(seatSelection: SeatAvailability[]) {
    this.coworkingService.draftReservation(seatSelection).subscribe({
      error: (response) => {
        this.snackBar.open(
          response.error.message,
          '',
          { duration: 8000 }
        );
      },
      next: (reservation) => {
        this.router.navigateByUrl(`/coworking/reservation/${reservation.id}`);
      }
    });
  }

  navigateToNewReservation() {
    this.router.navigateByUrl('/coworking/new-reservation');
  }
}
