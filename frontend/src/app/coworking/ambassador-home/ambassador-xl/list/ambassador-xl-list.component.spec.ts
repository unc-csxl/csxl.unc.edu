import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AmbassadorXlListComponent } from './ambassador-xl-list.component';

describe('AmbassadorXlListComponent', () => {
  let component: AmbassadorXlListComponent;
  let fixture: ComponentFixture<AmbassadorXlListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [AmbassadorXlListComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(AmbassadorXlListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
