import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OfficeHoursPageComponent } from './office-hours-page.component';

describe('OfficeHoursPageComponent', () => {
  let component: OfficeHoursPageComponent;
  let fixture: ComponentFixture<OfficeHoursPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [OfficeHoursPageComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(OfficeHoursPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
