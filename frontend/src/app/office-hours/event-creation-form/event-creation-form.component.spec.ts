import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EventCreationFormComponent } from './event-creation-form.component';

describe('EventCreationFormComponent', () => {
  let component: EventCreationFormComponent;
  let fixture: ComponentFixture<EventCreationFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [EventCreationFormComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(EventCreationFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
