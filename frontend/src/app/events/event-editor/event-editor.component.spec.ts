import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EventEditorComponent } from './event-editor.component';

describe('EventEditorComponent', () => {
  let component: EventEditorComponent;
  let fixture: ComponentFixture<EventEditorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ EventEditorComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(EventEditorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
