import { Component, Input } from '@angular/core';
import { ApplicationReviewOverview } from '../../hiring.models';
import { MatDialog } from '@angular/material/dialog';

@Component({
  selector: 'application-card',
  templateUrl: './application-card.widget.html',
  styleUrl: './application-card.widget.css'
})
export class ApplicationCardWidget {
  @Input() item!: ApplicationReviewOverview;

  constructor(protected dialog: MatDialog) {}
}
