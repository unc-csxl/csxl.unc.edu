import { TestBed } from '@angular/core/testing';

import { AmbassadorRoomService } from './ambassador-room.service';

describe('AmbassadorRoomService', () => {
  let service: AmbassadorRoomService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(AmbassadorRoomService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
