import { Component, Input } from '@angular/core';

@Component({
  selector: 'application-card',
  templateUrl: './application-card.widget.html',
  styleUrl: './application-card.widget.css'
})
export class ApplicationCardWidget {
  @Input() item!: string;
}
