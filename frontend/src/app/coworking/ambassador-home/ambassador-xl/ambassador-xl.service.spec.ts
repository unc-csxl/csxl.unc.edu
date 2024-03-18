import { TestBed } from '@angular/core/testing';

import { AmbassadorXlService } from './ambassador-xl.service';

describe('AmbassadorXlService', () => {
  let service: AmbassadorXlService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(AmbassadorXlService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
