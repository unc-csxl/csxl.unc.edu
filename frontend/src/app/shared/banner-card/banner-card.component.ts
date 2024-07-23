import { Component, EventEmitter, Input, Output } from '@angular/core';

export enum BannerType {
  INFO = 'info',
  ALERT = 'alert'
}

@Component({
  selector: 'banner-card',
  templateUrl: './banner-card.component.html',
  styleUrl: './banner-card.component.css'
})
export class BannerCardComponent {
  @Input() type!: string;
  @Input() icon!: string;
  @Input() title!: string;
  @Input() body!: string;
  @Input() bottomActionButton!: boolean;
  @Input() actionButtonText!: string;
  @Input() linkAction?: boolean;
  @Input() link?: string;
  @Output() actionButtonPressed = new EventEmitter<void>();
  @Input() wide: boolean = false;
  @Input() newTab: boolean = false;

  buttonPressed() {
    if (this.linkAction) {
      this.openLink();
    } else {
      this.actionButtonPressed.emit();
    }
  }
  openLink() {
    window.open(this.link ?? '', this.newTab ? '_blank' : '_self');
  }

  bannerClassName(): string {
    switch (this.type) {
      case BannerType.INFO:
        return `mat-csxl-alert-card-info ${this.wide && ' wide-banner-card'}`;
      case BannerType.ALERT:
        return `mat-csxl-alert-card-alert ${this.wide && ' wide-banner-card'}`;
      default:
        return '';
    }
  }
}
