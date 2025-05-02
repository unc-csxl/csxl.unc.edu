import { Injectable } from '@angular/core';
import { MatIconRegistry } from '@angular/material/icon';
import { DomSanitizer } from '@angular/platform-browser';

@Injectable({
  providedIn: 'root'
})
export class SocialMediaIconWidgetService {
  constructor(
    private iconRegistry: MatIconRegistry,
    private sanitizer: DomSanitizer
  ) {
    iconRegistry.addSvgIcon(
      'instagram',
      sanitizer.bypassSecurityTrustResourceUrl(
        'https://simpleicons.org/icons/instagram.svg'
      )
    );
    iconRegistry.addSvgIcon(
      'github',
      sanitizer.bypassSecurityTrustResourceUrl(
        'https://simpleicons.org/icons/github.svg'
      )
    );
    iconRegistry.addSvgIcon(
      'slack',
      sanitizer.bypassSecurityTrustResourceUrl(
        'https://simpleicons.org/icons/slack.svg'
      )
    );
    iconRegistry.addSvgIcon(
      'linkedin',
      sanitizer.bypassSecurityTrustResourceUrl('/assets/linkedin-logo.svg')
    );
    iconRegistry.addSvgIcon(
      'youtube',
      sanitizer.bypassSecurityTrustResourceUrl(
        'https://simpleicons.org/icons/youtube.svg'
      )
    );
  }
}
