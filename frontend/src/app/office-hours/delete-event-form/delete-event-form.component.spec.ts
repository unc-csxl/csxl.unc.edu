import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DeleteEventFormComponent } from './delete-event-form.component';

describe('DeleteEventFormComponent', () => {
  let component: DeleteEventFormComponent;
  let fixture: ComponentFixture<DeleteEventFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DeleteEventFormComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DeleteEventFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
