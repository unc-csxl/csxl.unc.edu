import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OrganizationPageComponent } from './organization-page.component';

describe('OrganizationPageComponent', () => {
  let component: OrganizationPageComponent;
  let fixture: ComponentFixture<OrganizationPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ OrganizationPageComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(OrganizationPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
