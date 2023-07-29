import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OrgRosterComponent } from './org-roster.component';

describe('OrgRosterComponent', () => {
  let component: OrgRosterComponent;
  let fixture: ComponentFixture<OrgRosterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ OrgRosterComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(OrgRosterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
