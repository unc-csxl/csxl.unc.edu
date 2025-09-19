import { Component, Input } from '@angular/core';
import { MatIconRegistry } from '@angular/material/icon';
import { DomSanitizer } from '@angular/platform-browser';
import { SocialMediaIconWidgetService } from './social-media-icon.widget.service';

@Component({
    selector: 'social-media-icon',
    templateUrl: './social-media-icon.widget.html',
    styleUrls: ['./social-media-icon.widget.css'],
    standalone: false
})
export class SocialMediaIcon {
  @Input() fontIcon: string = '';
  @Input() svgIcon: string = '';
  @Input() href: string = '';

  constructor(private _: SocialMediaIconWidgetService) {}
}
