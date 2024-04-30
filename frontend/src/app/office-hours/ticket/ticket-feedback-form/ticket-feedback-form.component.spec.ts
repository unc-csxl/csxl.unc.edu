import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TicketFeedbackFormComponent } from './ticket-feedback-form.component';

describe('TicketFeedbackFormComponent', () => {
  let component: TicketFeedbackFormComponent;
  let fixture: ComponentFixture<TicketFeedbackFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [TicketFeedbackFormComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(TicketFeedbackFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
