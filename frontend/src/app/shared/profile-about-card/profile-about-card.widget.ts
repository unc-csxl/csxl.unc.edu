import { Component, Input } from '@angular/core';
import { Profile } from '../../models.module';

@Component({
  selector: 'profile-about-card',
  templateUrl: './profile-about-card.widget.html',
  styleUrls: ['./profile-about-card.widget.css']
})
export class ProfileAboutCard {
  @Input() profile!: Profile;

  constructor() {}
}
