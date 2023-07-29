import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OrgEditorComponent } from './org-editor.component';

describe('OrgEditorComponent', () => {
  let component: OrgEditorComponent;
  let fixture: ComponentFixture<OrgEditorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ OrgEditorComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(OrgEditorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
