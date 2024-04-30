import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PeopleTableComponent } from './people-table.component';

describe('PeopleTableComponent', () => {
  let component: PeopleTableComponent;
  let fixture: ComponentFixture<PeopleTableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PeopleTableComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PeopleTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
