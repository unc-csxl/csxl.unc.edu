import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { HttpClient } from '@angular/common/http';
import { ProfileService } from 'src/app/profile/profile.service';

@Component({
  selector: 'community-agreement',
  templateUrl: './community-agreement.widget.html',
  styleUrls: ['./community-agreement.widget.css']
})
export class CommunityAgreement {
  constructor(
    public dialogRef: MatDialogRef<CommunityAgreement>,
    public profileService: ProfileService,
    private http: HttpClient,
    @Inject(MAT_DIALOG_DATA) public data: any
  ) {}

  onCloseClick(): void {
    this.dialogRef.close();
  }

  onAcceptClick() {
    this.profileService.profile$.subscribe((profile) => {
      if (profile) {
        profile.has_agreed = true;
        const url = '/api/profile';
        this.http.put(url, profile).subscribe(
          (updatedProfile) => {
            console.log('Terms accepted successfully:', updatedProfile);
          },
          (error) => {
            console.error('Error accepting terms:', error);
          }
        );
      }
    });
    this.dialogRef.close();
  }
}
