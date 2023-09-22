import { TestBed } from '@angular/core/testing';

import { SocialMediaIconWidgetService } from './social-media-icon.widget.service';

describe('SocialMediaIconWidgetService', () => {
  let service: SocialMediaIconWidgetService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SocialMediaIconWidgetService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
