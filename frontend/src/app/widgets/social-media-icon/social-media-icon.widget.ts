import { Component, Input } from '@angular/core';
import { MatIconRegistry } from '@angular/material/icon';
import { DomSanitizer } from '@angular/platform-browser';

@Component({
    selector: 'social-media-icon',
    templateUrl: './social-media-icon.widget.html',
    styleUrls: ['./social-media-icon.widget.css']
})
export class SocialMediaIcon{

    @Input() fontIcon: string = "";
    @Input() svgIcon: string = "";
    @Input() href: string = "";

    constructor(private iconRegistry: MatIconRegistry, private sanitizer: DomSanitizer) {

        /** Import Logos using MatIconRegistry */
        iconRegistry.addSvgIcon('instagram', sanitizer.bypassSecurityTrustResourceUrl('https://simpleicons.org/icons/instagram.svg'));
        iconRegistry.addSvgIcon('github', sanitizer.bypassSecurityTrustResourceUrl('https://simpleicons.org/icons/github.svg'));
        iconRegistry.addSvgIcon('linkedin', sanitizer.bypassSecurityTrustResourceUrl('https://simpleicons.org/icons/linkedin.svg'))
        iconRegistry.addSvgIcon('youtube', sanitizer.bypassSecurityTrustResourceUrl('https://simpleicons.org/icons/youtube.svg'))
    }
}


