import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TicketQueuePageComponent } from './ticket-queue-page.component';

describe('TicketQueuePageComponent', () => {
  let component: TicketQueuePageComponent;
  let fixture: ComponentFixture<TicketQueuePageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TicketQueuePageComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TicketQueuePageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
