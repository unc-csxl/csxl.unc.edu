import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MatStrokedIconButtonComponent } from './mat-stroked-icon-button.component';

describe('MatStrokedIconButtonComponent', () => {
  let component: MatStrokedIconButtonComponent;
  let fixture: ComponentFixture<MatStrokedIconButtonComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MatStrokedIconButtonComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(MatStrokedIconButtonComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
