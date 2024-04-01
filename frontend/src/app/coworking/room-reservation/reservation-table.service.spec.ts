import { TestBed } from '@angular/core/testing';

import { ReservationTableService } from './reservation-table.service';

describe('ReservationTableService', () => {
  let service: ReservationTableService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ReservationTableService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
