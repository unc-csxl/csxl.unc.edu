import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RoomCapacityDialogComponent } from './room-dialogue.component';

describe('RoomCapacityDialogComponent', () => {
  let component: RoomCapacityDialogComponent;
  let fixture: ComponentFixture<RoomCapacityDialogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [RoomCapacityDialogComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(RoomCapacityDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
