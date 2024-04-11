import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InstructorSectionHomeComponent } from './instructor-section-home.component';

describe('InstructorSectionHomeComponent', () => {
  let component: InstructorSectionHomeComponent;
  let fixture: ComponentFixture<InstructorSectionHomeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [InstructorSectionHomeComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(InstructorSectionHomeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
