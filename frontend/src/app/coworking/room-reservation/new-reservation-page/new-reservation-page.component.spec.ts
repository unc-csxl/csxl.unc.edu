import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NewReservationPageComponent } from './new-reservation-page.component';

describe('NewReservationPageComponent', () => {
  let component: NewReservationPageComponent;
  let fixture: ComponentFixture<NewReservationPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [NewReservationPageComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(NewReservationPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
