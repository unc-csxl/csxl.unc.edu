import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ReservationEditorComponent } from './reservation-editor.component';

describe('ReservationEditorComponent', () => {
  let component: ReservationEditorComponent;
  let fixture: ComponentFixture<ReservationEditorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ReservationEditorComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ReservationEditorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
