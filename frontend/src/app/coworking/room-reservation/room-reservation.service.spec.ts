import { TestBed } from '@angular/core/testing';

import { RoomReservationService } from './room-reservation.service';

describe('RoomReservationService', () => {
  let service: RoomReservationService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(RoomReservationService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
