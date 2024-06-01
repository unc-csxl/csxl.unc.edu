import { Component, Input } from '@angular/core';
import { NagivationAdminGearService } from 'src/app/navigation/navigation-admin-gear.service';

@Component({
  selector: 'admin-fab',
  templateUrl: './admin-fab.component.html',
  styleUrl: './admin-fab.component.css'
})
export class AdminFabComponent {
  @Input() primaryIcon!: string;
  @Input() primaryText!: string;
  @Input() secondaryIcon?: string;

  constructor(
    protected navigationAdminGearService: NagivationAdminGearService
  ) {}
}
