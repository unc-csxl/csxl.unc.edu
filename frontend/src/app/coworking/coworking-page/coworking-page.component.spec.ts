import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CoworkingPageComponent } from './coworking-page.component';

describe('CoworkingPageComponent', () => {
  let component: CoworkingPageComponent;
  let fixture: ComponentFixture<CoworkingPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [CoworkingPageComponent]
    })
      .compileComponents();

    fixture = TestBed.createComponent(CoworkingPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
