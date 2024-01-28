/**
 * The Community Agreement Widget showcases the agreement that existing and new users
 * will have to sign. It is currently used on the coworking home page and the profile
 * page. It also checks whether or not users have accepted.
 *
 * @author Matt Vu
 * @copyright 2023
 * @license MIT
 */

import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { HttpClient } from '@angular/common/http';
import { ProfileService } from 'src/app/profile/profile.service';

@Component({
  selector: 'community-agreement',
  templateUrl: './community-agreement.widget.html',
  styleUrls: ['./community-agreement.widget.css']
})
export class CommunityAgreement implements OnInit {
  public has_user_agreed: boolean = false;

  constructor(
    public dialogRef: MatDialogRef<CommunityAgreement>,
    public profileService: ProfileService,
    private http: HttpClient,
    @Inject(MAT_DIALOG_DATA) public data: any
  ) {}

  ngOnInit(): void {
    this.profileService.profile$.subscribe((profile) => {
      if (profile) {
        this.has_user_agreed = profile?.has_agreed;
      }
    });
  }
  onButtonClick() {
    if (this.has_user_agreed) {
      this.onCloseClick();
    } else {
      this.onAcceptClick();
    }
  }

  onCloseClick(): void {
    this.dialogRef.close();
  }

  onAcceptClick() {
    this.profileService.profile$.subscribe((profile) => {
      if (profile) {
        profile.has_agreed = true;
        const url = '/api/profile';
        this.http.put(url, profile).subscribe();
      }
    });
    this.dialogRef.close();
  }
}
