/**
 * The Community Agreement Widget showcases the agreement that existing and new users
 * will have to sign. It is currently used on the coworking home page and the 'About the
 * XL' page. It also checks whether or not users have accepted.
 *
 * @author Matt Vu
 * @copyright 2024
 * @license MIT
 */

import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Profile } from 'src/app/models.module';
import { ProfileService } from 'src/app/profile/profile.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'community-agreement',
  templateUrl: './community-agreement.widget.html',
  styleUrls: ['./community-agreement.widget.css']
})
export class CommunityAgreement {
  public has_user_agreed: boolean | undefined = false;
  public agreementSectionsAccepted: boolean[];
  public loggedInUser: Profile | undefined;
  private subscription: Subscription;

  constructor(
    public dialogRef: MatDialogRef<CommunityAgreement>,
    public profileService: ProfileService,
    @Inject(MAT_DIALOG_DATA) public data: any,
    public snackBar: MatSnackBar
  ) {
    this.agreementSectionsAccepted = new Array(12).fill(false);
    this.subscription = this.profileService.profile$.subscribe((profile) => {
      this.loggedInUser = profile;
      this.has_user_agreed = this.loggedInUser?.accepted_community_agreement;
    });
  }

  onButtonClick() {
    if (this.has_user_agreed) {
      this.onCloseClick();
    } else {
      if (this.allSectionsAccepted()) {
        this.onAcceptClick();
        this.snackBar.open('Successfully Accepted Community Agreement', '', {
          duration: 2000
        });
      } else {
        this.snackBar.open(
          'Please Accept All Terms in the Community Agreement',
          '',
          { duration: 2000 }
        );
      }
    }
  }

  onCloseClick(): void {
    this.dialogRef.close();
  }

  onAcceptClick() {
    if (this.loggedInUser) {
      this.loggedInUser.accepted_community_agreement = true;
      this.profileService.put(this.loggedInUser).subscribe();
    }
    this.dialogRef.close();
  }

  updateSectionAcceptance(index: number, isAccepted: boolean): void {
    this.agreementSectionsAccepted[index] = isAccepted;
  }

  allSectionsAccepted(): boolean {
    return this.agreementSectionsAccepted.every((value) => value);
  }
}
