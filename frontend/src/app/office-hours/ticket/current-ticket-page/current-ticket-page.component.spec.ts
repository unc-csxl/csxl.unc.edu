import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CurrentTicketPageComponent } from './current-ticket-page.component';

describe('CurrentTicketPageComponent', () => {
  let component: CurrentTicketPageComponent;
  let fixture: ComponentFixture<CurrentTicketPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CurrentTicketPageComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CurrentTicketPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
