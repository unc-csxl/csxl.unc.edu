import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OrganizationEditorComponent } from './organization-editor.component';

describe('OrganizationEditorComponent', () => {
  let component: OrganizationEditorComponent;
  let fixture: ComponentFixture<OrganizationEditorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ OrganizationEditorComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(OrganizationEditorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
