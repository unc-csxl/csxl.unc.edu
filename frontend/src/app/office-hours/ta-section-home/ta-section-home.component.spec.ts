import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TaSectionHomeComponent } from './ta-section-home.component';

describe('TaSectionHomeComponent', () => {
  let component: TaSectionHomeComponent;
  let fixture: ComponentFixture<TaSectionHomeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [TaSectionHomeComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(TaSectionHomeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
