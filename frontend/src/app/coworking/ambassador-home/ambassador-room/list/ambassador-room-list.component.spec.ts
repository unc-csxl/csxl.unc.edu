import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AmbassadorRoomListComponent } from './ambassador-room-list.component';

describe('AmbassadorRoomListComponent', () => {
  let component: AmbassadorRoomListComponent;
  let fixture: ComponentFixture<AmbassadorRoomListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [AmbassadorRoomListComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(AmbassadorRoomListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
