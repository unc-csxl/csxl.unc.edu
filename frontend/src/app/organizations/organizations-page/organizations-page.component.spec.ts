import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OrganizationsPageComponent } from './organizations-page.component';

describe('OrganizationsPageComponent', () => {
  let component: OrganizationsPageComponent;
  let fixture: ComponentFixture<OrganizationsPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ OrganizationsPageComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(OrganizationsPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
