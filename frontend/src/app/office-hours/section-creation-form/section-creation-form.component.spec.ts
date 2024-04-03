import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SectionCreationFormComponent } from './section-creation-form.component';

describe('SectionCreationFormComponent', () => {
  let component: SectionCreationFormComponent;
  let fixture: ComponentFixture<SectionCreationFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SectionCreationFormComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SectionCreationFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
