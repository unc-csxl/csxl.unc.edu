import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StudentSectionHomeComponent } from './student-section-home.component';

describe('StudentSectionHomeComponent', () => {
  let component: StudentSectionHomeComponent;
  let fixture: ComponentFixture<StudentSectionHomeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ StudentSectionHomeComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(StudentSectionHomeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
